


# helper function for parse result of queries file
import collections
import pickle
import time
from math import log2


def invertDictionaryForQueries(dict):
    '''

    :param dict: {term: { query: tf_in_query}
    :return:   dict of {Query: { Term: tf_ in query}
    '''
    result = {}
    for term in dict:
        for query in dict[term]:
            if query not in result:
                query_dict = {}
                query_dict[term] = dict[term][query]
                result[query] = query_dict
            else:  # for case query is not exists yet on dictionary
                result[query][term] = dict[term][query]
    return result

class Ranker:
    __dictionary_of_posting_pointers = {
        'a': 'abc', 'b': 'abc', 'c': 'abc', 'A': 'abc', 'B': 'abc', 'C': 'abc',
        'd': 'defgh', 'e': 'defgh', 'f': 'defgh', 'g': 'defgh', 'h': 'defgh', 'D': 'defgh', 'E': 'defgh', 'F': 'defgh',
        'G': 'defgh', 'H': 'defgh',
        'i': 'ijklmn', 'j': 'ijklmn', 'k': 'ijklmn', 'l': 'ijklmn', 'm': 'ijklmn', 'n': 'ijklmn', 'I': 'ijklmn',
        'J': 'ijklmn', 'K': 'ijklmn', 'L': 'ijklmn', 'M': 'ijklmn', 'N': 'ijklmn',
        'o': 'opqrs', 'p': 'opqrs', 'q': 'opqrs', 'r': 'opqrs', 's': 'opqrs', 'O': 'opqrs', 'P': 'opqrs', 'R': 'opqrs',
        'S': 'opqrs', 'Q': 'opqrs',
        't': 'tuvwxyz', 'u': 'tuvwxyz', 'v': 'tuvwxyz', 'w': 'tuvwxyz', 'x': 'tuvwxyz', 'y': 'tuvwxyz', 'z': 'tuvwxyz',
        'T': 'tuvwxyz', 'U': 'tuvwxyz', 'V': 'tuvwxyz', 'W': 'tuvwxyz', 'X': 'tuvwxyz', 'Y': 'tuvwxyz', 'Z': 'tuvwxyz'
    }


    #todo: add to documentation- memoization of terms grades

    def __init__(self, docs_dictionary, main_dictionary, avdl, N, stem_suffix, indexPath):
        self.weight_bm_25 = 1
        self.b=0.75
        self.k=2
        self.avdl = avdl
        self.N = N
        self.max_top_docs_to_retrieve = 50
        self.main_dictionary = main_dictionary
        self.docs_dictionary = docs_dictionary
        self.result_bm_25={} # { query : { docNo: final_grade } }
        self.stem_suffix = stem_suffix # "_stem"
        self.indexPath = indexPath
        self.final_result = {} #{ query : { doc : grade} }
        self.weight_title=0.7

        self.__current_posting_file_name = ''
        self.__currentPostingFile = None
        self.__term_grades_in_doc = {}  # { term : {doc:grade}}
        self.mini_posting = {}
        self.city_docs = {}

    def calculate_final_rank(self, ranked_title, ranked_addons):
        '''
        this functions calcs the final garde by weights
        :param ranked_title: { query : { doc : grade} }
        :param ranked_addons: { query : { doc : grade} }
        :return: the final grade by 2 weights
        '''
        if len(ranked_addons) == 0:
            self.final_result = ranked_title
            for query in self.final_result:
                self.final_result[query] = collections.OrderedDict(sorted(self.final_result[query].items(), key=lambda x: x[1], reverse=True))
                self.final_result[query] = self.get_top_50(query)
            return
        for query in ranked_addons:
            self.final_result[query] = {}
            for doc in ranked_addons[query]:
                self.final_result[query][doc] = (1 - self.weight_title) * ranked_addons[query][doc]
        for query in ranked_title:
            for doc in ranked_title[query]:
                if doc not in self.final_result[query]:
                    self.final_result[query][doc] = (self.weight_title) * ranked_title[query][doc]
                else:
                    self.final_result[query][doc] += (self.weight_title) * ranked_title[query][doc]
            self.final_result[query] = collections.OrderedDict(sorted(self.final_result[query].items(), key=lambda x: x[1], reverse=True))
            self.final_result[query] = self.get_top_50(query)

    def calc_bm_25(self, term_tf_dict, query_id):
        '''
        calculate the grades of all docs of one query in dict.
        update result dictionary for all terms in query
        :param { term : tf_in_query } sorted by term
        :param: query id
        '''
        self.result_bm_25[query_id] = {}
        for term in term_tf_dict: # of one query
            if term not in self.__term_grades_in_doc:
                self.__term_grades_in_doc[term] = {}
                if term not in self.main_dictionary:
                    #print (term + " not found in dictionary !!!")
                    continue #no coalculation is needed because the term not exists in corpus
                else:
                    mone = self.N + 0.5 - self.main_dictionary[term].get_df()
                    mechane = 0.5 + self.main_dictionary[term].get_df()
                    idf = log2(mone / mechane)

                    self.__currentPostingFile = self.mini_posting[term]

                    for doc in self.__currentPostingFile:  # for each doc that includes this term
                        if len(self.city_docs) != 0 and doc not in self.city_docs:
                            continue
                        tf_in_doc = self.__currentPostingFile[doc]
                        doc_len = self.docs_dictionary[doc].number_of_words

                        mone = tf_in_doc * (self.k + 1)
                        mechane = tf_in_doc + self.k * (1 - self.b + self.b * (doc_len / self.avdl))
                        okapi = mone / mechane
                        self.__term_grades_in_doc[term][doc] = okapi * idf  # memoization of term in doc
                        if doc not in self.result_bm_25[query_id]:
                            self.result_bm_25[query_id][doc] = 0
                        self.result_bm_25[query_id][doc] += self.__term_grades_in_doc[term][doc] * term_tf_dict[term] #final grade for doc by query
            else: # the term already calculated for all docs
                for doc in self.__term_grades_in_doc[term]:
                    if doc not in self.result_bm_25[query_id]:
                        self.result_bm_25[query_id][doc] = 0
                    self.result_bm_25[query_id][doc] += self.__term_grades_in_doc[term][doc] * term_tf_dict[term]  # final grade for doc by query
        sorted_dic = collections.OrderedDict(sorted(self.result_bm_25[query_id].items(), key=lambda x: x[1], reverse=True))
        return sorted_dic

    def rank(self, query_dict):
        '''
        will rank the files by calculating bm25
        :param query_dict: {Term: {Query : tf_ in query}
        :return: bm25 result {query : {doc : grade}}
        '''
        self.result_bm_25 = {} #initialize
        query_term_tf_dict = invertDictionaryForQueries(query_dict) # dict of {Query: { Term: tf_ in query}
        for query in query_term_tf_dict:
            self.result_bm_25[query] = self.calc_bm_25(query_term_tf_dict[query], query) #override for sorted by grades
        return self.result_bm_25

    def open_posting_file(self, term):
        if self.__current_posting_file_name != self.__dictionary_of_posting_pointers.get(term[0] , 'others'):
            self.__current_posting_file_name = self.__dictionary_of_posting_pointers.get(term[0] , 'others')
            with open(self.indexPath + '\\' + str(self.__current_posting_file_name) + self.stem_suffix, 'rb') as file:
                self.__currentPostingFile = pickle.load(file)
                file.close()

    def fill_mini_posting_file(self, list_of_terms):
        for term in list_of_terms:
            if term not in self.main_dictionary:
                print(term + " not found in dictionary !!!")
                continue  # no coalculation is needed because the term not exists in corpus
            else:
                if term not in self.mini_posting:
                    self.open_posting_file(term)
                    self.mini_posting[term] = self.__currentPostingFile[term]

    def get_top_50(self, query):
        counter = 0
        tmp_dic = {}
        for doc in self.final_result[query]:
            if counter == 50:
                break
            counter += 1
            tmp_dic[doc] = self.final_result[query][doc]
        return tmp_dic






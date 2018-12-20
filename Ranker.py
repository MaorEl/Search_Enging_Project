


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

    __current_posting_file_name = ''
    __currentPostingFile = None
    __term_grades_in_doc = {} # { term : {doc:grade}}
    __mini_posting = {}
    #todo: add to documentation- memoization of terms grades

    def __init__(self, docs_dictionary, main_dictionary, avdl, N, stem_suffix, indexPath):
        self.weight_bm_25 = 1 #todo: check if we need to add weight and another calculation for similarity
        self.b=0.75
        self.k=2
        self.avdl = avdl
        self.N = N
        self.main_dictionary = main_dictionary
        self.docs_dictionary = docs_dictionary
        self.result_bm_25={} # { query : { docNo: final_grade } }
        self.stem_suffix = stem_suffix # "_stem"
        self.indexPath = indexPath
        self.final_result = None

    def calc_bm_25(self, term_tf_dict, query_id):
        '''
        calculate the grades of all docs of one query in dict.
        update result dictionary for all terms in query
        :param { term : tf_in_query } sorted by term
        '''
        self.result_bm_25[query_id] = {}
        for term in term_tf_dict: # of one query
            if term not in self.__term_grades_in_doc:
                self.__term_grades_in_doc[term] = {}
                if term not in self.main_dictionary:
                    print (term + " not found in dictionary !!!")
                    continue #no coalculation is needed because the term not exists in corpus
                else:
                    mone = self.N + 0.5 - self.main_dictionary[term].get_df()
                    mechane = 0.5 + self.main_dictionary[term].get_df()
                    idf = log2(mone / mechane)

                    self.__currentPostingFile = self.__mini_posting[term]

                    for doc in self.__currentPostingFile:  # for each doc that includes this term
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
                    self.result_bm_25[query_id][doc] += self.__term_grades_in_doc[term][doc] * term_tf_dict[term]  # final grade for doc by query\
        sorted_dic = collections.OrderedDict(sorted(self.result_bm_25[query_id].items(), key=lambda x: x[1], reverse=True))
        return sorted_dic

    def rank(self, query_dict):
        self.result_bm_25 = {}
        query_term_tf_dict = invertDictionaryForQueries(query_dict) # dict of {Query: { Term: tf_ in query}
        start = time.time()
        for query in query_term_tf_dict:
            #sorted_dict = collections.OrderedDict(sorted(query_term_tf_dict[query].items(), key = lambda v: v[0].upper()))
            self.result_bm_25[query] = self.calc_bm_25(query_term_tf_dict[query], query)
        print ("calculation: " + str(time.time() - start))
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
                #todo: we may need to add the missing term into the mini posting
            else:
                if term not in self.__mini_posting:
                    self.open_posting_file(term)
                    self.__mini_posting[term] = self.__currentPostingFile[term]







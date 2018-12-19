


# helper function for parse result of queries file
import collections
import pickle
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
    #todo: add to documentation- memoization of terms grades

    def __init__(self, docs_dictionary, main_dictionary, avdl, N, stem_suffix, indexPath):
        self.weight_bm_25 = 1
        self.b=0.75
        self.k=2
        self.avdl = avdl
        self.N = N
        self.main_dictionary = main_dictionary
        self.docs_dictionary = docs_dictionary
        self.result={} # { query : { docNo: final_grade } }
        self.term_bm_grade_dict = {}
        self.stem_suffix = stem_suffix # "_stem"
        self.indexPath = indexPath


    def calc_bm_25(self, term_tf_dict, query_id):
        '''
        calculate the grades of all docs of one query in dict
        :param { term : tf_in_query } sorted by term
        :return: { docNo : Grade }
        '''
        for term in term_tf_dict:
            mone = self.N + 0.5 - self.main_dictionary[term].get_df()
            mechane = 0.5 + self.main_dictionary[term].get_df()
            idf = mone / mechane

            #need to open posting file
            self.open_posting_file(term)
            for doc in self.__currentPostingFile[term]:
                if doc not in self.__term_grades_in_doc[term]:
                    tf_in_doc = self.__currentPostingFile[term][doc]
                    doc_len = self.docs_dictionary[doc].number_of_words

                    mone = tf_in_doc * (self.k + 1)
                    mechane = tf_in_doc + self.k * (1 - self.b + self.b * (doc_len/self.avdl))
                    okapi = mone / mechane
                    self.__term_grades_in_doc[term] = {doc : okapi * idf} #memoization of term in doc
                else:
                    if query_id not in self.result:
                        self.result[query_id] = {doc : self.__term_grades_in_doc[term][doc] * term_tf_dict[term]}
                    else: # query inside but not sure about doc
                        if doc not in self.result[query_id]:
                            self.result[query_id][doc] = self.__term_grades_in_doc[term][doc] * term_tf_dict[term]
                        else: #doc inside

                if query_id not in self.result:
                    self.result[query_id] = self.__term_grades_in_doc[term] * term_tf_dict[term]

                elif :
                    self.result[query_id][doc] += self.__term_grades_in_doc[term][doc]



        return

    def rank(self, query_dict):
        query_term_tf_dict = invertDictionaryForQueries(query_dict) # dict of {Query: { Term: tf_ in query}
        for query in query_term_tf_dict:
            self.result[query] = self.weight_bm_25 * self.calc_bm_25(collections.OrderedDict(sorted(query_term_tf_dict[query])), query)

    def open_posting_file(self, term):
        if self.__current_posting_file_name != self.__dictionary_of_posting_pointers[term[0]]:
            self.__current_posting_file_name = self.__dictionary_of_posting_pointers[term[0]]
            with open(self.indexPath + '\\' + str(self.__current_posting_file_name) + self.stem_suffix, 'rb') as file:
                self.__currentPostingFile = pickle.load(file)
                file.close()






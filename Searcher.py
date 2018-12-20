import time

from Ranker import Ranker


class Searcher:

    def __init__(self, docs_dictionary, main_dictionary, avdl, stem_suffix, ip):
        self.main_dictionary = main_dictionary
        self.__ranker = Ranker(docs_dictionary, main_dictionary, avdl, len(docs_dictionary), stem_suffix, ip)

     # will be trigger from controller
    def search(self, query_dict , addons_dict = None):
        '''
        searching docs that includes terms in query
        :param query_dict: {term : { query : tf } }
        :param addons_dict: {term : { query : tf } } - optional
        :return:
        '''
        query_dict = self.adjust_terms(query_dict)
        if addons_dict is not None:
            addons_dict = self.adjust_terms(addons_dict)
            all_terms = list(set(list(query_dict.keys()) + list(addons_dict.keys())))
            #all_terms = self.merge_all_terms_to_one_list(query_dict, addons_dict)
            self.__ranker.fill_mini_posting_file(sorted(all_terms, key=lambda v: v.upper()))
            ranked_titles = self.__ranker.rank(query_dict)
            self.__ranker.counter_for_doc = 0
            ranked_addons = self.__ranker.rank(addons_dict)
        else:
            start = time.time()
            self.__ranker.fill_mini_posting_file(sorted(query_dict.keys(), key=lambda v: v.upper()))
            ranked_files = self.__ranker.rank(query_dict)

    def adjust_terms(self, query_dict):
        '''

        :param query_dict: {term : { query : tf } }
        :return:
        '''
        result = {}
        for term in query_dict:
            if term not in self.main_dictionary:
                value = query_dict[term]
                if term.lower() in self.main_dictionary:
                    if term.lower() not in result:
                        result[term.lower()] = value
                    else:  # exists in result -> merge
                        result[term.lower()] = self.mergi_mergi(result[term.lower()], value)
                elif term.upper() in self.main_dictionary:
                    if term.upper() not in result:
                        result[term.upper()] = value
                    else: #exists in result -> merge
                        result[term.upper()] = self.mergi_mergi(result[term.upper()], value)
                else:
                    print (term + " not exists in main dic at all")
                    if term not in result:
                        result[term] = query_dict[term]
                    else:
                        result[term] = self.mergi_mergi(result[term], query_dict[term])
                    #not exists in the main dictionary
                    #todo: or semantic care or nothing
            else:
                if term not in result:
                    result[term] = query_dict[term]
                else:
                    result[term] = self.mergi_mergi(result[term], query_dict[term])
        return result

    def mergi_mergi(self, dic1, dic2):
        '''
        merge two dictionaries that looks like this: { Query:tf in query }
        :param dic1: first
        :param dic2: second
        :return: merged dictionary
        '''
        for q in dic1:
            if q in dic2:
                dic2[q] += dic1[q]
            else:
                dic2[q] = dic1[q]
        return dic2

    def merge_all_terms_to_one_list(self, query_dict, addons_dict):
        '''
        creates a list of merged terms
        :param query_dict: {term : { query : tf } }
        :param addons_dict: {term : { query : tf } }
        :return: list of terms
        '''
        result = []
        for term in query_dict:
            if term not in result:
                result.append(term)
        for term in addons_dict:
            if term not in result:
                result.append(term)
        return result

#todo : check for each term how it exists in main dictionary
























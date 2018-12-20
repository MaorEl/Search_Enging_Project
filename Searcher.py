import time

from Ranker import Ranker


class Searcher:

    def __init__(self, docs_dictionary, main_dictionary, avdl, stem_suffix, ip, city_dictionary):
        self.main_dictionary = main_dictionary
        self.__ranker = Ranker(docs_dictionary, main_dictionary, avdl, len(docs_dictionary), stem_suffix, ip)
        self.__list_of_cities = []
        self.__city_dictionary = city_dictionary

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
            if self.__list_of_cities is not None:
                self.remove_not_relevant_docs()
            ranked_titles = self.__ranker.rank(query_dict)
            self.__ranker.counter_for_doc = 0
            ranked_addons = self.__ranker.rank(addons_dict)
            final = self.__ranker.calculate_final_rank(ranked_titles, ranked_addons)
        else:
            self.__ranker.fill_mini_posting_file(sorted(query_dict.keys(), key=lambda v: v.upper()))
            if self.__list_of_cities is not None:
                self.remove_not_relevant_docs()
            ranked_files = self.__ranker.rank(query_dict)
            self.__ranker.final_result = ranked_files
            self.__ranker.final_result["1"] = self.__ranker.get_top_50("1")

    def set_cities_filter_list(self, list):
        self.__list_of_cities = list

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

    def remove_not_relevant_docs(self):
        start = time.time()
        #posting_file = self.__ranker.mini_posting
        city_docs = []
        for city_name in self.__list_of_cities:
            city_docs = list(set(list(self.__city_dictionary[city_name].dic_doc_index.keys()) + city_docs))
        city_docs = {key : None for key in city_docs}
        self.__ranker.city_docs = city_docs
        # print("merge: " + str(time.time() - start))
        # new_temp_posting = {}
        # start = time.time()
        # for term in posting_file:
        #     new_temp_posting[term] = {}
        #     for doc in posting_file[term]:
        #         if doc in city_docs:
        #             new_temp_posting[term][doc] = posting_file[term][doc]
        # self.__ranker.mini_posting = new_temp_posting
        # print("remove: " + str(time.time() - start))


























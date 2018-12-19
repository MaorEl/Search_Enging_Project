from Ranker import Ranker


class Searcher:

    def __init__(self, docs_dictionary, main_dictionary, avdl, stem_suffix, ip):
        self.__ranker = Ranker(docs_dictionary, main_dictionary, avdl, len(docs_dictionary), stem_suffix, ip)

     # will be trigger from controller
    def search(self, query_dict , addons_dict = None):
        ranked_files = self.__ranker.rank(query_dict)


#todo : check for each term how it exists in main dictionary
























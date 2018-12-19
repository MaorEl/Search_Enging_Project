
class Ranker:

    def __init__(self):
        self.b=0.75
        self.k=2

    # for one query calc bm25 for all documents
    def calc_bm_25(self, query_dict, document_dict):
        for doc, docInfo in document_dict:



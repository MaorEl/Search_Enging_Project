import os
import concurrent.futures
import pathlib
import re
import time

from NewTry.Document import Document

docs_dictionary = {} #Doc Number will be the key. value is a Document
corpus_path = ''
dic_to_parse = {}


def cleanTextOfFile():
    # TODO: to be implemented . clean all of the shitty tags and infromatiob
    pass

class ReadOneFile:
    current_doc =""
    current_DOCNO=""
    current_CITY =""
    current_DATE=""

    def __extractDOCNO(self):
        self.current_DOCNO = (self.current_doc.split("</DOCNO>", 1)[0]).split("<DOCNO>")[1].strip()
        #print (self.current_DOCNO)

    def __extractCITY(self):
        if "<F P=104>" in self.current_doc:
            self.current_CITY = self.current_doc.split("<F P=104>")[1].split()[0]

    def __extractDATE(self):
        if "<DATE1>" in self.current_doc:
            self.current_DATE = (self.current_doc.split("</DATE1>", 1)[0]).split("<DATE1>")[1].strip()
        elif "<DATE>" in self.current_doc:
            self.current_DATE = (self.current_doc.split("</DATE>", 1)[0]).split("<DATE>")[1].strip()

    def __extractTEXT(self):
        text = (self.current_doc.split("</TEXT>", 1)[0]).split("<TEXT>")[1].strip()
        dic_to_parse[self.current_DOCNO] = text


    def takeDocsInfoFromOneFile(self,path):
        file = open(path, 'r')
        text_of_file = "".join(file.readlines())
        list_of_docs = text_of_file.split('</DOC>')
        del list_of_docs[-1] #not necessary

        for doc in list_of_docs:
            self.current_doc = doc
            self.__extractDOCNO()
            self.__extractCITY()
            self.__extractDATE()
            self.__extractTEXT()
            docs_dictionary[self.current_DOCNO] = Document(self.current_DATE, self.current_CITY, str(path))


'''
def countdocno():
    count=0
    for root, dirs, files in os.walk(path):
        for file in files:
            with open(str(pathlib.PurePath(root, file))) as f:
                for line in f:
                    count += line.count("<DOCNO>")
    return count
'''


class SendToParser(object):
    #TODO: clean the dictionary and send original dictionary to parser
    pass


def Main():
    path = 'C:\Retrieval_folder\corpus'
    # ReadOneFile.readFile(path)
    start = time.time()
    global corpus_path
    corpus_path = path
    # executor = concurrent.futures.ThreadPoolExecutor(1)
    for root, dirs, files in os.walk(corpus_path):
        for file in files:
            oneFile = ReadOneFile()
            oneFile.takeDocsInfoFromOneFile(str(pathlib.PurePath(root, file)))
            cleanTextOfFile()
            SendToParser()
    end = time.time()
    print(end-start)
    dic = docs_dictionary
    print(dic.__len__()) #472525

Main()




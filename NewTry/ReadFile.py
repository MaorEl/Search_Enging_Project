import os
import concurrent.futures
import pathlib
import re


docs_dictionary = {} #Doc Number will be the key. value is a Document
corpus_path = ''
regDOC = '<DOC> (.*?) </DOC>'
regDOCNO = '<DOCNO> (.*?) </DOCNO>'


def readFile(path):
    global corpus_path
    corpus_path = path
    executor = concurrent.futures.ThreadPoolExecutor(1)
    for root, dirs, files in os.walk(corpus_path):
        for file in files:
            executor.submit(takeDocsInfoFromOneFile,pathlib.PurePath(root, file))


def cleanText(text_of_doc):
    #TODO: to be implemented . clean all of the shitty tags and infromatiob
    pass


def takeDocsInfoFromOneFile(path):
    file = open(path, 'r')
    text_of_file = "".join(file.readlines())
    list_of_docs = re.split('\n<DOC>\n|\n</DOC>\n',text_of_file)

    print("mm")

    for doc in list_of_docs:
        docNumber = (doc.split("</DOCNO>", 1)[0]).split("<DOCNO>")[1].strip()
        docs_dictionary[docNumber] = path
        text_of_doc = (doc.split("</TEXT>", 1)[0]).split("<TEXT>")[1].strip()
        cleanedText = cleanText(text_of_doc)
        #TODO: send the text to Parser with doc number or any identifictaion


path='C:\Retrieval_folder\corpus'
readFile(path)

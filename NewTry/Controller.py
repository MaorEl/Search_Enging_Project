import json
import os
import pathlib
import pickle
import time
import collections
from fractions import Fraction

from NewTry import ReadFile
from NewTry import Parser
from NewTry import Indexer
from NewTry.Indexer import merge_dictionaries
from NewTry.Indexer import main_dictionary
from NewTry.ReadFile import dic_to_parse
from NewTry import PorterStemmer

#stemmer = PorterStemmer.PorterStemmer()


def SendToParser(file):
    return Parser.parse(dic_to_parse, file)


def data_set_Path(path):
    global __stopwords_path
    __stopwords_path = path+"/stop_words.txt"
    Parser.set_stop_words_file(__stopwords_path)


def getStemmerFromUser(flag):

    #TODO: implements this from user GUI
    return flag

#
# def stem_dictionary(dictionary_of_one_file,stemmer):
#     for doc in dictionary_of_one_file:
#         new_dic_of_one_doc = {}
#         for term, freqInDoc in dictionary_of_one_file[doc].items():
#             stemmed_term = stemmer.stem(term.lower())
#             #if (stemmed_term!=term): #if the stem has changed the term
#             if term.isupper():
#                 stemmed_term = stemmed_term.upper()
#             if stemmed_term in new_dic_of_one_doc: #if the stemmed term is already on this dictionary
#                 new_dic_of_one_doc[stemmed_term] += freqInDoc
#             else:
#                 new_dic_of_one_doc[stemmed_term] = freqInDoc
#         dictionary_of_one_file[doc]=new_dic_of_one_doc
#     return dictionary_of_one_file
#
def contains_digit(term):
    return any(char.isdigit() for char in term)

def Main():
    global main_dictionary
    global stemmer
    path = 'C:\Retrieval_folder\\full_corpus'
    #path = 'C:\Retrieval_folder\\full_corpus'
    start = time.time()
    corpus_path = path
    data_set_Path(path)
    counter = 0
    start2 = time.time()
    for root, dirs, files in os.walk(corpus_path):
        for file in files:

            if str(file) != 'stop_words.txt':
                #start = time.time()
                ReadFile.takeDocsInfoFromOneFile(str(pathlib.PurePath(root, file)))
                dictionary_of_one_file = SendToParser(file)
                s = collections.OrderedDict(sorted(dictionary_of_one_file.items()))
                #merge_dictionaries(s)
                #main = main_dictionary
                dic_to_parse.clear()
                #end = time.time()
                #print (end-start)
    #saveDictionaryToDisk()
    end2 = time.time();
    print((end2 - start2) / 60)


Main()


def debug_parser(corpus_path):
    for root, dirs, files in os.walk(corpus_path):
        for file in files:
            if str(file) != 'stop_words.txt':
                start = time.time()
                ReadFile.takeDocsInfoFromOneFile(str(pathlib.PurePath(root, file)))
                dictionary_of_one_file = SendToParser(file)
                dic_to_parse.clear()

def debug_dictionary_creation(dicionary):
    pass

def debug_indexer_flow(dixtionary):
    pass


























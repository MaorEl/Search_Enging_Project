import json
import os
import pathlib
import pickle
import time
import collections
from fractions import Fraction

from NewTry import ReadFile, tmp_parser
from NewTry import Parser
from NewTry import Indexer
from NewTry.Indexer import merge_dictionaries
from NewTry.Indexer import main_dictionary
from NewTry.ReadFile import dic_to_parse
from NewTry import PorterStemmer
from NewTry.Parser import stem



def SendToParser(file):
    return Parser.parse(dic_to_parse)


def data_set_Path(path):
    global __stopwords_path
    __stopwords_path = path+"/stop_words.txt"
    Parser.set_stop_words_file(__stopwords_path)


def getStemmerFromUser():

    #TODO: implements this from user GUI
    return True

def contains_digit(term):
    return any(char.isdigit() for char in term)

def Main():
    global stem
    Parser.stem = getStemmerFromUser()
    #path = 'C:\Retrieval_folder\corpus'
    path = 'C:\Retrieval_folder\\full_corpus'
    start = time.time()
    corpus_path = path
    data_set_Path(path)
    counter = 0
    start2 = time.time()
    for root, dirs, files in os.walk(corpus_path):
        for file in files:
            end2 = time.time()
            if ((end2-start2)/60)>10 and ((end2-start2)/60) <10.10:
                print(str(file))
            #print((end2 - start2) / 60)
            if str(file) != 'stop_words.txt':
                #start = time.time()
                ReadFile.takeDocsInfoFromOneFile(str(pathlib.PurePath(root, file)))
                dic_of_one_file = SendToParser(file)
                dic_to_parse.clear()
                #end = time.time()
                #print (end-start)
    #saveDictionaryToDisk()
    end2 = time.time()
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


























import os
import pathlib
import pickle
import time
import collections

import ReadFile
import Parser
import Indexer
from ReadFile import dic_to_parse
from City import create_city_db,city_db

__corpus_path = ""
__index_path = ""

def SendToParser():
    return Parser.parse(dic_to_parse)


def data_set_Path(corpus_path, index_path):
    global __stopwords_path
    global __corpus_path
    global __index_path
    __stopwords_path = corpus_path + "\\stop_words.txt"
    Parser.set_stop_words_file(__stopwords_path)
    __corpus_path = corpus_path
    __index_path = index_path
    Indexer.set_path_to_postiong_files(__index_path)


def getStemmerFromUser():

    #TODO: implements this from user GUI
    return True


def Main(cp, ip, to_stem):
    global __corpus_path
    global __index_path
    global doc
    create_city_db()
    Parser.stem = getStemmerFromUser() #todo: change to_stem and remove the function
    #cp = 'C:\Retrieval_folder\corpus' #todo: to delete
    ip = 'C:\Retrieval_folder\\index' #todo: to delete
    cp = 'C:\Retrieval_folder\\full_corpus'
    ip = 'D:\documents\\users\\anaelgor\Downloads\corpus\index'  # todo: to delete
    cp = 'd:\documents\\users\\anaelgor\Downloads\corpus\corpus'
    start = time.time()
    data_set_Path(cp, ip)
    Indexer.create_posting_files()
    counter=0
    for root, dirs, files in os.walk(__corpus_path):
        for file in files:
            end2 = time.time()
            if ((end2-start)/60)>10 and ((end2-start)/60) <10.10:
                print(str(file))
            if str(file) != 'stop_words.txt':
                ReadFile.takeDocsInfoFromOneFile(str(pathlib.PurePath(root, file)))
                dic_of_one_file = SendToParser()
                sorted_dictionary = collections.OrderedDict(sorted(dic_of_one_file.items())) #todo: check this on lab
                index_start = time.time()
                Indexer.merge_dictionaries(sorted_dictionary)
                dic_to_parse.clear()
                docs_dic = ReadFile.docs_dictionary
                counter += 1
            if counter == 100:
                Indexer.SaveAndMergePostings()
                counter = 0
    Indexer.SaveAndMergePostings()
    end2 = time.time()
    print((end2 - start) / 60)


Main("","",True)

























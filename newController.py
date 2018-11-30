import os
import pathlib
import pickle
import time
import collections

import ReadFile
import Parser
import newIndexer
from ReadFile import dic_to_parse

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
    newIndexer.set_path_to_postiong_files(__index_path)


def getStemmerFromUser():

    #TODO: implements this from user GUI
    return True

def contains_digit(term):
    return any(char.isdigit() for char in term)


def Main(cp, ip, to_stem):
    global __corpus_path
    global __index_path
    global doc
    Parser.stem = getStemmerFromUser() #todo: change to_stem and remove the function
    #cp = 'C:\Retrieval_folder\corpus' #todo: to delete
    ip = 'C:\Retrieval_folder\\index' #todo: to delete
    cp = 'C:\Retrieval_folder\\full_corpus'
    start = time.time()

    data_set_Path(cp, ip)
    #Indexer.create_empty_posting_files()
    # counter=0
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
                newIndexer.merge_dictionaries(sorted_dictionary)
                # index_end = time.time()
                # print("indexer time for file: " +str(counter) + " " +  str(index_end-index_start))
                # counter+=1
                dic_to_parse.clear()
                docs_dic = ReadFile.docs_dictionary
                x=5
    newIndexer.create_posting_files()
    with open('C:\Retrieval_folder\\index\docs_dic', 'wb') as file:
        pickle.dump(docs_dic, file)
        file.close()
    end2 = time.time()
    print((end2 - start) / 60)


Main("","",True)

























import os
import pathlib
import pickle
import shutil
import time
import collections

import ReadFile
import Parser
import Indexer
import ReadQuery
from ReadFile import dic_to_parse
from City import create_city_db,city_db
import GUI

stop = False
__corpus_path = ""
__index_path = ""
__stem_suffix = ''

def data_set_Path(corpus_path, index_path):
    global __stopwords_path
    global __corpus_path
    global __index_path
    __stopwords_path = corpus_path + "\\stop_words.txt"
    Parser.set_stop_words_file(__stopwords_path)
    __corpus_path = corpus_path
    __index_path = index_path
    Indexer.set_path_to_postiong_files(__index_path)

def saveCityDictionaryToDisk(ip):
    global __stem_suffix
    with open(ip + '\cities' + __stem_suffix, 'wb') as file:
        pickle.dump(ReadFile.city_dictionary, file)
        file.close()

def saveLangListToDisk(ip):
    global __stem_suffix
    with open(ip + '\languages' + __stem_suffix, 'wb') as file:
        pickle.dump(ReadFile.lang_list, file)
        file.close()



def saveMainDictionaryToDisk(ip):
    global __stem_suffix
    with open(ip + '\main_dictionary' + __stem_suffix, 'wb') as file:
        pickle.dump(Indexer.main_dictionary, file)
        file.close()


def saveDocumentDictionaryToDisk(ip):
    global __stem_suffix
    with open(ip + '\docs_dictionary' + __stem_suffix, 'wb') as file:
        pickle.dump(ReadFile.docs_dictionary, file)
        file.close()


def Main(cp, ip, to_stem):
    global __corpus_path
    global __index_path
    global doc
    global __stem_suffix
    create_city_db()
    Parser.stem = to_stem
    if to_stem is True:
        __stem_suffix = '_stem'

    start = time.time()
    data_set_Path(cp, ip)
    Indexer.create_posting_files(__stem_suffix)
    counter = 0
    for root, dirs, files in os.walk(__corpus_path):
        for file in files:
            if (stop==True):
                reset() #will clear the memory of the program %% will remove the posting files and dictionary
                return
            #print("file!!!")
            end2 = time.time()
            # if ((end2-start)/60)>10 and ((end2-start)/60) <10.10:
            #     print(str(file))
            if str(file) != 'stop_words.txt':
                ReadFile.takeDocsInfoFromOneFile(str(pathlib.PurePath(root, file)))
                dic_of_one_file = Parser.parse(dic_to_parse)
                sorted_dictionary = collections.OrderedDict(sorted(dic_of_one_file.items()))
                index_start = time.time()
                Indexer.merge_dictionaries(sorted_dictionary)
                dic_to_parse.clear()
                counter += 1
            if counter == 100:
                Indexer.SaveAndMergePostings()
                counter = 0
    Indexer.SaveAndMergePostings()
    saveCityDictionaryToDisk(ip)
    saveMainDictionaryToDisk(ip)
    saveDocumentDictionaryToDisk(ip)
    saveLangListToDisk(ip)
    x=ReadFile.lang_list
    end2 = time.time()
    time_final = str((end2 - start) / 60)
    print("time of program: " + time_final)
    sendInfoToGUI(time_final)



def remove_index_files():
    global __index_path
    if os.path.exists(__index_path):
        for root, dirs, files in os.walk(__index_path):
            for file in files:
                os.remove(os.path.join(root, file))

def reset():
    global __corpus_path,__index_path, __stem_suffix
    ReadFile.reset()
    Parser.reset()
    Indexer.reset()
    remove_index_files()
    __stem_suffix = ''
    __corpus_path = ""
    __index_path = ""

#this function will update the boolean of stopping, so the program will stop safely
def reset_from_GUI():
    global stop
    stop = True

def loadDictionaryFromDisk(to_stem, ip):
    global __index_path, __stem_suffix
    __index_path = ip
    if to_stem == True:
        __stem_suffix = '_stem'
    main_dic_path = __index_path +  '/' + 'main_dictionary' + __stem_suffix
    with open(main_dic_path, 'rb') as file:
        Indexer.main_dictionary = pickle.load(file)
        file.close()


def getMainDictionaryFromIndexerToGUI():
    return Indexer.main_dictionary

def sendInfoToGUI(time):
    num_docs = len(ReadFile.docs_dictionary)
    num_terms = len(Indexer.main_dictionary)
    GUI.show_information_about_indexing(num_docs,num_terms,time)


#for GUI
def getLangList():
    return ReadFile.lang_list


#helper function for parse result of queries file
def invertDictionaryForQueries(dict):
    result = {}
    for term in dict:
        for query in dict[term]:
            if query not in result:
                query_dict={}
                query_dict[term]= dict[term][query]
                result[query]=query_dict
            else: #for case query is not exists yet on dictionary
                result[query][term]=dict[term][query]
    return result

def controlQueriesOfFreeText(text):
    dictionary_of_queries = ReadQuery.create_dictionary_from_free_text_query(text)
    dic_after_parse = invertDictionaryForQueries(Parser.parse(dictionary_of_queries))


def controlQueriesOfFile(path):
    dictionary_of_queries_by_title, dictionary_of_queries_by_addons = ReadQuery.create_dictionary_of_file(path)
    dic_after_parse_by_title = invertDictionaryForQueries(Parser.parse(dictionary_of_queries_by_title))
    dic_after_parse_by_addons = invertDictionaryForQueries(Parser.parse(dictionary_of_queries_by_addons))
    print(8)

#todo: call this from GUI before the functions above
def setStemForPartB(to_stem):
    global __stem_suffix
    Parser.stem = to_stem
    if to_stem is True:
        __stem_suffix = '_stem'

controlQueriesOfFile("C:\Retrieval_folder\queries.txt")
#todo: we are not must to desc and narrative - so let se if it does not make too much problem we'll edit this
#todo: check if term is exists or not on main dictionary (lower upper case - need to decide when and how)
#todo: check which data we need to take for Ranker & Searcher and then we will keep it on {term: {DocNo: x } }


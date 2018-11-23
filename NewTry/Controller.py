import os
import pathlib
import time
from fractions import Fraction

from NewTry import ReadFile
from NewTry import Parser
from NewTry.ReadFile import dic_to_parse



def SendToParser(file):
    one_file_dic = Parser.parse(dic_to_parse, file)
    pass


def data_set_Path(path):
    global __stopwords_path
    __stopwords_path = path+"/stop_words.txt"
    Parser.set_stop_words_file(__stopwords_path)


def Main():
    path = 'C:\Retrieval_folder\corpus'
    start = time.time()
    global corpus_path
    corpus_path = path
    data_set_Path(path)
    #counter = 0
    start2 = time.time()

    for root, dirs, files in os.walk(corpus_path):
        for file in files:

            if str(file) != 'stop_words.txt':
                ReadFile.takeDocsInfoFromOneFile(str(pathlib.PurePath(root, file)))
                SendToParser(file)
                dic_to_parse.clear()
                #counter = counter + 1

    #saveDictionaryToDisk()
    end2 = time.time();
    print((end2 - start2) / 60)






Main()
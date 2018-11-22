import os
import pathlib
import time
from NewTry import ReadFile
from NewTry import Parser
from NewTry.ReadFile import dic_to_parse


def SendToParser(file):
    #TODO: send original dictionary to parser
    one_file_dic = Parser.parse(dic_to_parse, file)
    pass

def Main():
    path = 'C:\Retrieval_folder\corpus'
    start = time.time()
    global corpus_path
    corpus_path = path
    for root, dirs, files in os.walk(corpus_path):
        for file in files:
            ReadFile.takeDocsInfoFromOneFile(str(pathlib.PurePath(root, file)))
            SendToParser(file)
            dic_to_parse.clear()

    docdoc = dic_to_parse
    #saveDictionaryToDisk()
    end = time.time()
    print(end-start)

Main()
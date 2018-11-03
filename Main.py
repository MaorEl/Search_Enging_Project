import os
import pathlib
import time
import readJson
import ReadFile
import json
import requests
import string

rootdir = "C:\Retrieval_folder\corpus"



from pprint import pprint


def main():
    start = time.time()
    rf = readJson.ReadJson(rootdir)
    rf.create_maagar_meida()
    end = time.time()

    print (end-start)


    path=rootdir + "\\allDocs"
    file = open (path,'r')
    lines = file.readlines()
    file.close()
    for line in lines:
        print (line)
        data = json.loads(line)
    print ("c")


main()

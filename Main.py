import os
import pathlib
import time

import ReadFile

rootdir = "C:\Retrieval_folder\corpus"



def main():
    start = time.time()
    rf = ReadFile.ReadFile(rootdir)
    rf.create_maagar_meida()
    end = time.time()

    print (end-start)


main()

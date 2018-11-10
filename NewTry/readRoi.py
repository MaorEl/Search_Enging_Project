import concurrent.futures
import datetime
import os
import pathlib
import pickle
import time

from NewTry import Document

__months_dictionary = {'january': '01', 'jan': '01', 'february': '02', 'feb': '02', 'march': '03', 'mar': '03',
                       'april': '04', 'apr': '04', 'may': '05', 'june': '06', 'jun': '06', 'july': '07',
                       'jul': '07',
                       'august': '08', 'aug': '08', 'september': '09', 'sep': '09', 'october': '10', 'oct': '10',
                       'november': '11', 'nov': '11', 'december': '12', 'dec': '12'}

path = ""  # The path to the file
docNumList = []  # A list of all doc nums in the file
docCityList = []  # A list of all doc city in the file
docDateList = []  # A list of all doc date of publication
textList = []  # A list of all the texts in a file
textDic = {}  # A dictionary that key is doc number and value is the text
docDictionary = {}  # A dictionary for all document in corpus
length = 0  # The number of documents in the current file (length of docNumList)
fileName = ""  # The file name of the documents. Used for part 2 of the assignment
index = 0

def split_doc(path_corpus="", sub_dir=""):
    global path
    global docNumList
    global docCityList
    global textList
    global textDic
    global docDictionary
    global length
    global fileName
    global index

    path = path_corpus
    dir = sub_dir
    for root, dirs, files in os.walk(path + "/" +dir):  # traverses the given file path.
        fileName = path + "/" + dir + "/" + files[0]
        text_file = open(os.path.join(path + "/" +dir, files[0]), 'r', encoding="ISO-8859-1")  # The encoding of text files.
        textList = text_file.read().split("</TEXT>")  # Split at </TEXT> tag.
        text_file.close()
        del textList[-1]  # The last object in the list is the garbage past the final </TEXT> tag.
        length = len(textList)
        index = len(textDic)
        idx_create = len(textDic)
        __takeDocNum()
        __takeDocCity()
        __takeDocDate()
        __takeText()
        __createDocDictionary(idx_create)

# Extract the docNum from a whole Document
def __takeDocNum():
    global length
    global textList
    global docNumList

    for i in range(length):
        docNum = (textList[i].split("</DOCNO>", 1)[0]).split("<DOCNO>")[1].strip()
        docNumList.append(docNum)


# Extract the doc city from a whole Document
def __takeDocCity():
    global length
    global textList
    global docCityList

    for i in range(length):
        if "<F P=104>" in textList[i]:
            docCity = textList[i].split("</F>")[0]
            docCity = textList[i].split("<F P=104>")[1].split()
            docCityList.append(docCity[0].upper())
        else:
            docCityList.append("")


# Extract the docDate from a whole Document
def __takeDocDate():
    global length
    global textList
    global docDateList

    for i in range(length):
        if "<DATE1>" in textList[i]:
            docDate = textList[i].split("</DATE1>")[0]
            docDate = textList[i].split("<DATE1>")[1].split()
            if docDate[0].lower() in __months_dictionary:
                months = __months_dictionary[docDate[0].lower()]
                day = docDate[1]
                year = docDate[2]
                if year[len(year) - 1] == '*':
                    year = year[:-1]
                if not year.isnumeric():
                    year = ""
                if year.isnumeric() and 0 < int(year) < 100:
                    year = "19" + year
                if len(day) == 1:
                    day = "0" + day
                if year == "":
                    docDateList.append(months + "-" + day)
                else:
                    docDateList.append(year + "-" + months + "-" + day)
            elif docDate[1].lower() in __months_dictionary:
                months = __months_dictionary[docDate[1].lower()]
                day = docDate[0]
                year = docDate[2]
                if year[len(year)-1] == '*':
                    year = year[:-1]
                if not year.isnumeric():
                    year=""
                if year.isnumeric() and 0 < int(year) < 100:
                    year = "19" + year
                if len(day) == 1:
                    day = "0" + day
                if year == "":
                    docDateList.append(months+"-"+day)
                else:
                    docDateList.append(year + "-" + months + "-" + day)
            elif docDate[0] == "000" and docDate[1] == "000":
                year = docDate[2]
                if year[len(year)-1] == '*':
                    year = year[:-1]
                if not year.isnumeric():
                    year=""
                if year.isnumeric() and 0 < int(year) < 100:
                    year = "19" + year
                docDateList.append(year)

        elif "<DATE>" in textList[i]:
            docDate = textList[i].split("</DATE>")[0]
            docDate = textList[i].split("<DATE>")[1].split()
            if docDate[0].isnumeric() and len(docDate[0]) == 6:
                day = docDate[0][4:]
                months = docDate[0][2:4]
                year = docDate[0][:-4]
                year = "19" + year
                docDateList.append(year + "-" + months + "-" + day)
            if not len(docDate[0]) == 6:
                idx = 1
                while not docDate[idx].lower() in __months_dictionary:
                    idx += 1
                months = __months_dictionary[docDate[idx].lower()]
                day = docDate[idx+1]
                if ',' in day:
                    day = docDate[idx+1][:-1]
                year = docDate[idx+2]
                if ',' in year:
                    year = docDate[idx+2][:-1]
                if 0 < int(year) < 100:
                    year = "19" + year
                if len(day) == 1:
                    day = "0" + day
                docDateList.append(year + "-" + months + "-" + day)

        else:
            docDateList.append("")


# Extract the clean text
def __takeText():
    global length
    global textList
    global textDic
    global index

    for i in range(length):
        text = textList[i].split("<TEXT>")[1].strip()
        # remove problematic or meaningless strings that clutter the corpus
        #text = text.replace('\n', " ")
        #text = text.replace('CELLRULE', " ")
        #text = text.replace('TABLECELL', " ")
        #text = text.replace('CVJ="C"', " ")
        #text = text.replace('CHJ="C"', " ")
        #text = text.replace('CHJ="R"', " ")
        #text = text.replace('CHJ="L"', " ")
        #text = text.replace('TABLEROW', " ")
        #text = text.replace('ROWRULE', " ")
        #text = text.replace('>', " ")
        #text = text.replace('<', " ")
        text = ' '.join(text.split())
        textDic[docNumList[index]] = text
        index += 1


# creates the dictionary to be returned
def __createDocDictionary(idx):
    global length
    global docNumList
    global docCityList
    global docDictionary
    global textList
    global fileName

    length = len(docNumList)
    while idx < length:
        docDictionary[docNumList[idx]] = Document.Document(docDateList[idx],docCityList[idx], fileName)
        idx += 1

# Delete Reader's data structures
def __reset():
    global docNumList
    global docCityList
    global docDateList
    global textList
    global fileName
    global length
    global textDic
    global docDictionary
    global index

    docNumList = []
    docCityList = []
    docDateList = []
    textList = []
    textDic = {}
    docDictionary = {}
    length = 0
    index = 0
    fileName = ""


def read_doc(doc_num, file_path):
    global docNumList
    global textList
    global docDictionary
    global length

    text_file = open(os.path.join(file_path), 'r', encoding="ISO-8859-1")
    textList = text_file.read().split("</TEXT>")  # Split at </TEXT> tag.
    text_file.close()
    del textList[-1]  # The last object in the list is the garbage past the final </TEXT> tag.

    length = len(textList)
    __takeDocNum()
    __takeText()

    text = ""
    for i in range(length):
        if docNumList[i] == doc_num:
            text = textList[i]
            break
    return text

def Main():
    path = 'C:\Retrieval_folder\corpus\corpus'
    start = time.time()
    global corpus_path
    corpus_path = path
    #executor = concurrent.futures.ThreadPoolExecutor(8)
    for root, dirs, files in os.walk(corpus_path):
        for dir in dirs:
            #executor.submit(split_doc, path,str(dir))
            split_doc(path,str(dir))
    end = time.time()
    print (end-start)
    print (docDictionary.__len__()) #468370
            # executor.submit(takeDocsInfoFromOneFile,pathlib.PurePath(root, file))
    # parse()
Main()






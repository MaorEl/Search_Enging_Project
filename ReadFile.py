from City import City
from DocumentInfo import DocumentInfo

docs_dictionary = {} #Doc Number will be the key. value is a Document
corpus_path = ''
dic_to_parse = {}
city_dictionary = {}


current_doc =""
current_DOCNO=""
current_CITY =""
current_DATE=""

def __extractDOCNO():
    global current_DOCNO
    current_DOCNO = (current_doc.split("</DOCNO>", 1)[0]).split("<DOCNO>")[1].strip()

def __extractCITY():
    global  current_CITY, current_DOCNO
    global city_dictionary
    if "<F P=104>" in current_doc:
        current_CITY = current_doc.split("<F P=104>")[1].split()[0]
        if current_CITY != '</F>':
            if current_CITY not in city_dictionary:
                city_dictionary[current_CITY] = City(current_CITY,current_DOCNO)
            else:
                city_object = {current_DOCNO : ['TAG']}
                city_dictionary[current_CITY].dic_doc_index.update(city_object)

def __extractDATE():
    global current_DATE
    if "<DATE1>" in current_doc:
        current_DATE = (current_doc.split("</DATE1>", 1)[0]).split("<DATE1>")[1].strip()
    elif "<DATE>" in current_doc:
        current_DATE = (current_doc.split("</DATE>", 1)[0]).split("<DATE>")[1].strip()

def __extractTEXT():
    global  current_doc
    if "</TEXT>" in current_doc:
        text = (current_doc.split("</TEXT>", 1)[0]).split("<TEXT>")[1].strip()
    else:
        text = ""
    dic_to_parse[current_DOCNO] = text


def takeDocsInfoFromOneFile(path):
    global current_doc, current_DATE, current_CITY, current_DOCNO,docs_dictionary
    file = open(path, 'r')
    text_of_file = "".join(file.readlines())
    list_of_docs = text_of_file.split('</DOC>')
    del list_of_docs[-1] #not necessary

    for doc in list_of_docs:
        current_doc = doc
        __extractDOCNO()
        __extractCITY()
        __extractDATE()
        __extractTEXT()
        docs_dictionary[current_DOCNO] = DocumentInfo(current_DATE, current_CITY, str(path))


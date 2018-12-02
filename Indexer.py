
import pickle
import time

import TermInfo

main_dictionary = {} # {term : <df , ptr to the first occurrence of this term in posting file> }

__posting_files_path = ""
__current_posting = {}
__current_posting_file_name = 'others'
__dictionary_of_posting_pointers = {
    'a':'abc','b':'abc','c':'abc','A':'abc','B':'abc','C':'abc',
    'd':'defgh','e':'defgh','f':'defgh','g':'defgh','h':'defgh','D':'defgh','E':'defgh','F':'defgh','G':'defgh','H':'defgh',
    'i':'ijklmn', 'j':'ijklmn','k':'ijklmn','l':'ijklmn','m':'ijklmn','n':'ijklmn','I':'ijklmn','J':'ijklmn','K':'ijklmn','L':'ijklmn','M':'ijklmn','N':'ijklmn',
    'o':'opqrs','p':'opqrs','q':'opqrs','r':'opqrs','s':'opqrs','O':'opqrs','P':'opqrs','R':'opqrs','S':'opqrs','Q':'opqrs',
    't':'tuvwxyz','u':'tuvwxyz','v':'tuvwxyz','w':'tuvwxyz','x':'tuvwxyz','y':'tuvwxyz','z':'tuvwxyz','T':'tuvwxyz','U':'tuvwxyz','V':'tuvwxyz','W':'tuvwxyz','X':'tuvwxyz','Y':'tuvwxyz','Z':'tuvwxyz'
}

posting_abc = {}
posting_defgh = {}
posting_ijklmn = {}
posting_opqrs = {}
posting_tuvwxyz =  {}
posting_others = {}

__posting_from_disk = {}

__dictionary_of_postings = {'abc': posting_abc,'defgh': posting_defgh, 'ijklmn':posting_ijklmn, 'opqrs': posting_opqrs, 'tuvwxyz': posting_tuvwxyz, 'others': posting_others }



def create_posting_files():
    global __posting_files_path
    global __dictionary_of_postings

    for key in __dictionary_of_postings:
        with open(__posting_files_path + '\\' + str(key), 'wb') as file:
            pickle.dump(__dictionary_of_postings[key], file)
            file.close()

def insert_to_posting(term, docID_tf_dic):
    global __current_posting
    if term in __current_posting:
        tmp_termContentOnPostingFile = __current_posting[term]
        tmp_termContentOnPostingFile.update(docID_tf_dic)
    else:
        __current_posting[term] = docID_tf_dic


def set_path_to_postiong_files(path):
    global __posting_files_path
    __posting_files_path = path
    pass

def calculate_tf(doc_id_tf):
    counter = 0
    for key in doc_id_tf:
        counter = counter + doc_id_tf[key]
    return counter


def merge_dictionaries(dictionary): # {term : {doc id : tf}}
    global main_dictionary
    global __current_posting
    global __current_posting_file_name
    global __dictionary_of_posting_pointers
    for str_term in dictionary:
        str_term_0 = str_term[0]
        __current_posting = __dictionary_of_postings[__dictionary_of_posting_pointers.get(str_term_0,'others')]
        if str_term in main_dictionary: #in dictionary, posting file exists
            term_info = main_dictionary[str_term]
            term_info.add_df(len(dictionary[str_term]))
            term_info.add_tf(calculate_tf(dictionary[str_term]))
            insert_to_posting(str_term, dictionary[str_term])
        elif str_term.lower() in main_dictionary: #upper case -> insert as lower case
            str_term_lower = str_term.lower()
            term_info = main_dictionary[str_term_lower]
            term_info.add_df(len(dictionary[str_term]))
            term_info.add_tf(calculate_tf(dictionary[str_term]))
            insert_to_posting(str_term_lower, dictionary[str_term])
        elif str_term.islower():
            if str_term.upper() in main_dictionary:
                term_in_upper = str_term.upper()
                term_info = main_dictionary[term_in_upper]
                term_info.add_df(len(dictionary[str_term]))
                term_info.add_tf(calculate_tf(dictionary[str_term]))
                del main_dictionary[term_in_upper]
                main_dictionary[str_term] = term_info
                if term_in_upper in __current_posting:
                    current_posting_upper_content = __current_posting[term_in_upper]
                    del __current_posting[term_in_upper]
                    __current_posting[str_term] = current_posting_upper_content
                insert_to_posting(str_term, dictionary[str_term])
            else: # lower case not in dictionary
                term_info = TermInfo.TermInfo()
                term_info.add_df(len(dictionary[str_term]))
                term_info.add_tf(calculate_tf(dictionary[str_term]))
                term_info.set_ptr(__current_posting_file_name)
                main_dictionary[str_term] = term_info
                insert_to_posting(str_term, dictionary[str_term])
        else: #upper case not in dictionary
            term_info = TermInfo.TermInfo()
            term_info.add_df(len(dictionary[str_term]))
            term_info.add_tf(calculate_tf(dictionary[str_term]))
            term_info.set_ptr(__current_posting_file_name)
            main_dictionary[str_term] = term_info
            insert_to_posting(str_term, dictionary[str_term])


# merge 2 dictionaries of posting files
# the dictionary we get as argument is the most update by term upper/lower case.
# so we need to deal with it well
def mergePostingsAndSaveToDisk(key): # {term : { doc : term}}
    global __dictionary_of_postings
    global  __posting_from_disk
    posting_from_disk = __posting_from_disk
    dic = __dictionary_of_postings[key]
    for str_term in dic: # the most update term
        if str_term in posting_from_disk: # as it is
            posting_from_disk[str_term].update(dic[str_term])
        elif str_term.upper() in posting_from_disk: # in upper case in the old posting
            str_term_upper = str_term.upper()
            term_dic = posting_from_disk[str_term_upper]
            term_dic.update(dic[str_term])
            del posting_from_disk[str_term_upper]
            posting_from_disk[str_term] = term_dic # add with the lower case term
        else: # not exists
            posting_from_disk[str_term] = dic[str_term]
    write_posting_file_to_disk(key)

def write_posting_file_to_disk(key):
    global __posting_files_path
    global __posting_from_disk

    with open(__posting_files_path + '\\' + str(key), 'wb') as file:
        pickle.dump(__posting_from_disk, file)
        file.close()

def readPosting(key):
    global __posting_files_path
    global __posting_from_disk

    with open(__posting_files_path + '\\' + str(key), 'rb') as file:
        __posting_from_disk = pickle.load(file)
        file.close()

def SaveAndMergePostings():
    start = time.time()
    global __dictionary_of_postings
    for key in __dictionary_of_postings:
        readPosting(key)
        mergePostingsAndSaveToDisk(key)
        __dictionary_of_postings[key].clear()
    print (time.time() - start)


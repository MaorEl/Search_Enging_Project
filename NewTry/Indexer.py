
import pickle

from NewTry import TermInfo

main_dictionary = {} # {term : <df , ptr to the first occurrence of this term in posting file> }


__punctuations_for_file_name = { '\"','*','/', ':', '"','<', '>', '|'}
__posting_files_path = ""

def set_path_to_postiong_files(path):
    global __posting_files_path
    __posting_files_path = path
    pass

def update_exists_posting_file(posting_term_path, dic):
    with open(posting_term_path, 'rb') as file:
        o = pickle.load(file)
        file.close()
    with open(posting_term_path, 'wb') as file:
        o.update(dic)
        pickle.dump(o, file)
        file.close()

def create_new_posting_file(posting_term_path, dic):
    with open(posting_term_path, 'wb') as file:
        pickle.dump(dic, file)
        file.close()



def insert_to_posting(term, docID_tf_dic , isExists):
    global __posting_files_path
    clear_term = term.replace('\"','@_@').replace('*','@_@').replace(':','@_@').replace('"','@_@').replace('<','@_@').replace('>','@_@').replace('|','@_@').replace('?','@_@').replace('/','@_@')
    term_path = __posting_files_path + '\\' + clear_term + '.txt'
    if (isExists is True):
        update_exists_posting_file(term_path, docID_tf_dic)
    else:
        create_new_posting_file(term_path, docID_tf_dic)
    pass



def merge_dictionaries(dictionary): # {term : {doc id : tf}}
    global main_dictionary
    for str_term in dictionary:
        if str_term in main_dictionary: #in dictionary, posting file exists
            term_info = main_dictionary[str_term]
            term_info.add_df(len(dictionary[str_term]))
            insert_to_posting(str_term, dictionary[str_term], True)
        elif str_term.lower() in main_dictionary: #upper case -> insert as lower case
            str_term_lower = str_term.lower()
            term_info = main_dictionary[str_term_lower]
            term_info.add_df(len(dictionary[str_term]))
            insert_to_posting(str_term_lower, dictionary[str_term], True)
        elif str_term.islower():
            if str_term.upper() in main_dictionary:
                term_info = main_dictionary[str_term.upper()]
                term_info.add_df(len(dictionary[str_term]))
                del main_dictionary[str_term.upper()]
                main_dictionary[str_term] = term_info
                insert_to_posting(str_term, dictionary[str_term], True)
            else: # lower case not in dictionary
                term_info = TermInfo.TermInfo()
                term_info.add_df(len(dictionary[str_term]))
                main_dictionary[str_term] = term_info
                insert_to_posting(str_term, dictionary[str_term], False)
        else: #upper case not in dictionary
            term_info = TermInfo.TermInfo()
            term_info.add_df(len(dictionary[str_term]))
            main_dictionary[str_term] = term_info
            insert_to_posting(str_term, dictionary[str_term], False)




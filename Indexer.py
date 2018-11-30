
import pickle

import TermInfo

main_dictionary = {} # {term : <df , ptr to the first occurrence of this term in posting file> }

__posting_files_path = ""
__current_posting = {}
__current_posting_file_name = 'others'
__dictionary_of_posting_pointers = {
    'a':'abc','b':'abc','c':'abc','A':'abc','B':'abc','C':'abc',
    'd':'defgh','e':'defgh','f':'defgh','g':'defgh','h':'defgh','D':'defgh','E':'defgh','F':'defgh','G':'defgh','H':'defgh',
    'i':'ijklmn', 'j':'ijklmn','k':'ijklmn','l':'ijklmn','m':'ijklmn','n':'ijklmn','I':'ijklmn','J':'ijklmn','K':'ijklmn','L':'ijklmn','M':'ijklmn','N':'ijklmn',
    'o':'opqrs','p':'opqrs','q':'opqrs','r':'opqrs','s':'opqrs','O':'opqrs','P':'\opqrs','R':'opqrs','S':'opqrs','Q':'opqrs',
    't':'tuvwxyz','u':'tuvwxyz','v':'tuvwxyz','w':'tuvwxyz','x':'tuvwxyz','y':'tuvwxyz','z':'tuvwxyz','T':'tuvwxyz','U':'tuvwxyz','V':'tuvwxyz','W':'tuvwxyz','X':'tuvwxyz','Y':'tuvwxyz','Z':'tuvwxyz'
}

def create_empty_posting_files():
    global __posting_files_path
    with open(__posting_files_path + '\\abc', 'wb') as file: # 20 percent
        pickle.dump({}, file)
        file.close()
    with open(__posting_files_path + '\\defgh', 'wb') as file: # 18 percent
        pickle.dump({}, file)
        file.close()
    with open(__posting_files_path + '\\ijklmn', 'wb') as file: # 18 percent
        pickle.dump({}, file)
        file.close()
    with open(__posting_files_path + '\\opqrs', 'wb') as file: # 21 percent
        pickle.dump({}, file)
        file.close()
    with open(__posting_files_path + '\\tuvwxyz', 'wb') as file: # 24 percent
        pickle.dump({}, file)
        file.close()
    with open(__posting_files_path + '\\others', 'wb') as file:
        pickle.dump({}, file)
        file.close()


def insert_to_posting(term, docID_tf_dic, termIsAlreadyOnPostingFile):
    global __current_posting
    if termIsAlreadyOnPostingFile == True:
        tmp_termContentOnPostingFile = __current_posting[term]
        tmp_termContentOnPostingFile.update(docID_tf_dic)
    else:
        __current_posting[term] = docID_tf_dic


def set_path_to_postiong_files(path):
    global __posting_files_path
    __posting_files_path = path
    pass

def switch_dictionaries(letter):
    global __posting_files_path
    global __current_posting_file_name
    global __current_posting
    global __dictionary_of_posting_pointers
    with open(__posting_files_path + '\\' + __current_posting_file_name, 'wb') as file:
        pickle.dump(__current_posting, file)
        file.close()
    __current_posting_file_name = __dictionary_of_posting_pointers.get(letter, 'others')
    with open(__posting_files_path + '\\' + __current_posting_file_name, 'rb') as file:
        __current_posting = pickle.load(file)
        file.close()



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
        if __dictionary_of_posting_pointers.get(str_term_0,'others') != __current_posting_file_name:
            switch_dictionaries(str_term_0)
        if str_term in main_dictionary: #in dictionary, posting file exists
            term_info = main_dictionary[str_term]
            term_info.add_df(len(dictionary[str_term]))
            term_info.add_tf(calculate_tf(dictionary[str_term]))
            insert_to_posting(str_term, dictionary[str_term], True)
        elif str_term.lower() in main_dictionary: #upper case -> insert as lower case
            str_term_lower = str_term.lower()
            term_info = main_dictionary[str_term_lower]
            term_info.add_df(len(dictionary[str_term]))
            term_info.add_tf(calculate_tf(dictionary[str_term]))
            insert_to_posting(str_term_lower, dictionary[str_term], True)
        elif str_term.islower():
            if str_term.upper() in main_dictionary:
                term_in_upper = str_term.upper()
                term_info = main_dictionary[term_in_upper]
                term_info.add_df(len(dictionary[str_term]))
                term_info.add_tf(calculate_tf(dictionary[str_term]))
                del main_dictionary[term_in_upper]
                main_dictionary[str_term] = term_info
                current_posting_upper_content = __current_posting[term_in_upper]
                del __current_posting[term_in_upper]
                __current_posting[str_term] = current_posting_upper_content
                insert_to_posting(str_term, dictionary[str_term], True)
            else: # lower case not in dictionary
                term_info = TermInfo.TermInfo()
                term_info.add_df(len(dictionary[str_term]))
                term_info.add_tf(calculate_tf(dictionary[str_term]))
                term_info.set_ptr(__current_posting_file_name)
                main_dictionary[str_term] = term_info
                insert_to_posting(str_term, dictionary[str_term], False)
        else: #upper case not in dictionary
            term_info = TermInfo.TermInfo()
            term_info.add_df(len(dictionary[str_term]))
            term_info.add_tf(calculate_tf(dictionary[str_term]))
            term_info.set_ptr(__current_posting_file_name)
            main_dictionary[str_term] = term_info
            insert_to_posting(str_term, dictionary[str_term], False)





import pickle

from NewTry import TermInfo

main_dictionary = {} # {term : <df , ptr to the first occurrence of this term in posting file> }


__punctuations_for_file_name = { '\"','*','/', ':', '"','<', '>', '|'}
__posting_files_path = ""
__current_posting = {}
__current_posting_file_name = ''
__dictionary_of_posting_pointers = {
    'a':'\\abc','b':'\\abc','c':'\\abc','A':'\\abc','B':'\\abc','C':'\\abc',
    'd':'\\defgh','e':'\\defgh','f':'\\defgh','g':'\\defgh','h':'\\defgh','D':'\\defgh','E':'\\defgh','F':'\\defgh','G':'\\defgh','H':'\\defgh',
    'i':'\\ijklmn', 'j':'\\ijklmn','k':'\\ijklmn','l':'\\ijklmn','m':'\\ijklmn','n':'\\ijklmn','I':'\\ijklmn','J':'\\ijklmn','K':'\\ijklmn','L':'\\ijklmn','M':'\\ijklmn','N':'\\ijklmn',
    'o':'\\opqrs','p':'\\opqrs','q':'\\opqrs','r':'\\opqrs','s':'\\opqrs','O':'\\opqrs','P':'\\opqrs','R':'\\opqrs','S':'\\opqrs',
    't':'\\tuvwxyz','u':'\\tuvwxyz','v':'\\tuvwxyz','w':'\\tuvwxyz','x':'\\tuvwxyz','y':'\\tuvwxyz','z':'\\tuvwxyz','T':'\\tuvwxyz','U':'\\tuvwxyz','V':'\\tuvwxyz','W':'\\tuvwxyz','X':'\\tuvwxyz','Y':'\\tuvwxyz','Z':'\\tuvwxyz'
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
    global __posting_files_path
    global __current_posting_file_name
    global __current_posting
    clear_term = term.replace('\"','@_@').replace('*','@_@').replace(':','@_@').replace('"','@_@').replace('<','@_@').replace('>','@_@').replace('|','@_@').replace('?','@_@').replace('/','@_@')
    term_path = __posting_files_path + '\\' + __current_posting_file_name
    if termIsAlreadyOnPostingFile == True:
        tmp_termContentOnPostingFile = __current_posting[term]
        tmp_termContentOnPostingFile.update(docID_tf_dic)
    else:
        __current_posting[term] = docID_tf_dic




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



# def insert_to_posting(term, docID_tf_dic , isExists):
#     global __posting_files_path
#     clear_term = term.replace('\"','@_@').replace('*','@_@').replace(':','@_@').replace('"','@_@').replace('<','@_@').replace('>','@_@').replace('|','@_@').replace('?','@_@').replace('/','@_@')
#     term_path = __posting_files_path + '\\' + clear_term + '.txt'
#     if (isExists is True):
#         update_exists_posting_file(term_path, docID_tf_dic)
#     else:
#         create_new_posting_file(term_path, docID_tf_dic)
#     pass


def need_to_change_posting_file (letter):
    global __current_posting_file_name
    if letter == __current_posting_file_name:
        return True
    else:
        return False
    pass

def switch_dictionaries(letter):
    global __posting_files_path
    global __current_posting_file_name
    global __current_posting
    with open(__posting_files_path + '\\' + __current_posting_file_name, 'wb') as file:
        pickle.dump(__current_posting, file)
        file.close()
    __current_posting_file_name = letter
    with open(__posting_files_path + '\\' + __current_posting_file_name, 'rb') as file:
        __current_posting = pickle.load(file)
        file.close()



def add_tf_for_term_in_all_corpus(doc_id_tf,str_term):
    counter = 0
    for key in doc_id_tf:
        tmp = counter + doc_id_tf[key]
    tmp_term = main_dictionary[str_term]
    tmp_term.add_tf(counter)
    main_dictionary[str_term]=tmp_term


def merge_dictionaries(dictionary): # {term : {doc id : tf}}
    global main_dictionary
    for str_term in dictionary:
        if str_term in main_dictionary: #in dictionary, posting file exists
            term_info = main_dictionary[str_term]
            term_info.add_df(len(dictionary[str_term]))
            add_tf_for_term_in_all_corpus(dictionary[str_term],str_term)
            insert_to_posting(str_term, dictionary[str_term], True)
        elif str_term.lower() in main_dictionary: #upper case -> insert as lower case
            str_term_lower = str_term.lower()
            term_info = main_dictionary[str_term_lower]
            term_info.add_df(len(dictionary[str_term]))
            add_tf_for_term_in_all_corpus(dictionary[str_term],str_term)
            insert_to_posting(str_term_lower, dictionary[str_term], True)
        elif str_term.islower():
            if str_term.upper() in main_dictionary:
                term_info = main_dictionary[str_term.upper()]
                term_info.add_df(len(dictionary[str_term]))
                add_tf_for_term_in_all_corpus(dictionary[str_term], str_term)
                del main_dictionary[str_term.upper()]
                main_dictionary[str_term] = term_info
                insert_to_posting(str_term, dictionary[str_term], True)
            else: # lower case not in dictionary
                term_info = TermInfo.TermInfo()
                term_info.add_df(len(dictionary[str_term]))
                add_tf_for_term_in_all_corpus(dictionary[str_term], str_term)
                main_dictionary[str_term] = term_info
                insert_to_posting(str_term, dictionary[str_term], False)
        else: #upper case not in dictionary
            term_info = TermInfo.TermInfo()
            term_info.add_df(len(dictionary[str_term]))
            add_tf_for_term_in_all_corpus(dictionary[str_term],str_term)
            main_dictionary[str_term] = term_info
            insert_to_posting(str_term, dictionary[str_term], False)




import json
import pickle

from NewTry import Term

main_dictionary = {} # {term : <df , ptr to the first occurrence of this term in posting file> }


def insert_to_posting(term, docID_tf_dic):
    with open(term + '.txt', 'w') as file:
        file.write(json.dumps(docID_tf_dic))
    file.close()
    del file
    pass


def merge_dictionaries(dictionary): # {term : {doc id : tf}}
    global main_dictionary
    for str_term in dictionary:
        if str_term in main_dictionary: #in dictionary
            term = main_dictionary[str_term]
            term.add_df(len(dictionary[str_term]))
            insert_to_posting(str_term, dictionary[str_term])
        elif str_term.lower() in main_dictionary: #upper case -> insert as lower case
            str_term_lower = str_term.lower()
            term = main_dictionary[str_term_lower]
            term.add_df(len(dictionary[str_term]))
            insert_to_posting(str_term_lower, dictionary[str_term])
        elif str_term.islower():
            if str_term.upper() in main_dictionary:
                term = main_dictionary[str_term.upper()]
                term.add_df(len(dictionary[str_term]))
                del main_dictionary[str_term.upper()]
                main_dictionary[str_term] = term
                insert_to_posting(str_term, dictionary[str_term])
            else: # lower case not in dictionary
                term = Term.Term()
                term.add_df(len(dictionary[str_term]))
                main_dictionary[str_term] = term
                insert_to_posting(str_term, dictionary[str_term])
        else: #upper case not in dictionary
            term = Term.Term()
            term.add_df(len(dictionary[str_term]))
            main_dictionary[str_term] = term
            insert_to_posting(str_term, dictionary[str_term])



def index_dictionary(dictionary):
    merge_dictionaries(dictionary)
    pass


from NewTry import Term



main_dictionary = {} # {term : <df , ptr to the first occurrence of this term in posting file> }


def merge_dictionaries(dictionary):
    global main_dictionary
    for str_term in dictionary:
        if str_term.lower() in main_dictionary or str_term in main_dictionary:
            term = main_dictionary[str_term]
            term.add_df(term, len(dictionary[str_term]))
            # todo: add to posting
        elif str_term.islower():
            if str_term.upper() in main_dictionary:
                term = main_dictionary[str_term.upper()]
                term.add_df(term, dictionary[str_term].size())
                del main_dictionary[str_term.upper()]
                main_dictionary[str_term] = term
                # todo: add to posting
            else: # lower case not in dictionary
                term = Term.Term()
                term.add_df(len(dictionary[str_term]))
                main_dictionary[str_term] = term
                # todo: add to posting
        else: #upper case not in dictionary
            term = Term.Term()
            term.add_df(len(dictionary[str_term]))
            main_dictionary[str_term] = term
            # todo: add to posting



def index_dictionary(dictionary):
    merge_dictionaries(dictionary)
    pass


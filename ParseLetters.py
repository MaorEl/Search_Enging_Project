import os

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize


def tokenizeTexttoList(text):
    list = word_tokenize(text)
    return list

rootdir = "C:\Retrieval_folder\corpus"


def isExist(term, list):
    """
    this function check if a term already exist in the list of all terms
    :param term: to check if it is already in list
    :param list: list of all terms
    :return:    0 - not exist
                1 - exist as it is
                2 - exist in lower case version
                3 - exist in upper case version
    """
    if term in list:
        return 1
    else:
        if term.lower() in list:
            return 2
        elif term.upper() in list:
            return 3
        else :
            return 0


def Replace_Upper_to_Lower(term_lower_case, list):
    """
    this function removes the upper case term and adds the lower case term
    :param term_lower_case: term to replace
    :param list: list of all terms
    :return:
    """
    upperCase = term_lower_case.upper()
    list.remove(upperCase)
    list.append(term_lower_case)
    pass


def write_into_terms(list):
    """
    this function write all list into the file terms.
    # need to check about the python 3 in university
    :param list: list of terms
    :return: nothing :)
    """
    path = rootdir + "\\terms"
    if os.path.exists(path) == False:
        terms = open(path, 'w')
        terms.close()
        list_of_all_terms = []
    else:
        terms = open(path,'r')
        list_of_all_terms = [line.rstrip() for line in open(path)]
        terms.close()


    for might_be_term in list:
        # if the first letter is capital - change the term to upper case
        if might_be_term[0] >= 'A' and might_be_term[0] <= 'Z':
            might_be_term = might_be_term.upper()
        else : #else , just leave it lower
            might_be_term = might_be_term.lower()

        might_be_term_isExist = isExist(might_be_term,list_of_all_terms)
        if might_be_term_isExist == 0:
            list_of_all_terms.append(might_be_term)
        elif might_be_term_isExist == 3:
            Replace_Upper_to_Lower(might_be_term,list_of_all_terms)

        with open(path, "w") as f:
            for term in list_of_all_terms:
                f.write(str(term) + "\n")

        #
        # terms = open(path,'w')
        # terms.writelines(list_of_all_terms) #available only in python 3
        # terms.close()



text = "I Cat. cat is bad."
list = tokenizeTexttoList(text)
write_into_terms(list)










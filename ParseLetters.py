import datetime
import os

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize


def tokenizeTexttoList(text):
    list = word_tokenize(text)
    return list

rootdir = "C:\Retrieval_folder\corpus"
months_choices = []
for i in range(1,13):
    months_choices.append(datetime.date(2008, i, 1).strftime('%B').upper())


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

def parse_Month (month):
    return  {
        "JANUARY": "01",
        "FEBRUARY": "02",
        "MARCH": "03",
        "APRIL": "04",
        "MAY": "05",
        "JUNE": "06",
        "JULY": "07",
        "AUGUST": "08",
        "SEPTEMBER": "09",
        "OCTOBER": 10,
        "NOVEMBER": 11,
        "DECEMBER": 12
    }[month]



def ParseDate(month, day_or_year):
    if len(day_or_year) == 1:
        day_or_year = "0" + str(day_or_year)
        return str(month) + "-" + str(day_or_year)
    elif len(day_or_year) == 2:
        return str(month) + "-" + str(day_or_year)
    else:
        return str(day_or_year)+ "-" + str(month)



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
        #take care of dates
        if might_be_term.upper() in months_choices:
            day_or_year = list.pop(1)
            month = parse_Month(might_be_term)
            might_be_term = ParseDate (month, day_or_year)

        # if the first letter is capital - change the term to upper case
        elif might_be_term[0] >= 'A' and might_be_term[0] <= 'Z':
            might_be_term = might_be_term.upper()
        elif might_be_term[0] >= 'a' and might_be_term[0] <= 'z': #else , just leave it lower
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



text = "DECEMBER 1992 kenene"
list = tokenizeTexttoList(text)
write_into_terms(list)










import datetime
import os

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

__months_set = {'january':'01', 'jan':'01', 'february':'02', 'feb':'02', 'march':'03', 'mar':'03', 'april':'04', 'apr':'04',
                'may':'05', 'june':'06', 'jun':'06', 'july':'07', 'jul':'07', 'august':'08', 'aug':'08', 'september':'09',
                'sep':'09', 'october':'10', 'oct':'10', 'november':'11', 'nov':'11', 'december':'12', 'dec':'12'}


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

#will return MM-DD date
def dd_month_format(day,month):
    if (len(day)==1):
        day='0'+day
    return __months_set[month] + '-' + day  ;

#will return YYYY-MM
def month_year_format(month, year):
    return year + '-' +__months_set[month]


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
            place_in_list = list.index(might_be_term) + 1
            day_or_year = list.pop(place_in_list)
            month = parse_Month(might_be_term.upper())
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



text = "January 1984 january 22"
list = tokenizeTexttoList(text)
write_into_terms(list)










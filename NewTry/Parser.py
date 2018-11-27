import time
from fractions import Fraction
from NewTry import PorterStemmer

__punctuations_set = {'[', '(', '{', '`', ')', '<', '|', '&', '~', '+', '^', '@', '*', '?', '.',
                      '>', ';', '_', '\'', ':', ']', '\\', "}", '!', '=', '#', ',', '\"','-','/'}

__months_set = {'january':'01', 'jan':'01', 'february':'02', 'feb':'02', 'march':'03', 'mar':'03', 'april':'04', 'apr':'04',
                'may':'05', 'june':'06', 'jun':'06', 'july':'07', 'jul':'07', 'august':'08', 'aug':'08', 'september':'09',
                'sep':'09', 'october':'10', 'oct':'10', 'november':'11', 'nov':'11', 'december':'12', 'dec':'12'}

__stop_words = []
stop_words_dict = {}
stemmed_terms = {}
stemmer = PorterStemmer.PorterStemmer()
one_file_dictionary = {}


def set_stop_words_file(path):
    global __stop_words
    with open(path,'r') as wordbook:
        __stop_words = wordbook.read().splitlines()
        global stop_words_dict
        for term in __stop_words:
            stop_words_dict[term]=0

def _clean_stop_words(dictionary):
    for term in stop_words_dict:
        if term in dictionary:
            dictionary.pop('key', None)

def clean_term_from_punctuations(term):
    length = term.__len__()
    while length > 0 and term[len(term)-1] in __punctuations_set:
        term = term[:-1]
        length -= 1
    while length > 0 and term[0] in __punctuations_set:
        term = term[1:]
        length -= 1
    return term


def isNumeric(word):
    return word.isdigit() or word.replace(',','').replace('.','').replace('$','').replace('m','').replace("bn",'').isdigit()

def get_clear_number(word):
    return word.replace('$','').replace('m','').replace("bn",'')

def get_bn_ot_m(word):
    if "bn" in word:
        return "B"
    elif "m" in word:
        return "M"
    elif "t" in word:
        return "T"
    else: return ""


def convertToFloat(word):
    return float(word.replace(',',''))


#function to avoid ".0" in end of float numbers
def formatNumber(num):
        if num % 1 == 0:
            return int(num)
        else:
            return num

def price_format(price, bmt=''):
    price = convertToFloat(price)
    if bmt == '':
        if price<1000000:
            return str(formatNumber(price)) + ' Dollars'
        else: return str(formatNumber(price/1000000)) + ' M Dollars'
    elif bmt == 'M':
        return str(formatNumber(price)) + ' M Dollars'
    elif bmt == 'B':
        return str(formatNumber((price*1000)))  + ' M Dollars'
    elif bmt == 'T':
        return str(formatNumber((price*1000000)))   + ' M Dollars'

def fraction_price_format(number, fraction):
    if fraction.count('/') >= 2:
        fraction = eval(fraction)
        fraction = Fraction(fraction)
    return number + ' ' + str(fraction) + ' Dollars'

def percentage_format(number):
    return number + '%'


#  will get a number and text like 123 Million and change to 123M
def number_kbmt_format(number, word):
    newFormat=''
    if word.lower() == 'thousand':
        newFormat =  str(number) + 'K'
    elif word.lower() == 'million':
        newFormat =  str(number) + 'M'
    elif word.lower() == 'billion':
        newFormat =  str(number)+ 'B'
    elif word.lower() == 'trillion':
        newFormat =  str(number) + 'T'
    elif word.lower() == 'quadrillion':
        newFormat = str(number) + 'Q'
    return newFormat


def number_format(number):
    number = convertToFloat(number)
    if number < 1000: # numbers smaller than 1000
        return str(formatNumber(number))
    elif number < 1000000: #numebrs between 1K to 1M
        return str(formatNumber(number/1000)) + 'K'
    elif number < 1000000000: #numbers between 1M to 1B
        return str(formatNumber(number/1000000)) + 'M'
    else:  # numbers > 1B
        return str(formatNumber(number/1000000000)) + 'B'


#will return MM-DD date
def dd_month_format(day,month):
    if (len(day)==1):
        day='0'+day
    return __months_set[month.lower()] + '-' + day

#will return YYYY-MM
def month_year_format(month, year):
    return year + '-' +__months_set[month.lower()]


def upper_lower_case_format(term):
    if term[0] >='A' and term[0] <='Z':
        return term.upper()
    return term.lower()


def size_format(term, size):
    if size == "meters":
        return term + "m"
    elif size == "millimeters":
        return term + "mm"
    elif size == "centimeters":
        return term + "cm"
    elif size == "nanometers":
        return term + "nm"
    elif size == "kilometers":
        return term + "km"


def contains_char(term):
    return (not (term.replace('.', '').replace(',', '').isdigit()))

def contains_digit(term):
    return any(char.isdigit() for char in term)


def one_dot_in_price(term):
    if term.count('.') >= 2:
        one_dot = False
        i = 0
        for i in range(len(term) - 1):
            if term[i] == '.' and one_dot is False:
                one_dot = True
            elif term[i] == '.' and one_dot is True:
                term = term[:i] + term[i+1:]
    return term

def stem_the_term(term):
    global stemmed_terms
    s = stemmed_terms
    if term.isupper():
        lower_new_term = term.lower()
        if lower_new_term not in stemmed_terms:
            stemmed_term = stemmer.stem(lower_new_term)
            stemmed_terms[lower_new_term] = stemmed_term
            new_term = stemmed_term.upper()
        else:  # in stemmed_terms
            new_term = stemmed_terms[lower_new_term]
    else:  # lower case
        if term not in stemmed_terms:
            stemmed_term = stemmer.stem(term)
            stemmed_terms[term] = stemmed_term
            new_term = stemmed_term
        else:  # in stemmed_terms
            new_term = stemmer.stem(term)
    return new_term

def insert_to_dic(new_term, doc):
    dic = one_file_dictionary
    if new_term.lower() in stop_words_dict.keys():
        return
    if new_term in one_file_dictionary:  # term exists in dictionary
        if doc in (one_file_dictionary[new_term]):
            insert_to_here = one_file_dictionary[new_term]
            insert_to_here[doc] += 1
        else:
            insert_to_here = one_file_dictionary[new_term]
            insert_to_here[doc] = 1
    elif new_term.upper() in one_file_dictionary:  # in dictionary in upper case
        data_inside = one_file_dictionary[new_term.upper()]
        if doc in (data_inside): # just add 1
            data_inside[doc] += 1
            one_file_dictionary[new_term] = data_inside
        else:
            data_inside[doc] = 1
            one_file_dictionary[new_term] = data_inside
        del one_file_dictionary[new_term.upper()]
    else:
        one_file_dictionary[new_term] = {doc: 1}



def parse(dictionary, file):
    #print(file)
    global stemmed_terms
    global stemmer
    global one_file_dictionary
    one_file_dictionary = {} # contains : key = term , value = {docID : frequency in doc}
    for doc in dictionary:
        text = dictionary[doc]
        if text is not None or text is not "":
            index = 0
            splited = text.split()
            length_of_splited_text = len(splited)
            while index < length_of_splited_text:
                stem = False # at the end of the loop, if FALSE don't stem the term, if TRUE stem the term
                new_term =""
                original_term = splited[index]
                term = clean_term_from_punctuations(original_term)

                if len(term) == 0 or term =='':
                    index = index + 1
                    continue
                if isNumeric(term): #for numbers , pruces, percentage, dates
                    if '$' in term:
                        term = one_dot_in_price(term)
                        if index + 1 != length_of_splited_text:
                            next_word = clean_term_from_punctuations(splited[index + 1].lower())
                            if next_word in ["million", "billion", "trillion"]:
                                new_term = price_format(get_clear_number(term), next_word[0].upper()) # $ price million/billion,trillion
                                index = index + 2
                            else:
                                new_term = price_format(get_clear_number(term)) # S price
                                index = index + 1
                        else: #last one in text
                            new_term = price_format(get_clear_number(term)) # $ price
                            index = index + 1
                    elif 'mm' in term or 'cm' in term or 'm' in term or 'km' in term or 'nm' in term:
                        new_term = term
                        index = index + 1
                    elif term.count('.') >= 2:
                        new_term = term
                        index = index + 1
                    else: # no $
                        if index + 1 < length_of_splited_text:
                            next_word = clean_term_from_punctuations(splited[index + 1].lower())
                            if next_word in ["percentage","percent"]:
                                new_term = percentage_format(term) # number percent/percentage
                                index = index + 2
                            elif next_word == "dollars":
                                new_term = price_format(get_clear_number(term),get_bn_ot_m(term)) # price dollars
                                index = index + 2
                            elif next_word in ["million", "billion", "trillion"]:
                                if index + 3 < length_of_splited_text:
                                    third_word = clean_term_from_punctuations(splited[index+2])
                                    fourth_word = clean_term_from_punctuations(splited[index+3].lower())
                                    if third_word == "U.S" and fourth_word == "dollars":
                                        new_term = price_format(get_clear_number(term),next_word[0].upper()) # price million/trillion/billion U.S dollars
                                        index = index + 4
                                    else:
                                        new_term = number_kbmt_format(term, next_word) # number million/billion/trillion
                                        index = index + 2
                                else:
                                    new_term = number_kbmt_format(term, next_word)# number million/billion/trillion
                                    index = index + 2
                            elif next_word == "thousand":
                                new_term = number_kbmt_format(term, next_word) # number thousand
                                index = index + 2
                            elif next_word in ["meters", "kilometers", "millimeters", "centimeters", "nanometers"]:
                                new_term = size_format(term, next_word) # number meters, kilometers, centimeters, nanoneters, millimeters
                                index = index + 2
                            elif next_word in __months_set:
                                new_term = dd_month_format(term, next_word) # DD Month
                                index = index + 2
                            elif index + 2 != length_of_splited_text:
                                third_word = clean_term_from_punctuations(splited[index+2].lower())
                                if third_word == "dollars" and '/' in next_word and isNumeric(next_word.replace('/','')):
                                    new_term = fraction_price_format(get_clear_number(term), get_clear_number(next_word)) #number fraction dollars
                                    index = index + 3
                                elif next_word in ["m", "bn", "t"] and third_word == "dollars":
                                    new_term = price_format(get_clear_number(term), get_bn_ot_m(next_word))  # price m/bn dollars
                                    index = index + 3
                                elif contains_char(term):
                                    new_term = term
                                    index = index + 1
                                else:
                                    new_term = number_format(term) # number
                                    index = index + 1
                            else:
                                if contains_char(term):
                                    new_term = term
                                    index = index + 1
                                else:
                                    new_term = number_format(term) # number
                                    index = index + 1
                        else: #last number in text
                            if contains_char(term):
                                new_term = term
                                index = index + 1
                            else:
                                new_term = number_format(term) # number
                                index = index + 1
                else: # take care of words
                    if term.lower() in __months_set.keys():
                        if index + 1 != length_of_splited_text:
                            next_word = clean_term_from_punctuations(splited[index+1])
                            if next_word.isdigit() and len(next_word)<=2:
                                new_term = dd_month_format(next_word,term) # DD month
                                index = index + 2
                            elif next_word.isdigit() and len(next_word)==4:
                                new_term = month_year_format(term,next_word) # month year
                                index = index + 2
                            else:  # upper/lower case regular word
                                new_term = upper_lower_case_format(term)
                                index = index + 1
                        else:  # upper/lower case regular word
                            new_term = upper_lower_case_format(term)
                            index = index + 1
                    elif term.lower() == "between" and index + 3 <length_of_splited_text:
                        number1 = clean_term_from_punctuations(splited[index + 1])
                        if isNumeric(number1):
                            and_= clean_term_from_punctuations(splited[index + 2])
                            if and_ == "and":
                                number2 = clean_term_from_punctuations(splited[index + 3])
                                if isNumeric(number2):
                                    new_term = "between " + clean_term_from_punctuations(number1) + " and " + clean_term_from_punctuations(number2) #between n1 and n2
                                    index = index + 4
                                else:  # upper/lower case regular word
                                    new_term = upper_lower_case_format(term)
                                    index = index + 1
                            else:  # upper/lower case regular word
                                new_term = upper_lower_case_format(term)
                                index = index + 1
                        else:  # upper/lower case regular word
                            new_term = upper_lower_case_format(term)
                            index = index + 1
                    elif '-' in term:
                        new_term = term
                        index = index + 1
                    else: # upper/lower case regular word
                        new_term = upper_lower_case_format(term)
                        index = index + 1
                        if not contains_digit(new_term):
                            stem = True
                ###################################DONE WITH PARSING########################################
                ###################################STEMMING SECTION#########################################
                #if stem is True and new_term.lower() not in stop_words_dict.keys():
                    #new_term = stem_the_term(new_term)
                ###################################END OF STEM SECTION######################################
                insert_to_dic(new_term, str(doc))
    return one_file_dictionary


                #todo: check in indexer if term exist upper/lower ->> merging the keys

##dobug##
# path = 'C:\Retrieval_folder\\full_corpus'
# __stopwords_path = path + "/stop_words.txt"
# set_stop_words_file(__stopwords_path)
# text = "internity intern Dog dogs"
# dic = {}
# dic ["doc1"] = text
# parse(dic,"m")

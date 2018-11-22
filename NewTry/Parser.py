import time

__punctuations_set = {'[', '(', '{', '`', ')', '<', '|', '&', '~', '+', '^', '@', '*', '?', '.',
                      '>', ';', '_', '\'', ':', ']', '\\', "}", '!', '=', '#', ',', '\"','-','/'}

__months_set = {'january':'01', 'jan':'01', 'february':'02', 'feb':'02', 'march':'03', 'mar':'03', 'april':'04', 'apr':'04',
                'may':'05', 'june':'06', 'jun':'06', 'july':'07', 'jul':'07', 'august':'08', 'aug':'08', 'september':'09',
                'sep':'09', 'october':'10', 'oct':'10', 'november':'11', 'nov':'11', 'december':'12', 'dec':'12'}

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
    return number + fraction

def percentage_format(number):
    return number + '%'


#  will get a number and text like 123 Million and change to 123M
def number_kbmt_format(number, word):
    newFormat=''
    if word.lower() == 'thousand':
        newFormat =  str(number) + 'K'
    elif word.lower() == 'million':
        newFormat =  str(number) + 'M'
    elif word.lower == 'billion':
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
    return not (term.replace('.', '').isdigit())


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


def parse(dictionary, file):
    counter = 0
    one_file_dictionary = {} # contains : key = docID , value = {term : frequency in doc}
    for doc in dictionary:
        print (doc)
        counter =+ 1
        one_doc_dictionary = {} # term : frequency in doc
        text = dictionary[doc]
        if text is not None or text is not "":
            index = 0
            splited = text.split()
            length_of_splited_text = len(splited)
            while index < length_of_splited_text:
                new_term =""
                original_term = splited[index]
                term = clean_term_from_punctuations(original_term)

                if len(term) == 0:
                    index = index + 1
                    continue
                if isNumeric(term): #for numbers , pruces, percentage, dates
                    if '$' in term:
                        term = one_dot_in_price(term)
                        if index + 1 != length_of_splited_text:
                            next_word = splited[index + 1].lower()
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
                            next_word = splited[index + 1].lower()
                            if next_word in ["percentage","percent"]:
                                new_term = percentage_format(term) # number percent/percentage
                                index = index + 2
                            elif next_word == "dollars":
                                new_term = price_format(get_clear_number(term),get_bn_ot_m(term)) # price dollars
                                index = index + 2
                            elif next_word in ["million", "billion", "trillion"]:
                                if index + 3 < length_of_splited_text:
                                    third_word = splited[index+2]
                                    fourth_word = splited[index+3].lower()
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
                            elif index + 2 != length_of_splited_text:
                                third_word = splited[index+2].lower()
                                if third_word == "dollars" and '/' in next_word and isNumeric(next_word.replace('/','')):
                                    new_term = fraction_price_format(get_clear_number(term), get_clear_number(next_word)) #number fraction dollars
                                    index = index + 3
                                elif contains_char(term):
                                    new_term = term
                                    index = index + 1
                                else:
                                    new_term = number_format(term) # number
                                    index = index + 1
                            elif next_word in __months_set:
                                new_term = dd_month_format(term, next_word) # DD Month
                                index = index + 2
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
                            next_word = splited[index+1]
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
                        number1 = splited[index + 1]
                        if isNumeric(number1):
                            and_= splited[index + 2]
                            if and_ == "and":
                                number2 = splited[index + 3]
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
                ###################################DONE WITH PARSING########################################
                if new_term in one_doc_dictionary:
                    one_doc_dictionary[new_term] += 1
                else: # not in dictionary
                    one_doc_dictionary[new_term] = 1
        one_file_dictionary[str(doc)] = one_doc_dictionary
    return one_file_dictionary


                    #Todo: advance the index
                    #Todo: take care of upper/lower cases
                    #Todo: add functions as needed
                #todo: check in indexer if term exist upper/lower ->> merging the keys






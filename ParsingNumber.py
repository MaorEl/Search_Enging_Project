

rootdir = "C:\Retrieval_folder\corpus"
def write_into_terms(list):
    path = rootdir + "\\terms"
    terms = open(path,'a')
    terms.writelines(list) #TODO: available only in python 3. we need to check what they have on labratories
    terms.close()
    terms = open(path,'r')
    terms_list = terms.read()
    if 'maor' in terms_list:
        print("yes")

write_into_terms(['maorrrrr'])

# def isWordOnTermsFile(word):
# list_of_sentences = content.split(".")
# for sentence in list_of_sentences:
#     words = sentence.split(" ")
#     for word in words:
#         if word == key:
#             print sentence

### returns True only if there is only digits on the number (without ','))
def thisIsRegularNumber(word):
    return word.isdigit() or word.replace(',','').replace('.','').isdigit()


def convertToFloat(word):
    return float(word.replace(',',''))


#function to avoid ".0" in end of float numbers
def formatNumber(num):
        if num % 1 == 0:
            return int(num)
        else:
            return num



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
#
# list_of_numbers = random.sample(range(0, 1000000), 100)
# bmt = ['B','M','T', '']
# for i in range(len(list_of_numbers)):
#     index = i%4;
#     print ("Number should be: " + str(list_of_numbers[i]) + bmt[index] + "||||" + price_format(str(list_of_numbers[i]),bmt[index])    )
#
#





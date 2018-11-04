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
    pass


def convertToFloat(word):
    return float(word.replace(',',''))


def changeFormatToKMB(number):
    if number < 1000: # numbers smaller than 1000
        return number
    elif number <= 1000000: #numebrs between 1K to 1M
        return str(number/1000) + 'K'
    elif number <= 1000000000: #numbers between 1M to 1B
        return str(number/1000000) + 'M'
    else:  # numbers > 1B
        return str(number/1000000000) + 'B'
    pass

#  will get a number and text like 123 Million and change to 123M
def changenumberAndTextToKMBFormat(number, word):
    if word.lower() == 'thousand':
        return number + 'K'
    elif word.lower() == 'million':
        return number + 'M'
    elif word.lower == 'billion':
        return number + 'B'
    elif word.lower() == 'trillion':
        return number*1000 + 'B'
    elif word.lower == 'quadrillion':
        return number*1000000 + 'B'








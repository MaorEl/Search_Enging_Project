

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







#
# list_of_numbers = random.sample(range(0, 1000000), 100)
# bmt = ['B','M','T', '']
# for i in range(len(list_of_numbers)):
#     index = i%4;
#     print ("Number should be: " + str(list_of_numbers[i]) + bmt[index] + "||||" + price_format(str(list_of_numbers[i]),bmt[index])    )
#
#





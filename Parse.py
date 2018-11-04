
from nltk.tokenize import sent_tokenize, word_tokenize
# import nltk
# nltk.download('punkt')


class Parse:



    def tokenizeTexttoList(text):
        list = word_tokenize(text)
        return list


text = 'Providi 100,000K, 100000 $68, $20.40, 30$ and $10.80, the 3-1 choice, in the final yards. Three lengths back was U.S.-built, Libyan-owned C-130 and Boeing 707 transport planes into refueling </P>'
list = Parse.tokenizeTexttoList(text)
print (list)

string_num = '563,331.45'
print (string_num.isdigit() or string_num.replace(',','').replace('.','').isdigit())
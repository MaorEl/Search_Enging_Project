
__punctuations_set = {'[', '(', '{', '`', ')', '<', '|', '&', '~', '+', '^', '@', '*', '?', '$', '.',
                      '>', ';', '_', '\'', ':', ']', '/', '\\', "}", '!', '=', '#', ',', '\"', '-'}



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
    return word.isdigit() or word.replace(',','').replace('.','').replace('%','').replace('$','').replace('m','').replace("bn",'').isdigit()


def parse(dictionary):
    for doc in dictionary:
        text = dictionary[doc]
        if text is not None or text is not "":
            index = 0
            splited = text.split()
            for term in splited:
                term = clean_term_from_punctuations(term)
                if isNumeric(term):
                    next_word = splited[index + 1]
                    if next_word.lower() in ["thousand", "milloin", "billion", "trillion"]:
                        if '$' in term:
                            $price_mbtt_Format2(index) # $price million / billion / trillion / thousand
                        third_word = splited[index + 2]
                        fourth_word = splited[index + 3]
                        if third_word == "U.S" and fourth_word.lower() == "dollar":
                            price_bmtt_US_dollars_Format(index) # price million / billion / trillion / thousand U.S. dollars
                        else:
                            changenumberAndTextToKMBFormat(index) # number million / billion / trillion / thousand
                    elif next_word.lower() in ["percent", "percentage"]:
                        changenumberAndTextToPercentageFormat(term)
                    elif next_word.lower() in ["dollar"]:
                        changenumberAndTextToPriceFormat(term)
                print(term)
                index += 1
            print("stop")





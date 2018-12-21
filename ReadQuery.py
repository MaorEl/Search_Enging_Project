

def create_dictionary_from_free_text_query(text):
     return {'1': text}

def __cleanFromSpaces(param):
    text_list = param.split()
    return " ".join(text_list)
    pass


def create_dictionary_of_file(path_of_query_file):
    '''
    this function returns dictionaries of queryID:title & queryID:content
    by spliting the text by tags
    :param path_of_query_file: path
    :return: dictionaries queryID:title & queryID:content
    '''
    query_dic_by_title = { }#qurery_id: text of title query
    query_dic_by_addons = {} #qurery_id: text of desc+narr
    file = open(path_of_query_file, 'r')
    queries = "".join(file.readlines())
    queries_list = queries.split('</top>')
    queries_list = queries_list[:-1]

    for q in queries_list:
        text = q.replace("\n", ' ')
        text = "".join(text.split("<top>"))
        text = text.split(" <num> Number:")[1]
        text = text.split("<title> ")
        query_num = __cleanFromSpaces(text[0])
        text = text[1]
        text = text.split("<desc> Description: ")
        query_title = __cleanFromSpaces(text[0])
        text = text[1]
        text = text.split("<narr> Narrative: ")
        query_desc = __cleanFromSpaces(text[0])
        #query_narr = __cleanFromSpaces(text[1])

        query_dic_by_title[query_num] = query_title
        query_dic_by_addons[query_num] = query_desc
        #not includes naratives

    return query_dic_by_title, query_dic_by_addons





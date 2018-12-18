# import collections
# import csv
# import operator
# import pickle
# import re
# import urllib
# import json
# #
# # __dictionary_of_postings = {1:{1:1,1:2}, 2:{2:1,2:2}}
# #
# # url = 'http://getcitydetails.geobytes.com/GetCityDetails?fqcn=Paris'
# # response = urllib.urlopen(url)
# # json = json.loads(response.url)
# #
# # with urllib.request.urlopen(url) as url:
# #     s = url.read()
# #     json = json.loads(s)
# # #I'm guessing this would output the html source code?
# # print(s)
# # x=2
# # for key in __dictionary_of_postings:
# #     with open('C:\Retrieval_folder\index' + '\\' + str(key), 'wb') as file:
# #         pickle.dump(__dictionary_of_postings[key], file)
# #         file.close()
# #         x=2
# #
# #
# # #
# # #
# # with open( 'D:\documents\\users\\anaelgor\Downloads\corpus\index\cities', 'rb') as file:
# #     cities = pickle.load(file)
# #     print('x')
# #     file.close()
# #
#
# dic = {}
#
# with open( 'C:\Retrieval_folder\index\opqrs', 'rb') as file:
#     q1 = pickle.load(file)
#     #print( "Q1: " + str(len(q1)))
#     file.close()
#
# for term in q1:
#     docs = q1[term]
#     if 'FBIS3-3366' in docs:
#         dic[term] = docs['FBIS3-3366']
#
# with open('C:\Retrieval_folder\index\\tuvwxyz', 'rb') as file:
#     q1 = pickle.load(file)
#     # print( "Q1: " + str(len(q1)))
#     file.close()
#
# for term in q1:
#     docs = q1[term]
#     if 'FBIS3-3366' in docs:
#         dic[term] = docs['FBIS3-3366']
#
# with open( 'C:\Retrieval_folder\index\\abc', 'rb') as file:
#     q1 = pickle.load(file)
#     #print( "Q1: " + str(len(q1)))
#     file.close()
#
# for term in q1:
#     docs = q1[term]
#     if 'FBIS3-3366' in docs:
#         dic[term] = docs['FBIS3-3366']
#
# with open( 'C:\Retrieval_folder\index\defgh', 'rb') as file:
#     q1 = pickle.load(file)
#     #print( "Q1: " + str(len(q1)))
#     file.close()
#
# for term in q1:
#     docs = q1[term]
#     if 'FBIS3-3366' in docs:
#         dic[term] = docs['FBIS3-3366']
#
# with open( 'C:\Retrieval_folder\index\ijklmn', 'rb') as file:
#     q1 = pickle.load(file)
#     #print( "Q1: " + str(len(q1)))
#     file.close()
#
# for term in q1:
#     docs = q1[term]
#     if 'FBIS3-3366' in docs:
#         dic[term] = docs['FBIS3-3366']
#
# with open( 'C:\Retrieval_folder\index\others', 'rb') as file:
#     q1 = pickle.load(file)
#     #print( "Q1: " + str(len(q1)))
#     file.close()
#
# for term in q1:
#     docs = q1[term]
#     if 'FBIS3-3366' in docs:
#         dic[term] = docs['FBIS3-3366']
#
#
# print (dic)
# dic = collections.OrderedDict(sorted(dic.items()))
# v=1
# # with open( 'C:\Retrieval_folder\index\main_dictionary_stem', 'rb') as file:
# #     q2 = pickle.load(file)
# #     print( "Q2: " + str(len(q2)))
# #     file.close()
# #
# # q3 = []
# # for term in q2:
# #     if term[len(term) - 1] in ['K', 'B', 'M']:
# #         t = term[:-1]
# #         one_dot = 0
# #         isitterm = True
# #         for i in t:
# #             if i == '.' and one_dot == 0:
# #                 one_dot = 1
# #             elif i == '.' and one_dot == 1:
# #                 isitterm = False
# #             elif i <= '0' and i >= '9':
# #                 isitterm = False
# #         if isitterm:
# #             q3.append(term)
# #     elif term.isdigit():
# #         q3.append(term)
# # print( "Q3: " + str(len(q3)))
# #
# # with open( 'C:\Retrieval_folder\index\cities_stem' , 'rb') as file:
# #     cities = pickle.load(file)
# #     file.close()
# # #q4 = [cities[x].country for x in cities ]
# # list=[]
# # for city in cities:
# #     c = cities[city]
# #     if hasattr(c, 'country'):
# #         if c.country not in list and c.country != '':
# #             list.append(cities[city].country)
# # print( "Q4: " + str(len(list)))
# # print( "Q5_1: " + str(len(cities)))
# # not_capital = []
# # for i in cities:
# #     c = cities[i]
# #     if hasattr(c, 'capital'):
# #         if i != c.capital.upper():
# #             not_capital.append(i)
# #     else:
# #         not_capital.append(i)
# # print( "Q5_2: " + str(len(not_capital)))
# #
# # cityname = ''
# # dicname = ''
# # maxtf = 0
# # for city in cities:
# #     dic = cities[city].dic_doc_index
# #     for doc in dic:
# #         if len(dic[doc]) >maxtf:
# #             maxtf = len(dic[doc])
# #             docname = str(doc)
# #             cityname = city
# # print ("Q6: " + cityname + ', ' + docname+ ', ' + str(maxtf))
# #
# #
# # #sorted_dictionary = collections.OrderedDict(sorted(q1.items(), key=lambda x: x[1]['tf_in_corpus']))
# #    # OrderedDict(sorted(q1.values(), key = operator.attrgetter('tf_in_corpus')))
#
# # dictf = {}
# # for term in q1:
# #     terminfo = q1[term]
# #     dictf[term] = terminfo.tf_in_corpus
# # sorted_dictionary = collections.OrderedDict(sorted(dictf.items(), key=operator.itemgetter(1)))
# #
# # print ("Q7: ")
# # counter = 0
# # for te in sorted_dictionary:
# #     if counter <= 15:
# #         print (te)
# #     elif counter >= 1220090:
# #         print (te)
# #     counter += 1
#
# # with open ('C:\Retrieval_folder\Q9-result\main_dictionary', 'rb') as file:
# #     q9 = pickle.load(file)
# #     sorted = dict(sorted(q9.items()))
# #     file.close()
# # for key in sorted:
# #     print (key +'\t' + str(sorted[key].tf_in_corpus))
#
#
# #
# # with open('C:\Retrieval_folder\\test.csv', 'w') as f:
# #     writer = csv.writer(f)
# #     for row in q1.items():
# #         new = (row[0],row[1].tf_in_corpus)
# #         writer.writerow(new)
# #
#
#
#
# x=1
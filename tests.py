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


import tkinter as tk
from random import randint

# --- classes ---

class ScrolledFrame(tk.Frame):

    def __init__(self, parent, vertical=True, horizontal=False):
        super().__init__(parent)

        # canvas for inner frame
        self._canvas = tk.Canvas(self)
        self._canvas.grid(row=0, column=0, sticky='news') # changed

        # create right scrollbar and connect to canvas Y
        self._vertical_bar = tk.Scrollbar(self, orient='vertical', command=self._canvas.yview)
        if vertical:
            self._vertical_bar.grid(row=0, column=1, sticky='ns')
        self._canvas.configure(yscrollcommand=self._vertical_bar.set)

        # create bottom scrollbar and connect to canvas X
        self._horizontal_bar = tk.Scrollbar(self, orient='horizontal', command=self._canvas.xview)
        if horizontal:
            self._horizontal_bar.grid(row=1, column=0, sticky='we')
        self._canvas.configure(xscrollcommand=self._horizontal_bar.set)

        # inner frame for widgets
        self.inner = tk.Frame(self._canvas, bg='red')
        self._window = self._canvas.create_window((0, 0), window=self.inner, anchor='nw')

        # autoresize inner frame
        self.columnconfigure(0, weight=1) # changed
        self.rowconfigure(0, weight=1) # changed

        # resize when configure changed
        self.inner.bind('<Configure>', self.resize)
        self._canvas.bind('<Configure>', self.frame_width)

    def frame_width(self, event):
        # resize inner frame to canvas size
        canvas_width = event.width
        self._canvas.itemconfig(self._window, width = canvas_width)

    def resize(self, event=None):
        self._canvas.configure(scrollregion=self._canvas.bbox('all'))

class Question:

    def __init__(self, parent, question, answer):
        self.parent = parent
        self.question = question
        self.answer = answer
        self.create_widgets()

    def get_input(self):
        value = self.entry.get()
        print('value:', value)
        if value == self.answer:
            print("Esatto. è " + self.answer)
            self.label['text'] = "Esatto"

    def create_widgets(self):
        self.labelframe = tk.LabelFrame(self.parent, text="Domanda:")
        self.labelframe.pack(fill="both", expand=True)

        self.label = tk.Label(self.labelframe, text=self.question)
        self.label.pack(expand=True, fill='both')

        self.entry = tk.Entry(self.labelframe)
        self.entry.pack()

        self.button = tk.Button(self.labelframe, text="Click", command=self.get_input)
        self.button.pack()

# --- main ---

root = tk.Tk()
root.title("Quiz")
root.geometry("400x300")

window = ScrolledFrame(root)
window.pack(expand=True, fill='both')

for i in range(10):
    one = randint(1, 10)
    two = randint(1, 10)
    Question(window.inner, "Quanto fa {} + {} ?".format(one, two), str(one + two))

root.mainloop()
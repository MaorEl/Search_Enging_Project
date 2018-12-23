import tkinter as tk
from random import randint
from tkinter import messagebox

import Controller


class ScrolledFrame(tk.Frame):

    def __init__(self, parent, vertical=True, horizontal=True):
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
        self.inner = tk.Frame(self._canvas)
        self._window = self._canvas.create_window((0, 0), window=self.inner, anchor='nw')

        # autoresize inner frame
        self.columnconfigure(0, weight=1) # changed
        self.rowconfigure(0, weight=1) # changed

        # resize when configure changed
        self.inner.bind('<Configure>', self.resize)
        #self._canvas.bind('<Configure>', self.frame_width)


    def frame_width(self, event):
        # resize inner frame to canvas size
        canvas_width = event.width
        self._canvas.itemconfig(self._window, width = canvas_width)

    def resize(self, event=None):
        self._canvas.configure(scrollregion=self._canvas.bbox('all'))

class Result:

    def __init__(self, parent, query_id, doc_rank_dic):
        self.parent = parent
        self.query_id = query_id
        self.doc_rank_dic = doc_rank_dic
        self.create_widgets()

    def create_widgets(self):
        self.labelframe = tk.LabelFrame(self.parent, text=self.query_id)
        self.labelframe.pack(fill="both", expand=True, side=tk.RIGHT)


        for doc in self.doc_rank_dic:
            res = tk.TOP
            label = Doc_Button(doc, self.labelframe)
            label.button.pack(side=res)

class Doc_Button:
    def __init__(self, doc, labelframe):
        self.doc = doc
        self.button = tk.Button(labelframe, text=doc, command= lambda : self.getYeshuyot(self.doc),height=2, width = 10, bg='yellow2')

    def getYeshuyot(self, doc):
        yeshuyot_dic = Controller.getTop5Yeshuyot(doc)
        message = 'Top 5 Yeshuyot of ' + doc + ':' + '\n'
        counter = 1
        for yeshut in yeshuyot_dic:
            message = message + str(counter) + ')  ' + str(yeshut) +'\n'
            counter += 1
        messagebox.showinfo("Don't Worry! I'm good message", message, parent = self.button)
        pass

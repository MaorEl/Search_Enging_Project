import collections
import threading
import tkinter
from tkinter import *
from tkinter import filedialog, ttk
from tkinter import messagebox

import os.path
from tkinter.ttk import Treeview
#todo: enable import
import Controller
from Helper import ScrolledFrame, Result


class GUI:

    def start_program(self):
        self.window.mainloop()

    def __init__(self):
        self.list_of_cities = None
        self.finished_program = False
        self.index_thread = None
        self.window = Tk()
        self.dictionary_in_main_memory = False
        self.queries_result = None

        #3 parts of main page:
        self.topFrame = Frame(self.window, width=700,height=100)
        self.centerFrame = Frame(self.window,width=700, height=100)
        self.centerFrameButtons = Frame(self.window,width=700, height=50)

        self.centerFrameQuery = Frame(self.window,width=700, height=100)
        self.centerFrameQueryButtons = Frame(self.window,width=700, height=50)

        self.bottomFrame = Frame(self.window,width=700,height=100)

        # top frame part:
        # photo for logo
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, "images\logo.png")
        photo = PhotoImage(file=path)
        w = Label(self.topFrame, image=photo)
        w.image = photo
        w.pack()
        #for sizes of buttons
        self.button_height=2
        self.button_width=13

        # browsing files section:
        self.corpus_path = StringVar()  # to keep result of browse button
        self.index_path = StringVar()  # to keep result of browse button
        self.first_row = 0
        self.distance_between_lines = self.first_row + 1
        # for i in range(first_row,distance_between_lines):
        #     centerFrame.rowconfigure(i, minsize=30)
        # # this code is for keeping empty lines

        self.label_corpus_path = Label(self.centerFrame, text="Please enter your corpus path:")
        self.textfield_corpus_path = Entry(self.centerFrame, textvariable=self.corpus_path, width=40)
        self.browse_button_corpus = Button(self.centerFrame, text="Browse", command=self.browse_folder_for_corpus_path, bg="SkyBlue1")
        self.textfield_index_path = Entry(self.centerFrame, textvariable=self.index_path, width=40)
        self.label_index_path = Label(self.centerFrame, text="Please enter a path to keep index files:")
        self.browse_button_index = Button(self.centerFrame, text="Browse", command=self.browse_folder_for_index_path, bg="SkyBlue1")

        # stemming option:
        self.state_of_stem = tkinter.IntVar()
        self.stemCheckBox = Checkbutton(self.centerFrame, text="Stemming", variable=self.state_of_stem)

        # languages option:
        self.lang_button = Button(self.centerFrame,text="Languages List", bg="deep sky blue", command=self.lang_command)
        # self.label_lang_list = Label(self.centerFrame, text="Languages List")
        # self.scrollbar = Scrollbar(self.centerFrame)
        # self.list_lang = Listbox(self.centerFrame, yscrollcommand=self.scrollbar.set)
        # self.scrollbar.config(command=self.list_lang.yview)


        # start Button and more buttons
        self.start_button = Button(self.centerFrameButtons, text="Start", command=self.start_button_command, width=self.button_width,height=self.button_height, bg="DeepSkyBlue3")
        self.show_dic_button = Button(self.centerFrameButtons, text="Show Dictionary", command=self.show_dic_command, width=self.button_width,height=self.button_height, bg="turquoise")
        self.load_dic_button = Button(self.centerFrameButtons, text="Load Index", command=self.load_dic_command, width=self.button_width,height=self.button_height, bg="turquoise")
        self.reset_button = Button(self.centerFrameButtons, text="Reset", command=self.reset_command, width=self.button_width, height=self.button_height, bg='firebrick2', state=DISABLED)
        self.reset_index_button = Button(self.centerFrameButtons, text="Reset Index", command=self.reset_index_command, width=self.button_width, height=self.button_height, bg='firebrick2', state=DISABLED)

        #query section
        self.query_text = StringVar()
        self.queries_file_path = StringVar() # to keep result of browse button
        self.label_query_text = Label(self.centerFrameQuery, text="Please enter your query:")
        self.textfield_query_text = Entry(self.centerFrameQuery, textvariable=self.query_text, width=40, state=DISABLED)
        self.textfield_queries_file_path = Entry(self.centerFrameQuery, textvariable=self.queries_file_path, width=40, state=DISABLED)
        self.label_queries_file_path = Label(self.centerFrameQuery, text="Please load your queries file:")
        self.browse_button_queries_file_path = Button(self.centerFrameQuery, text="Browse", command=self.browse_file,bg="SkyBlue1", state=DISABLED)

        # semantic care option:
        self.state_of_semantic = tkinter.IntVar()
        self.semanticCheckBox = Checkbutton(self.centerFrameQuery, text="Semantic?", variable=self.state_of_semantic, state=DISABLED)

        # Cities filter option:
        self.filter_cities_button = Button(self.centerFrameQuery, text="Filter Cities", bg="deep sky blue", command=self.filter_cities_command, state=DISABLED)

        #buttons for queries
        self.search = Button(self.centerFrameQueryButtons, text="Search", command=self.search_query, width=self.button_width,height=self.button_height, bg="maroon1", state=DISABLED)
        #self.save_resuults = Button(self.centerFrameButtons, text="Show Dictionary", command=self.show_dic_command, width=self.button_width,height=self.button_height, bg="turquoise")



        self.design_GUI()

    def design_GUI(self):
        self.window.title("Search Engine")
        self.window.geometry("700x500")
        self.window.resizable(False, False)
        self.topFrame.pack()
        self.centerFrame.pack(side=TOP)
        self.centerFrameButtons.pack(side=TOP)
        self.centerFrameQuery.pack(side=TOP)
        self.centerFrameQueryButtons.pack(side=TOP)
        self.bottomFrame.pack(side=BOTTOM)



        self.label_corpus_path.grid(row=self.first_row, column=0, sticky=W)
        self.textfield_corpus_path.grid(row=self.first_row, column=1, padx=10)
        self.browse_button_corpus.grid(row=self.first_row, column=2)
        self.centerFrame.rowconfigure(1, minsize=30)
        self.textfield_index_path.grid(row=self.distance_between_lines, column=1, padx=10)
        self.label_index_path.grid(row=self.distance_between_lines, column=0, sticky=W)
        self.browse_button_index.grid(row=self.distance_between_lines, column=2)
        self.stemCheckBox.grid(row=self.distance_between_lines + 1, column=1, sticky=W)

        #languages thing
        #self.centerFrame.rowconfigure(self.distance_between_lines + 2, minsize=30)
        self.lang_button.grid(row=self.distance_between_lines + 1, column=0)
        # self.label_lang_list.grid(row=self.distance_between_lines + 3, column=0)
        # self.scrollbar.grid(row=self.distance_between_lines + 3, column=1)

        #self.centerFrame.rowconfigure(self.distance_between_lines + 4, minsize=30)
        #self.centerFrame.rowconfigure(self.distance_between_lines + 5, minsize=30)

        #buttons:
        self.centerFrameButtons.rowconfigure(0, minsize=80)
        self.centerFrameButtons.columnconfigure(0, minsize=5)
        self.start_button.grid(row=0, column=2, padx=20)
        self.show_dic_button.grid(row=0, column=3, padx=20)
        self.load_dic_button.grid(row=0, column=1, padx=20)
        self.reset_button.grid(row=0, column=4, padx=20)
        self.reset_index_button.grid(row=0, column=0, padx=20)

        self.centerFrameButtons.rowconfigure(1, minsize=20)
        self.centerFrameButtons.rowconfigure(2, minsize=20)

        '''
        ***************************QUERY SECTION***************************
        '''
        self.label_query_text.grid(row=self.first_row, column=0, sticky=W)
        self.textfield_query_text.grid(row=self.first_row, column=1)
        self.centerFrameQuery.rowconfigure(1, minsize=30)
        self.textfield_queries_file_path.grid(row=self.first_row+1, column=1, padx=10)
        self.label_queries_file_path.grid(row=self.first_row+1, column=0, sticky=W)
        self.browse_button_queries_file_path.grid(row=self.first_row+1, column=2)
        self.semanticCheckBox.grid(row=self.first_row+2, column=1, sticky=W)

        # cities filter thing
        self.centerFrameQuery.rowconfigure(self.first_row+3, minsize=30)
        self.filter_cities_button.grid(row=self.first_row+ + 2, column=0)


        self.search.grid(row=0)

    #this function will run as another thread for indexing, so we will be able to show message at end, and make start button active again
    def start_command_wrap_in_thread(self, x, y, z):
        Controller.Main(x,y,z)
        self.start_button.configure(state=ACTIVE)
        self.textfield_corpus_path.config(state='normal')
        self.textfield_index_path.config(state='normal')
        self.browse_button_index.config(state=ACTIVE)
        self.browse_button_corpus.config(state=ACTIVE)
        self.show_dic_button.config(state=ACTIVE)
        self.load_dic_button.config(state=ACTIVE)
        self.dictionary_in_main_memory = True
        self.finished_program = True
        self.lang_button.config(state=ACTIVE)
        self.stemCheckBox.config(state=ACTIVE)
        self.change_states_of_queries(NORMAL)


    def browse_folder_for_corpus_path(self):
        # Allow user to select a directory and store it in global var
        # called folder_path
        filename = filedialog.askdirectory()
        self.window.update()
        self.corpus_path.set(filename)


    def browse_folder_for_index_path(self):
        # Allow user to select a directory and store it in global var
        # called folder_path
        filename = filedialog.askdirectory()
        self.window.update()
        self.index_path.set(filename)

    def start_button_command(self):
        if self.state_of_stem.get() == 1:
            bool_stem = True
        else:
            bool_stem = False
        if len(self.index_path.get()) == 0:
            messagebox.showwarning("Error", "Please choose path to your index")
        elif len(self.corpus_path.get()) == 0:
            messagebox.showwarning("Error", "Please choose path of your corpus")
        elif not os.path.exists(self.corpus_path.get()):
            messagebox.showwarning("Error", "Your corpus path is not exists. \n Please check it out")
        elif not os.path.exists(self.index_path.get()):
            messagebox.showwarning("Error", "Your index path is not exists. \n Please check it out")
        elif not os.path.exists(self.corpus_path.get() + '\stop_words.txt'):
            messagebox.showwarning("Error", "Your corpus is not having stop words file. \n Please check it out")


        else:
            self.finished_program=False
            Controller.stop=False
            self.show_dic_button.config(state=DISABLED)
            self.reset_button.config(state=ACTIVE)
            self.start_button.config(state=DISABLED)
            self.load_dic_button.config(state=DISABLED)
            self.browse_button_index.config(state=DISABLED)
            self.browse_button_corpus.config(state=DISABLED)
            self.stemCheckBox.config(state=DISABLED)
            self.lang_button.config(state=DISABLED)
            self.textfield_corpus_path.config(state='disabled')
            self.textfield_index_path.config(state='disabled')
          # indexingThread = _thread.start_new_thread(Controller.Main,(corpus_path.get(),index_path.get(),bool_stem)) # Run the indexing in a thread
            self.index_thread = threading.Thread(target=self.start_command_wrap_in_thread, args=(self.corpus_path.get(), self.index_path.get(), bool_stem))
            self.index_thread.start()

    def lang_command(self):
        if self.finished_program == False:
            messagebox.showwarning("Error", "first, start indexing your corpus. then you'll be able to see the languages")
        else:
            self.lang_window = Toplevel(self.window)
            self.lang_window.geometry("200x400")
            self.lang_window.title("Languages List")
            self.lang_window.resizable(False, False)
            tree = Treeview(self.lang_window, selectmode="extended", columns=("lang"))

            tree.pack(expand=YES, fill=BOTH)
            tree['show'] = 'headings'
            tree.heading("lang", text="Language")
            tree.column("lang", minwidth=180, width=180, stretch=NO)
            scrollbar = ttk.Scrollbar(self.lang_window, orient="vertical", command=tree.yview)
            scrollbar.place(x=180, y=0, height=400)
            tree.configure(yscrollcommand=scrollbar.set)
            odd = 'odd'
            even = 'even'
            list_of_langs = Controller.getLangList()
            sorted_list_of_langs = sorted(list_of_langs)
            i=0
            for x in sorted_list_of_langs:
                if i%2 == 0:
                    tag=odd
                else:
                    tag=even
                tree.insert('', 'end', values=(x), tags=(tag,))
                i = i + 1
            tree.tag_configure(odd, background='hot pink')
            tree.tag_configure(even, background='deep pink')
            


    #show dic button
    def show_dic_command(self):
        if self.dictionary_in_main_memory==False:
            messagebox.showwarning("Error", "first, load dictionary to your main memory.\ndon't look at me like this! just do it with the Load Dictionary button\nif you have some time, you can also start the program and after it will be finished, you will be able to show dictionary")
        else:
            text_of_waiting = Label(self.bottomFrame,text="Please Wait.. the dictionary will be shown in 10-20 seconds")
            text_of_waiting.grid(row=0,column=1)
            self.window.update()
            self.dictionaryWindow = Toplevel(self.window)
            self.dictionaryWindow.geometry("400x600")
            self.dictionaryWindow.title("Main Dictionary")
            self.dictionaryWindow.resizable(False, False)
            tree = Treeview(self.dictionaryWindow, selectmode="extended", columns=("term", "tf"))

            style = ttk.Style()
            style.configure("Treeview.Heading", background='lavender')
            tree.pack(expand=YES, fill=BOTH)
            tree['show'] = 'headings'
            tree.column("#0",minwidth=10, width=20,stretch=NO)
            tree.heading("term", text="Term")
            tree.column("term", minwidth=250, width=200 ,stretch=NO)
            tree.heading("tf", text="Frequency in corpus")
            tree.column("tf", minwidth=180, width=180, stretch=NO)

            scrollbar = ttk.Scrollbar(self.dictionaryWindow, orient="vertical", command=tree.yview)
            scrollbar.place(x=380,y=0 ,height=600)

            tree.configure(yscrollcommand=scrollbar.set)
            main_dictionary_pointer = Controller.getMainDictionaryFromIndexerToGUI()
            sorted_main_dictionary = dict(sorted(main_dictionary_pointer.items()))
            odd = 'odd'
            even = 'even'
            i=0
            for key in sorted_main_dictionary:
                term = key
                tf = str(sorted_main_dictionary[key].tf_in_corpus)
                if i%2 == 0:
                    tag=odd
                else:
                    tag=even
                tree.insert('','end', values=(term, tf), tags=(tag,))
                i=i+1
            tree.tag_configure(odd, background='gold')
            tree.tag_configure(even, background='deep sky blue')
            tree.pack()
            text_of_waiting.grid_remove()

    #load dictionary button
    def load_dic_command(self):
        if self.state_of_stem.get() == 1:
            bool_stem = True
        else:
            bool_stem = False
        stem_suffix = ''
        if bool_stem == True:
            stem_suffix = '_stem'
        Controller.setStemForPartB(bool_stem)

        main_dic_path =  self.index_path.get() + '/' + 'main_dictionary' + stem_suffix
        if not os.path.exists(main_dic_path):
            messagebox.showwarning("Error", "Please check there is dictionary in your index path. \n if there is, please check the Stemming check box mark")
        else:
            text_of_waiting = Label(self.bottomFrame, text="Wait.. the dictionary will be loaded to main memory in 3-5 seconds")
            text_of_waiting.grid(row=0, column=1)
            self.window.update()
            Controller.loadDictionariesFromDisk(bool_stem, self.index_path.get())
            self.dictionary_in_main_memory=True
            text_of_waiting.grid_remove()
            self.change_states_of_indexing(DISABLED)
            self.change_states_of_queries(NORMAL)

    def change_states_of_indexing(self, _STATE):
        self.textfield_index_path.config(state=_STATE)
        self.textfield_corpus_path.config(state=_STATE)
        self.browse_button_corpus.config(state=_STATE)
        self.browse_button_index.config(state=_STATE)
        self.stemCheckBox.config(state=_STATE)
        self.load_dic_button.config(state=_STATE)
        if _STATE == ACTIVE or _STATE == NORMAL:
            self.reset_index_button.config(state=DISABLED)
        else:
            self.reset_index_button.config(state=NORMAL)
    def change_states_of_queries(self, _STATE):
        self.textfield_queries_file_path.config(state=_STATE)
        self.textfield_query_text.config(state=_STATE)
        self.browse_button_queries_file_path.config(state=_STATE)
        self.semanticCheckBox.config(state=_STATE)
        self.filter_cities_button.config(state=_STATE)
        self.search.config(state=_STATE)

    #reset button
    def reset_command(self):
        if self.finished_program == False: #if program is still running
            Controller.reset_from_GUI()
            self.start_button.config(state=ACTIVE)
            self.load_dic_button.config(state=ACTIVE)
            self.browse_button_index.config(state=ACTIVE)
            self.browse_button_corpus.config(state=ACTIVE)
            self.stemCheckBox.config(state=ACTIVE)
            self.textfield_corpus_path.config(state='normal')
            self.textfield_index_path.config(state='normal')
        else: #if the program has been finished
            Controller.remove_index_files()
        messagebox.showinfo("Reset Info","your proccess will be reseted in 5-10 seconds! all index files will be removed now\nyour memory of program will now be cleared!")

    def browse_file(self):
        filename = filedialog.askopenfilename()
        self.window.update()
        self.queries_file_path.set(filename)

    def filter_cities_command(self):
        #todo: complete
        pass

    def search_query(self):
        if self.state_of_semantic.get() == 1:
            bool_semantic = True
        else:
            bool_semantic = False
        bool_text_query = len(self.query_text.get()) == 0
        bool_files_query = len(self.queries_file_path.get()) == 0
        if (bool_text_query and bool_files_query) or (not bool_text_query and not bool_files_query):
            messagebox.showwarning("Error", "Please enter a query OR choose file (not both) !")
        elif not bool_text_query:
            self.queries_result = Controller.controlQueriesOfFreeText(self.query_text.get(), self.list_of_cities)
            self.message_on_bottom("Please Wait.. the result will be shown in 15-30 seconds")
            self.open_result_window()
        elif not bool_files_query:
            if not os.path.exists(self.queries_file_path.get()):
                messagebox.showwarning("Error", "Your queries file path is not exists. \n Please check it out")
            else:
                self.queries_result = Controller.controlQueriesOfFile(self.queries_file_path.get(),self.list_of_cities)
                self.message_on_bottom("Please Wait.. the result will be shown in 15-30 seconds")
                self.open_result_window()

        Controller.reset("Queries")


    def reset_index_command(self):
        self.change_states_of_indexing(NORMAL)
        self.change_states_of_queries(DISABLED)
        pass

    def open_result_window(self):
        self.text_of_waiting.grid_remove()
        self.result_window = Toplevel(self.window)
        self.scrolled_frame = ScrolledFrame(self.result_window)
        size_of_window = len(self.queries_result) * 100
        if size_of_window < 300:
            size_of_window = str(300)
        else: size_of_window = str(size_of_window)

        self.result_window.geometry(size_of_window + "x600")
        self.result_window.title("Search Result")
        self.result_window.resizable(False,False)
        save_button_result = Button(self.result_window, text="Save Results", command=self.save_result_command, bg="SkyBlue1")
        save_button_result.pack(side = TOP)
        label_of_info = Label(self.result_window, text = "In order to see the top 5 yeshuyot in the document,\njust click on it ", width = 100)
        label_of_info.pack(side=TOP)



        self.scrolled_frame.pack(expand=True, fill='both')


        for query in self.queries_result:
            result = Result(self.scrolled_frame.inner, query, self.queries_result[query])

    def message_on_bottom(self, _text):
        self.text_of_waiting = Label(self.bottomFrame, text=_text)
        self.text_of_waiting.grid(row=0, column=1)
        self.window.update()

    def save_result_command(self):
        #todo: complete
        pass


def show_information_about_indexing(num_docs,num_terms,time):
    messagebox.showinfo("Indexing has been finished!",'Number of docs indexed: ' + str(num_docs) + '\nNumber of unique terms: ' + str(num_terms) + '\nTime for whole program: ' + str(time) + ' minutes')

#todo: after loading of dictionary lock the stem check box & text fields. button of "unlock or cleear" will unlock this
#todo: while user sending query enforce him to put corpus path (of stopword file)



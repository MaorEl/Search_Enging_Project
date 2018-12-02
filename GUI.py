import threading
import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

import os.path

import Controller

class GUI:

    def start_program(self):
        self.window.mainloop()

    def __init__(self):
        self.index_thread = None
        self.window = Tk()

        #3 parts of main page:
        self.topFrame = Frame(self.window, width=700,height=100)
        self.centerFrame = Frame(self.window,width=700, height=300)
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
        self.button_height=4
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
        self.browse_button_corpus = Button(self.centerFrame, text="Browse", command=self.browse_folder_for_corpus_path, bg="pink")
        self.textfield_index_path = Entry(self.centerFrame, textvariable=self.index_path, width=40)
        self.label_index_path = Label(self.centerFrame, text="Please enter a path to keep index files:")
        self.browse_button_index = Button(self.centerFrame, text="Browse", command=self.browse_folder_for_index_path, bg="SpringGreen2")

        # stemming option:
        self.state_of_stem = tkinter.IntVar()
        self.checkBox = Checkbutton(self.centerFrame, text="Stemming", variable=self.state_of_stem)

        # languages option:
        self.label_lang_list = Label(self.centerFrame, text="Choose Language:")
        self.scrollbar = Scrollbar(self.centerFrame)
        self.list_lang = Listbox(self.centerFrame, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.list_lang.yview)
        # todo: languages list box


        # start Button and more buttons
        self.start_button = Button(self.centerFrame, text="Start", command=self.start_button_command, width=self.button_width * 2,height=self.button_height, bg="blue")
        self.show_dic_button = Button(self.centerFrame, text="Show Dictionary", command=self.show_dic_command, width=self.button_width,height=self.button_height, bg="yellow", state=DISABLED)
        self.load_dic_button = Button(self.centerFrame, text="Load Dictionary", command=self.load_dic_command, width=self.button_width,height=self.button_height, bg="green")
        self.reset_button = Button(self.centerFrame, text="Reset", command=self.reset_command, width=self.button_width, height=self.button_height, bg='red', state=DISABLED)
        self.design_GUI()

    def design_GUI(self):
        self.window.title("Search Engine")
        self.window.geometry("700x500")
        self.window.resizable(False, False)
        self.topFrame.pack()
        self.centerFrame.pack(side=TOP)
        self.bottomFrame.pack(side=BOTTOM)



        self.label_corpus_path.grid(row=self.first_row, column=0, sticky=W)
        self.textfield_corpus_path.grid(row=self.first_row, column=1)
        self.browse_button_corpus.grid(row=self.first_row, column=2)
        self.centerFrame.rowconfigure(1, minsize=30)
        self.textfield_index_path.grid(row=self.distance_between_lines, column=1)
        self.label_index_path.grid(row=self.distance_between_lines, column=0, sticky=W)
        self.browse_button_index.grid(row=self.distance_between_lines, column=2)
        self.checkBox.grid(row=self.distance_between_lines + 1, column=1, sticky=W)

        #languages thing
        self.label_lang_list.grid(row=self.distance_between_lines + 3, column=0)
        self.scrollbar.grid(row=self.distance_between_lines + 3, column=1)

        self.centerFrame.rowconfigure(self.distance_between_lines + 4, minsize=30)
        self.centerFrame.rowconfigure(self.distance_between_lines + 5, minsize=30)

        #buttons:
        self.start_button.grid(row=self.distance_between_lines + 6, column=1)
        self.show_dic_button.grid(row=self.distance_between_lines + 6, column=2)
        self.load_dic_button.grid(row=self.distance_between_lines + 6, column=0)
        self.centerFrame.rowconfigure(self.distance_between_lines + 7, minsize=30)
        self.reset_button.grid(row=self.distance_between_lines + 8, column=1)


    def browse_folder_for_corpus_path(self):
        # Allow user to select a directory and store it in global var
        # called folder_path
        filename = filedialog.askdirectory()
        self.corpus_path.set(filename)


    def browse_folder_for_index_path(self):
        # Allow user to select a directory and store it in global var
        # called folder_path
        filename = filedialog.askdirectory()
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

        else:
            self.reset_button.config(state=ACTIVE)
            self.start_button.config(state=DISABLED)
            self.load_dic_button.config(state=DISABLED)
            self.browse_button_index(state=DISABLED)
            self.browse_button_corpus(state=DISABLED)
            self.textfield_corpus_path(state=DISABLED)
            self.textfield_index_path(state=DISABLED)
          # indexingThread = _thread.start_new_thread(Controller.Main,(corpus_path.get(),index_path.get(),bool_stem)) # Run the indexing in a thread
            self.index_thread = threading.Thread(target=Controller.Main, args=(self.corpus_path.get(),self.index_path.get(),bool_stem))
            self.index_thread.start()


    #show dic button
    def show_dic_command(self):
        pass

    #load dictionary button
    def load_dic_command(self):
        if self.state_of_stem.get() == 1:
            bool_stem = True
        else:
            bool_stem = False
        stem_suffix = ''
        if bool_stem == True:
            stem_suffix = '_stem'
        main_dic_path =  self.index_path.get() + '/' + 'main_dictionary' + stem_suffix
        if not os.path.exists(main_dic_path):
            messagebox.showwarning("Error", "Please check there is dictionary in your index path. \n if there is, please check the Stemming check box mark")
        else:
            Controller.loadDictionaryFromDisk(bool_stem,  self.index_path.get())


    #reset button
    def reset_command(self):
        Controller.reset_from_GUI()
        self.start_button.config(state=ACTIVE)
        self.load_dic_button.config(state=ACTIVE)
        self.browse_button_index(state=ACTIVE)
        self.browse_button_corpus(state=ACTIVE)
        self.browse_button_index(state=ACTIVE)
        self.browse_button_corpus(state=ACTIVE)
        self.textfield_corpus_path(state=ACTIVE)
        self.textfield_index_path(state=ACTIVE)

        pass






#list_lang.grid(row=distance_between_lines+3, column=1)



# label = Label(topFrame,text="Please enter path of corpus:")
# label.grid(row=2,column=7)
# text_field1 = Entry(bottomFrame)
# button1 = Button(bottomFrame, text="button1",fg="red")
# button1.grid(row=0,sticky=W)
# text_field1.grid(row=1,sticky=W)
# button2 = Button(bottomFrame, text="button2")
# button2.grid(row=1,column=1,sticky=W)
#
# checkBox = Checkbutton(bottomFrame,text="I agree")
# checkBox.grid(column=0,columnspan=2)


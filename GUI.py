import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

import os.path

import Controller

window = Tk()
window.geometry("700x500")
window.resizable(False,False)
topFrame = Frame(window, width=700,height=100)
topFrame.config()
topFrame.pack()
centerFrame = Frame(window,width=700, height=300)
centerFrame.pack(side=TOP)
bottomFrame = Frame(window,width=700,height=100)
bottomFrame.pack(side=BOTTOM)

button_height=4
button_width=13

window.title("Search Engine")

#top frame part:

#title:
# label_title = Label(topFrame,text="Search Engine")
# label_title2 = Label(topFrame,text="by Maor Elfassy & Anael Gorfinkel")

#photo for logo
my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "images/logo.png")
photo = PhotoImage(file=path)
w = Label(topFrame,image=photo)
w.pack()

#center:
def browse_folder_for_corpus_path():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global corpus_path
    filename = filedialog.askdirectory()
    corpus_path.set(filename)


def browse_folder_for_index_path():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global index_path
    filename = filedialog.askdirectory()
    index_path.set(filename)

def start_button_command():
    global state_of_stem, corpus_path, index_path,reset_button,start_button
    if state_of_stem.get() == 1:
        bool_stem = True
    else:
        bool_stem = False
    if len(index_path.get()) == 0:
        messagebox.showwarning("Error", "Please choose path to your index")
    elif len(corpus_path.get()) == 0:
        messagebox.showwarning("Error", "Please choose path of your corpus")
    reset_button.config(state=ACTIVE)
    start_button.config(state=DISABLED)


#browsing files section:
corpus_path = StringVar() #to keep result of browse button
index_path = StringVar() #to keep result of browse button
first_row = 0
distance_between_lines= first_row + 1
# for i in range(first_row,distance_between_lines):
#     centerFrame.rowconfigure(i, minsize=30)
# # this code is for keeping empty lines

label_corpus_path = Label(centerFrame,text="Please enter your corpus path:")
label_corpus_path.grid(row=first_row,column=0,sticky=W)
textfield_corpus_path = Entry(centerFrame,textvariable=corpus_path, width=40)
textfield_corpus_path.grid(row=first_row,column=1)
browse_button_corpus = Button(centerFrame,text="Browse", command=browse_folder_for_corpus_path, bg="pink")
browse_button_corpus.grid(row=first_row,column=2)
centerFrame.rowconfigure(1, minsize=30)
textfield_index_path = Entry(centerFrame,textvariable=index_path,width=40)
textfield_index_path.grid(row=distance_between_lines,column=1)
label_index_path = Label(centerFrame,text="Please enter a path to keep index files:")
label_index_path.grid(row=distance_between_lines,column=0,sticky=W)
browse_button_index = Button(centerFrame, text="Browse", command=browse_folder_for_index_path, bg="SpringGreen2")
browse_button_index.grid(row=distance_between_lines,column=2)

#stemming option:
state_of_stem = tkinter.IntVar()
checkBox = Checkbutton(centerFrame,text="Stemming",variable=state_of_stem)
checkBox.grid(row=distance_between_lines+1,column=1, sticky=W)

#languages option:
label_lang_list = Label(centerFrame,text="Choose Language:")
label_lang_list.grid(row=distance_between_lines+3,column=0)
scrollbar = Scrollbar(centerFrame)
scrollbar.grid(row=distance_between_lines+3, column=1)
centerFrame.rowconfigure(distance_between_lines+4, minsize=30)
centerFrame.rowconfigure(distance_between_lines+5, minsize=30)




list_lang = Listbox(centerFrame,yscrollcommand = scrollbar.set)
scrollbar.config(command=list_lang.yview)

#todo: languages list box

#start Button
start_button = Button(centerFrame,text="Start",command = start_button_command,width = button_width*2, height=button_height, bg="blue")
start_button.grid(row=distance_between_lines+6,column=1)

#show dic button
def show_dic_command():
    pass


show_dic_button = Button(centerFrame,text="Show Dictionary", command=show_dic_command,width = button_width, height=button_height, bg="yellow",state=DISABLED)
show_dic_button.grid(row=distance_between_lines+6, column=2)

#load dictionary button
def load_dic_command():
    pass


load_dic_button = Button(centerFrame,text="Load Dictionary", command=load_dic_command,width = button_width, height=button_height,bg="green")
load_dic_button.grid(row=distance_between_lines+6, column=0)

#reset button
def reset_command():
    global start_button
    print("Stop Indexing :(")
    start_button.config(state=ACTIVE)
    Controller.reset()

    pass

centerFrame.rowconfigure(distance_between_lines+7, minsize=30)


reset_button = Button(centerFrame,text="Reset", command=reset_command, width = button_width, height=button_height,bg='red', state=DISABLED)
reset_button.grid(row=distance_between_lines+8, column=1)


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


window.mainloop()

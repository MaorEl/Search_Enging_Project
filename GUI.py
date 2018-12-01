from tkinter import *
from tkinter import filedialog
import os.path

window = Tk()
window.geometry("700x700")
window.resizable(False,False)
topFrame = Frame(window, width=700,height=100)
topFrame.pack()
centerFrame = Frame(window,width=700, height=300)
centerFrame.pack(side=TOP)
bottomFrame = Frame(window,width=700,height=300)
bottomFrame.pack(side=BOTTOM)


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



#browsing files section:
corpus_path = StringVar() #to keep result of browse button
index_path = StringVar() #to keep result of browse button
first_row = 0
distance_between_lines= first_row + 1
# for i in range(first_row,distance_between_lines):
#     centerFrame.rowconfigure(i, minsize=30)
#this code is for keeping empty lines

label_corpus_path = Label(centerFrame,text="Please enter your corpus path:")
label_corpus_path.grid(row=first_row,column=0,sticky=W)
textfield_corpus_path = Entry(centerFrame,textvariable=corpus_path, width=40)
textfield_corpus_path.grid(row=first_row,column=1)
browse_button_corpus = Button(centerFrame,text="Browse", command=browse_folder_for_corpus_path)
browse_button_corpus.grid(row=first_row,column=2)

textfield_index_path = Entry(centerFrame,textvariable=index_path,width=40)
textfield_index_path.grid(row=distance_between_lines,column=1)
label_index_path = Label(centerFrame,text="Please enter a path to keep index files:")
label_index_path.grid(row=distance_between_lines,column=0,sticky=W)
browse_button_index = Button(centerFrame, text="Browse", command=browse_folder_for_index_path)
browse_button_index.grid(row=distance_between_lines,column=2)

#stemming option:
checkBox = Checkbutton(centerFrame,text="Stemming")
checkBox.grid(row=distance_between_lines+1,column=1, sticky=W)

#languages option:
label_lang_list = Label(centerFrame,text="Choose Language:")
label_lang_list.grid(row=distance_between_lines+3,column=0)
scrollbar = Scrollbar(centerFrame)
scrollbar.grid(row=distance_between_lines+3, column=1)


list_lang = Listbox(centerFrame,yscrollcommand = scrollbar.set)
scrollbar.config(command=list_lang.yview)

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
def start_button_command():
    global checkBox, textfield_corpus_path, textfield_index_path
    if checkBox.variable==1:
        bool_stem = True
    else:
        bool_stem= False

window.mainloop()


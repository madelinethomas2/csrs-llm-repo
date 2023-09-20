# -*- coding: utf-8 -*-

'''
Make sure you have tkinter installed
Tkinter should be preinstalled on python 3.x
python -m pip install pysimplegui (on windows)
This installs PySimpleGUI, which comes wrapped with Tkinter
'''

from tkinter import *
import tkinter as tk
import sandbox
import re

# I just copied this from another project and edited it
# I'll optimize it a bit later, for now this is just a protoype
# (Tkinter in general is buggy+ugly enough that we should only use it for prototyping anyway)


#Initialize a tkinter window, set title and size
#Open config.txt and get preset options
win= Tk()
win.winfo_toplevel().title("[repo_name] GUI")
win.geometry("700x325")
prevsetsf = open("./config.txt", "r")
prevsets = prevsetsf.readlines()
prevsetsf.close()
print(prevsets)

chosen_configs = []

def display_text():
    
    '''
    Debug code
    Writes "Plotting..." to the GUI but doesn't plot anything
    '''
    
    string= "Plotting..."
    debug_label.configure(text=string)
    debug_label.grid(row=10, column=1)
    
def update_strings(label_list: list):
    
    '''
    Updates the 4 main string fields in the gui
    Enter the string values as a list
    '''
    
    string1 = label_list[0]
    print(string1)
    status_label1.configure(text=string1)
    status_label1.grid(row=3, column=1)

    string2 = label_list[1]
    print(string2)
    status_label2.configure(text=string2)
    status_label2.grid(row=4, column=1)

    string3 = label_list[2]
    print(string3)
    status_label3.configure(text=string3)
    status_label3.grid(row=5, column=1)

    string4 = label_list[3]
    print(string4)
    status_label4.configure(text=string4)
    status_label4.grid(row=6, column=1)
    
def start_gui():
    
    '''
    Adds all inputs to chosenconfigs
    config.txt is replaced with the inputs
    Runs the LLM on the file specified in the entry field
    '''
    
    # Writes current entry data to config.txt
    # If more entry fields are added, add their get functions to the chosen_configs list
    global cwd_entry
    chosen_configs = [cwd_entry.get()]
    for inp_option in chosen_configs:
        if '\n' not in inp_option:
            chosen_configs[chosen_configs.index(inp_option)] = inp_option + "\n"
    prevsetsw = open("./config.txt", "w")
    prevsetsw.writelines(chosen_configs)
    prevsetsw.close()
    print(chosen_configs)
    
    update_strings(["Analyzing proposal...", " ", " ", " "])
    
    data = sandbox.load_word_docx(cwd_entry.get())
    
    update_strings(["Analysis Complete."] + fake_analysis(data))
    
    '''
    string= "Parsing text..."
    print(string)
    status_label.configure(text=string)
    status_label.grid(row=3, column=1)
    
    string2= "Complete."
    print(string2)
    status_label.configure(text=string2)
    status_label.grid(row=3, column=1)
    
    string3= "hello i are a bad sentence"
    print(string3)
    status_label2.configure(text=string3)
    status_label2.grid(row=4, column=1)
    
    string4= "Grammar issue at char 8"
    print(string4)
    statuslab3.configure(text=string4)
    statuslab3.grid(row=5, column=1)
    
    string5= "'are' -> 'am'"
    print(string5)
    statuslab4.configure(text=string5)
    statuslab4.grid(row=6, column=1)
    '''
    
def fake_analysis(data: str) -> list:
    
    # Faking an LLM finding a grammar error
    
    bad_section = re.findall(r"are", data)
    
    return_strings = ["'%s'" % bad_section,
                      "Grammar Issue at char 5",
                      " 'are' -> 'is'"]
    
    return return_strings

def reset_gui():
    
    update_strings(["Reloading...", " ", " ", " "])
    update_strings(["Enter the location to the proposal.", " ", " ", " "])
    
    '''
    string= "Reloading..."
    print(string)
    statuslab.configure(text=string)
    statuslab.grid(row=3, column=1)
    
    string= "Enter the location to the proposal."
    print(string)
    statuslab.configure(text=string)
    statuslab.grid(row=3, column=1)

    string3= " "
    print(string3)
    statuslab2.configure(text=string3)
    statuslab2.grid(row=4, column=1)

    string4= " "
    print(string4)
    statuslab3.configure(text=string4)
    statuslab3.grid(row=5, column=1)

    string5= " "
    print(string5)
    statuslab4.configure(text=string5)
    statuslab4.grid(row=6, column=1)
    '''
    
'''
Label and entry widgets
Preset inputs are taken from config.txt
'''

debug_label=Label(win, text="", font=("Consolas 14"))
status_label1=Label(win, text="Enter the location to the proposal.", font=("Consolas 14"))
status_label2=Label(win, text=" ", font=("Consolas 14"))
status_label3=Label(win, text=" ", font=("Consolas 14"))
status_label4=Label(win, text=" ", font=("Consolas 14"))
status_label1.grid(row=3, column=1)
status_label2.grid(row=4, column=1)
status_label3.grid(row=5, column=1)
status_label4.grid(row=6, column=1)

cwd_label = tk.Label(win, text="File location: ")
cwd_entry = Entry(win, width= 40)
cwd_entry.insert(0, prevsets[0])
cwd_entry.focus_set()

runbutton1 = tk.Button(win, text= "Analyze Proposal",width= 20, command=start_gui)
runbutton2 = tk.Button(win, text= "Reset GUI",width= 20, command=reset_gui)

'''
Grid settings for the widgets
'''

cwd_label.grid(row=1, column=0)
cwd_entry.grid(row=1, column=1)
runbutton1.grid(row=7, column=1)
runbutton2.grid(row=7, column=0)

win.mainloop()

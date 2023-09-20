# -*- coding: utf-8 -*-

'''
Make sure you have tkinter installed
Tkinter should be preinstalled on python 3.x
python -m pip install pysimplegui (on windows)
This installs PySimpleGUI, which comes wrapped with Tkinter
'''

from tkinter import *
import tkinter as tk

# I just copied this from another project and edited it
# I'll optimize it a bit later, for now this is just a protoype
# Also doesn't work as intended right now, I'll debug later
# (Tkinter in general is buggy enough that we should only use it for prototyping anyway)

'''
Initialize a tkinter window, set title and size
Open config.txt and get preset options
'''

win= Tk()
win.winfo_toplevel().title("[repo_name] GUI")
win.geometry("700x325")

prevsetsf = open("./config.txt", "r")
prevsets = prevsetsf.readlines()
prevsetsf.close()
print(prevsets)

chosenconfigs = []

def display_text():
    
    '''
    Debug code
    Writes "Plotting..." to the GUI but doesn't plot anything
    '''
    
    string= "Plotting..."
    debuglab.configure(text=string)
    debuglab.grid(row=10, column=1)
    
def start_gui():
    
    '''
    Adds all inputs to chosenconfigs
    config.txt is replaced with the inputs
    Plots the FFT using inputted settings
    To plot another file within the same graph, just change your inputs as needed and click the button again
    To plot a brand new graph, restart the GUI
    '''
    
    global cwdent
    
    chosenconfigs = [cwdent.get()]
    for inpoption in chosenconfigs:
        if '\n' not in inpoption:
            chosenconfigs[chosenconfigs.index(inpoption)] = inpoption + "\n"
    prevsetsw = open("./config.txt", "w")
    prevsetsw.writelines(chosenconfigs)
    prevsetsw.close()
    print(chosenconfigs)
    
    string= "Parsing text..."
    print(string)
    statuslab.configure(text=string)
    statuslab.grid(row=3, column=1)
    
    string2= "Complete."
    print(string2)
    statuslab.configure(text=string2)
    statuslab.grid(row=3, column=1)
    
    string3= "hello i are a bad sentence"
    print(string3)
    statuslab2.configure(text=string3)
    statuslab2.grid(row=4, column=1)
    
    string4= "Grammar issue at char 8"
    print(string4)
    statuslab3.configure(text=string4)
    statuslab3.grid(row=5, column=1)
    
    string5= "'are' -> 'am'"
    print(string5)
    statuslab4.configure(text=string5)
    statuslab4.grid(row=6, column=1)

def reset_gui():
    
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
Label and entry widgets
Preset inputs are taken from config.txt
'''

debuglab=Label(win, text="", font=("Consolas 14"))
statuslab=Label(win, text="Enter the location to the proposal.", font=("Consolas 14"))
statuslab2=Label(win, text=" ", font=("Consolas 14"))
statuslab3=Label(win, text=" ", font=("Consolas 14"))
statuslab4=Label(win, text=" ", font=("Consolas 14"))
statuslab.grid(row=3, column=1)
statuslab2.grid(row=4, column=1)
statuslab3.grid(row=5, column=1)
statuslab4.grid(row=6, column=1)

cwdlab = tk.Label(win, text="File location: ")
cwdent = Entry(win, width= 40)
cwdent.insert(0, prevsets[0])
cwdent.focus_set()

runbutton1 = tk.Button(win, text= "Plot",width= 20, command=start_gui)
runbutton2 = tk.Button(win, text= "Reset Plot",width= 20, command=reset_gui)

'''
Grid settings for the widgets
'''

cwdlab.grid(row=1, column=0)
cwdent.grid(row=1, column=1)
runbutton1.grid(row=7, column=1)
runbutton2.grid(row=7, column=0)

win.mainloop()

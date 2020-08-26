import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, LabelFrame
import test2
import sys
import os
import subprocess

def printtext(e):
    test2.e = e

class GUI:
    def __init__(self, master):
        self.master = master 
        master.title("XRR/XRD Data Reduction")
        tabControl = ttk.Notebook(root)
        xrr_tab = ttk.Frame(tabControl)
        xrd_tab = ttk.Frame(tabControl)
        tabControl.add(xrr_tab, text='XRR')
        tabControl.add(xrd_tab, text='XRD')
        tabControl.pack(expand=1, fill="both")
        self.label = ttk.Label(xrr_tab, text="test baybeee")
        self.label.pack()
        self.button = ttk.Button(text = "Select zscan file",command = self.fileDialogZscan)
        self.button.pack()
        self.button = ttk.Button(text = "Select specular file",command = self.fileDialogSpec)
        self.button.pack()
        self.button = ttk.Button(text = "Select background file",command = self.fileDialogBkg)
        self.button.pack()
        self.button = ttk.Button(text = "Run",command = self.run)
        self.button.pack()

    def fileDialogZscan(self):
        global zscan
        zscan = filedialog.askopenfile(initialdir = "/", title="Select zscan file", filetypes = (("dat files","*.dat"),("text files","*.txt"), ("all files","*.*")), mode="r")
        #printtext(zscan)
        #test2.zscan = zscan

    def fileDialogSpec(self):
        global spec
        #subprocess.run('python test3.py')
        #os.system('python test3.py')
        spec= filedialog.askopenfile(initialdir = "/", title="Select specular file", filetypes = (("dat files","*.dat"),("text files","*.txt"), ("all files","*.*")), mode="r")
        #print(self.spec)

    def fileDialogBkg(self):
        global bkg
        bkg= filedialog.askopenfile(initialdir = "/", title="Select background file", filetypes = (("dat files","*.dat"),("text files","*.txt"), ("all files","*.*")), mode="r")

    def run(self):
        zscan_data, spec_data, bkg_data = test2.init_data(zscan, spec, bkg)
        print(zscan_data)

root = tk.Tk()
gui = GUI(root)
root.mainloop()

class xrr_tab:
    def __init__(self, master):
        self.master = master 
        self.frame = tk.Frame(self.master)
        #self.minsize(640, 400)
        
        self.labelFrame = ttk.LabelFrame(self, text = "Open File")
        self.labelFrame.grid(column = 0, row = 1, padx = 20, pady = 20)
        self.button = ttk.Button(self.labelFrame, text = "Browse A File",command = self.fileDialog)
        self.button.grid(column = 1, row = 1)
 
 
    def fileDialog(self):
 
        self.zscan = filedialog.askopenfile(initialdir = "/", title="Select zscan file", filetypes = (("dat files","*.dat"),("text files","*.txt"), ("all files","*.*")))
        self.label = ttk.Label(self.labelFrame, text = "")
        self.label.grid(column = 1, row = 2)
        self.label.configure(text = self.zscan)
 
def main():
    root = tk.Tk()
    root.title("XRR/XRD Data Reduction")
    tabControl = ttk.Notebook(root)
    xrr_tab = ttk.Frame(tabControl)
    xrd_tab = ttk.Frame(tabControl)
    tabControl.add(xrr_tab, text='XRR')
    tabControl.add(xrd_tab, text='XRD')
    tabControl.pack(expand=1, fill="both")
    root.mainloop()

main()

#parent window
root = tk.Tk()
root.title("XRR/XRD Data Reduction")
tabControl = ttk.Notebook(root)
xrr_tab = ttk.Frame(tabControl)
xrd_tab = ttk.Frame(tabControl)
tabControl.add(xrr_tab, text='XRR')
tabControl.add(xrd_tab, text='XRD')
tabControl.pack(expand=1, fill="both")
#use a button or drop down so people can change if they choose the wrong one
#xrr_tab.zscan = filedialog.askopenfile(initialdir = "/", title="Select zscan file", filetypes = (("dat files","*.dat"),("text files","*.txt"), ("all files","*.*")))
#xrr_tab.specular = filedialog.askopenfile(initialdir = "/", title="Select specular file", filetypes = (("dat files","*.dat"),("text files","*.txt"), ("all files","*.*")))
#xrr_tab.bkg = filedialog.askopenfile(initialdir = "/", title="Select background file", filetypes = (("dat files","*.dat"),("text files","*.txt"), ("all files","*.*")))
#root.mainloop()
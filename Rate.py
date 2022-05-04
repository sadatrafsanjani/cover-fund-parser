from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import Parser

        
class Rate:

    def __init__(self, master):
        
        self.master = master
        self.master.wm_iconbitmap('resources/img/logo.ico')
        self.master.resizable(False, False)
        self.master.geometry("300x200")
        
        self.content = ttk.Frame(master)
        self.content.pack()
        
        ttk.Label(self.content, text = 'Exchange Rate:').grid(row=0, column=0, padx=10, pady=10)
        self.entry = Entry(self.content)
        self.entry.grid(row=0, column=1)
        ttk.Button(self.content, text = 'Load Step1', command = self.step1).grid(row=1, column=0, padx=10, pady=10)
        ttk.Button(self.content, text = 'Load Cover Fund', command = self.cover).grid(row=1, column=1, padx=10, pady=10)
        ttk.Button(self.content, text = 'Go', command = self.go).grid(row=2, column=0, padx=10, pady=10)
    
        
    def step1(self):
        
        self.file1 = askopenfilename(filetypes=[("Excel files", "*.xls")])
        
    def cover(self):
        
        self.file2 = askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        
        
    def go(self):
        
        rate = self.entry.get()
        
        if((self.file1 == '') or (self.file2 == '') or (rate == '')):
            messagebox.showerror("Error!", "Please load the Step-1 File")
        else:
            self.window = Toplevel(self.master)
            rate = float(rate)
            Parser.Parser(self.window, rate, self.file1, self.file2)
            self.master.withdraw()
        
    
        
        
    
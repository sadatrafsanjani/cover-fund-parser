from tkinter import *
from tkinter import ttk
from pandastable import Table
import pandas as pd
import Code

class Branch:
    
    def __init__(self, master):
        
        self.master = master
        self.master.wm_iconbitmap('resources/img/logo.ico')
        
        #Titlebar
        self.header = ttk.Frame(master)
        self.header.pack(fill=X)
        ttk.Label(self.header, text = 'Branch Codes', font = ('Arial', 16)).pack(padx=10, pady=10)
        
        #Main Content
        self.body = ttk.Frame(master)
        self.body.pack(fill=BOTH, expand=1)
        
        column = ['Branch Code', 'Branch Name']
        data = Code.branchDetails()
        df = pd.DataFrame(data, columns=column)
       
        self.table = Table(self.body, dataframe=df, showtoolbar=False, showstatusbar=False)
        self.table.show()
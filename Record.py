from tkinter import *
from tkinter import ttk
from pandastable import Table
from tkinter import messagebox
import pandas as pd
import os
import Database

class Record:
    
    def __init__(self, master):
        
        self.master = master
        
        self.header = ttk.Frame(master)
        self.header.pack(fill=X)
        ttk.Label(self.header, text = 'Database Record', font = ('Arial', 16)).pack(padx=10, pady=10)
        
        self.content = ttk.Frame(master)
        self.content.pack(fill=BOTH, expand=1)
        
        column = ['Ref No.', 'Ref Date', 'Rem_name', 'Ben_name', 'Ben_bank', 'Ben_br_name', 
          'Ben_br_code', 'Pay_mode', 'Ben_ac_num', 'FC_amount', 'Exch_rate', 'FC_cur', 
          'Remit_amt', 'Pay_cur', 'Valu_dat', 'RMb_bank', 'Remarks']
        
          
        self.data = Database.select_all()
        self.df = pd.DataFrame(self.data, columns=column)
        Table(self.content, dataframe=self.df, showtoolbar=False, showstatusbar=False).show()
        
        self.footer = ttk.Frame(master)
        self.footer.pack()
        ttk.Button(self.footer, text = 'Print', command = self.printer).grid(row=0, column=0, padx=5, pady=5)
        
        
    def printer(self):
        
        if(not self.df.empty):
        
            writer = pd.ExcelWriter('all-record.xlsx', engine='xlsxwriter')
            self.df.to_excel(writer, sheet_name='Sheet1')
            writer.save()
            
            os.startfile("all-record.xlsx", "print")
            messagebox.showinfo("Print", "Printing In Progress....")
        else:
            messagebox.showerror("Warning", "Empty Database")
       
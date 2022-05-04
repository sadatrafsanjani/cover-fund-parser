from tkinter import *
from tkinter import ttk
from pandastable import Table
from tkinter import messagebox
import pandas as pd
import os
import Engine
import Database
import Record
import Login
import Code
import Branch

class Parser:
    
    def __init__(self, master, rate, step1, cover):
        
        self.master = master
        self.master.wm_iconbitmap('resources/img/logo.ico')
        
        Engine.setFileName(rate, step1, cover)
        Engine.matchBranch()
        
        #Titlebar
        self.header = ttk.Frame(master)
        self.header.pack(fill=X)
        ttk.Label(self.header, text = 'MT 103 Parsing System', font = ('Arial', 16)).pack(padx=10, pady=10)
        
        #Branch Code Queue
        self.branch = ttk.Frame(master)
        self.branch.pack(fill=X, expand=1)
        self.branch.grid_columnconfigure(1, weight=1)
        
        self.left = ttk.Frame(self.branch)
        self.left.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        self.right = ttk.Frame(self.branch)
        self.right.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        #Main Content
        self.body = ttk.Frame(master)
        self.body.pack(fill=X)

        self.loadData()        
        
        #Menu Buttons
        self.footer = ttk.Frame(master)
        self.footer.pack()
        
        ttk.Button(self.footer, text = 'Save References', command = self.saveRef).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(self.footer, text = 'Change', command = self.change).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.footer, text = 'Generate TXT', command = self.processTXT).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(self.footer, text = 'Save to DB', command = self.saveToDba).grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(self.footer, text = 'View Database', command = self.database).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(self.footer, text = 'Branch List', command = self.branchCode).grid(row=0, column=5, padx=5, pady=5)
        ttk.Button(self.footer, text = 'Print', command = self.printer).grid(row=0, column=6, padx=5, pady=5)
     
    
    def saveRef(self):
        
        counter = []
        
        for i in range(len(self.df3)):
            t = []
            for j in range(len(self.df3.iloc[0])):
                t.append(str(self.df3.iloc[i][j]))
                
            k = Database.insert_references(t)
            counter.append(k)
            
        message = str(len(counter)) + " rows inserted successfully!"
        messagebox.showinfo("Successful", message)
        
    
    def loadData(self):
            
        self.df1, self.df2, self.df3 = Engine.getData()
        
        #Missmatched Table
        self.table1 = Table(self.right, dataframe=self.df1, showtoolbar=False, showstatusbar=False)
        self.table1.show()
        
        #Matched Table
        self.table2 = Table(self.body, dataframe=self.df2, showtoolbar=False, showstatusbar=False)
        self.table2.show()
        
        #Missmatched Reference
        self.table3 = Table(self.left, dataframe=self.df3, showtoolbar=False, showstatusbar=False)
        self.table3.show()
        
        self.generateTable()
        
        
    def generateTable(self):
        
        self.steps = []
        
        for i in range(len(self.df2)):
        
            t = ''
            
            for j in range(len(self.df2.iloc[0])):
                
                data = str(self.df2.iloc[i][j]).strip()
                t += data + '|'
            
            self.steps.append(t)
        
        
        
    def processTXT(self):
        
        if(not self.steps):
            messagebox.showerror("Warning", "Empty List")
        else:
        
            file = open('steps.txt', 'w')
            
            header = "Ref_no|Ref_date|Rem_name|Ben_name|Ben_bank|Ben_br_name|Ben_br_code|"
            header += "Pay_mode|Ben_ac_num|FC_amount|Exch_rate|FC_Cur|Remit_amt|Pay_cur|"
            header += "Valu_dat|RMb_bank|Remarks\n"
            file.write(header)
            
            for i in range(len(self.steps)):
                
                t = self.steps[i] + '\n'
                file.write(t)
            
            file.close()
            
            messagebox.showinfo("Successful", "Steps Saved Successfully!")
        
        
    def saveToDba(self):
        
        counter = []
        
        for i in range(len(self.df2)):
            t = []
            for j in range(len(self.df2.iloc[0])):
                t.append(str(self.df2.iloc[i][j]))
                
            k = Database.insert_step(t)
            counter.append(k)
            
            
        message = str(len(counter)) + " rows inserted successfully!"
        messagebox.showinfo("Successful", message)
            
        
    def database(self):
        
        self.window = Toplevel(self.master)
        Record.Record(self.window)
        
        
    def check(self):
        
        missmatch = self.df1['Ben_br_code'].values.tolist()
        missmatch = list(map(str, missmatch))
        
        codes = Code.branchCode()
        self.flags = [False] * len(missmatch)
        
        for i in range(len(missmatch)):
            
            if(missmatch[i] in codes):
                self.flags[i] = True

        if(self.flags.count(False) > 0):
            return True
        else:
            return False
            
      
    def change(self):
        
        if(self.check()):
            errors = self.flags.count(False)
            message = "Total " + str(errors) + " errors found!"
            messagebox.showerror("Error!", message)
        else:
            frames = [self.df1, self.df2]
            
            self.df1 = pd.DataFrame([])
            self.df2 = pd.concat(frames)
            
            self.table1 = Table(self.right, dataframe=self.df1, showtoolbar=False, showstatusbar=False)
            self.table1.show()
            self.table1.redraw()
            
            self.table2 = Table(self.body, dataframe=self.df2, showtoolbar=False, showstatusbar=False)
            self.table2.show()
            self.table2.redraw()
            
            self.generateTable()
            
    def branchCode(self):
        
        self.window = Toplevel(self.master)
        Branch.Branch(self.window)
        
        
    def printer(self):
        
        if(not self.df2.empty):
        
            writer = pd.ExcelWriter('correted-list.xlsx', engine='xlsxwriter')
            self.df2.to_excel(writer, sheet_name='Sheet1')
            writer.save()
            
            os.startfile("correted-list.xlsx", "print")
            messagebox.showinfo("Print", "Printing In Progress....")
        else:
            messagebox.showerror("Warning", "Empty List")

        
def main():
    
    root = Tk()
    Login.Login(root)
    root.geometry("500x480")
    root.title('Parser')
    root.wm_iconbitmap('resources/img/logo.ico')
    root.mainloop()
    

if __name__ == "__main__":
    main()
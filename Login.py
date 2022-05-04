from tkinter import *
from tkinter import ttk
import PIL.Image
import PIL.ImageTk
import Rate
import Database

class Login:

    def __init__(self, master):
        
        self.master = master
        self.master.resizable(False, False)
        
        self.logo = ttk.Frame(master)
        self.logo.pack(fill=BOTH)
        
        self.im = PIL.Image.open("resources/img/login.png")
        self.photo = PIL.ImageTk.PhotoImage(self.im)
        ttk.Label(self.logo, image = self.photo).pack(padx=15, pady=15)
        
        self.content = ttk.Frame(master, width=600, height=500)
        self.content.pack()
        
        self.uv = StringVar()
        self.pv = StringVar()
        
        ttk.Label(self.content, text = 'Username').grid(row=0, column=0)
        self.username = Entry(self.content, textvariable=self.uv)
        self.username.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.content, text = 'Password').grid(row=1, column=0)
        self.password = Entry(self.content, show="*", textvariable=self.pv)
        self.password.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(self.content, text = 'Login', command = self.login).grid(row=2, column=0, columnspan=2, padx=15, pady=15)
        self.message = ttk.Label(self.content, text = '')
        self.message.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        
    def login(self):
        
        u = str(self.username.get())
        p = str(self.password.get())
        
        user = [u, p]
        flag = Database.login(user)
        
        if(flag is True):
            self.window = Toplevel(self.master)
            Rate.Rate(self.window)
            self.master.withdraw()
        else:
            self.message['text'] = 'Wrong Username/Password'
            self.uv.set('')
            self.pv.set('')
        
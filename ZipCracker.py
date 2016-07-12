'''
Created on 26.07.2015
@author: max
'''

from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror, showinfo
import zipfile
import os
from http.client import FOUND
import string

class MyFrame(Frame):
    
    def __init__(self):
            Frame.__init__(self)
            self.master.title("ZipCracker")
            self.master.geometry("475x100")
            self.grid(sticky=W + E + N + S)
            self.textArchive = Entry(self, width=35)
            self.textArchive.grid(row=0, column=0)
            self.textDictionary = Entry(self, width=35)
            self.textDictionary.grid(row=1, column=0)
            self.buttonArchive = Button(self, text="Browse to Archive", command=self.loadFileArchive, width=20).grid(row=0, column=1)
            self.buttonDictionary = Button(self, text="Browse to Dictionary", command=self.loadFileDictionary, width=20).grid(row=1, column=1)
            self.btnCrack = Button(self, text="Start Cracking", command=self.startCrack, width=20).grid(row=2, column=1)
            
            for x in range(200):
                Grid.columnconfigure(self, x, weight=1)
        
            for y in range(500):
                Grid.rowconfigure(self, y, weight=1)
        
    def startCrack(self):
        found=False
        zip_file = zipfile.ZipFile(self.textArchive.get())
        with open(self.textDictionary.get(), 'rb') as password_list:
            for index, line in enumerate(password_list.read().splitlines()):
                try:
                    foo = str(line,encoding='utf-8')
                    zip_file.extractall(pwd=line.strip(b'\n'))
                except Exception as e:
                    if 'Bad password for file' in str(e):
                        continue
                    elif 'Bad CRC-32 for file' in str(e):
                        continue
                    else:
                        print("Exception: ",str(e))
                        
                    showinfo(title="Password found", message="The password is: "+str(foo))
                    zip_file.close()
                    found=True
                    print(str(foo))
                    break
                else:
                    showinfo(title="Password found", message="The password is: "+str(foo))
                    zip_file.close()
                    found=True
                    print(str(foo))
                    break
        if found is False:
            showinfo(title="Password not found", message="No Password has been found")
            
    def loadFileArchive(self):
                fileArchive = askopenfilename(filetypes=(("Zip File", "*.zip"),
                                                   ("Dictionary Files", "*.dic"),
                                                   ("All files", "*.*")))
                if fileArchive:
                    try:
                        self.textArchive.insert(0, fileArchive)
                     
                    except:  # <- naked except is a bad idea
                        showerror("Open Source File", "Failed to read file\n'%s'" % fileArchive)
                    return
    
    def loadFileDictionary(self):
            fileDictionary = askopenfilename(filetypes=(("Text Files", "*.txt"),
                                               ("Dictionary Files", "*.dic"),
                                               ("All files", "*.*")))
            if fileDictionary:
                try:
                    self.textDictionary.insert(0, fileDictionary)
                except:  # <- naked except is a bad idea
                    showerror("Open Source File", "Failed to read file\n'%s'" % fileDictionary)
                return


if __name__ == "__main__":
    MyFrame().mainloop()

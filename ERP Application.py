# Import tkinter library
import tkinter as tk
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter import ttk
from tkinter.ttk import *
from ctypes import windll

# Import SQL Library
import sqlite3

# Connect to DB
conn = sqlite3.connect('ERP Test.db')
cursor = conn.cursor()

# App window Qualities
root = tk.Tk()

root.geometry("1000x500")
root.resizable(True, True)
root.title("ERP Application")

# App Widgets
# Text Label
labelTest = tk.Label(root, text="test", font=("Times New Roman", 12))
labelTest.grid(row=1, column=1)

# Run App
root.mainloop()
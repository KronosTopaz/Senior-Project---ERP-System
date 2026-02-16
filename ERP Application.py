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
# Button
dashboardButton = ttk.Button(root, text="Dashboard", compound=tk.LEFT)
dashboardButton.grid(row=1, column=1, sticky=W, pady=2, padx=5)

updateInventoryButton = ttk.Button(root, text="Update Inventory and Orders", compound=tk.LEFT)
updateInventoryButton.grid(row=10, column=1, sticky=W, pady=2, padx=5)

updateFinancialButton = ttk.Button(root, text="Update Financials", compound=tk.LEFT)
updateFinancialButton.grid(row=20, column=1, sticky=W, pady=2, padx=5)

# Tables
# Table Definitions
revenueTable = ttk.Treeview(root)
expenseTable = ttk.Treeview(root)
retailTable = ttk.Treeview(root)
supplierTable = ttk.Treeview(root)
orderTable = ttk.Treeview(root)

# Assign Table Columns
revenueTable['columns'] = ('tID', 'Amount', 'Time', 'pID')
revenueTable.column('#0', width=0, stretch=tk.NO)
revenueTable.column('tID', anchor=tk.W, width=150)
revenueTable.column('Amount', anchor=tk.W, width=150)
revenueTable.column('Time', anchor=tk.W, width=150)
revenueTable.column('pID', anchor=tk.W, width=150)

# Create Table headers
revenueTable.heading('#0', text="", anchor=tk.W)
revenueTable.heading('tID', text="Transaction ID", anchor=tk.W)
revenueTable.heading('Amount', text="Amount", anchor=tk.W)
revenueTable.heading('Time', text="Time Recorded", anchor=tk.W)
revenueTable.heading('pID', text="Party", anchor=tk.W)

cursor.execute('SELECT * FROM revenue')
data = cursor.fetchall()

revenueTable.tag_configure('oddrow', background="#A4A4A4")
revenueTable.tag_configure('evenrow', background="#C8C8C8")

# Add data to Revenue Table
for i in range(len(data)):
    if i % 2:
        revenueTable.insert(parent='', index=i, values=data[i], tags=('evenrow',))
    else:
        revenueTable.insert(parent='', index=i, values=data[i], tags=('oddrow',))

revenueTable.grid(row=2, column=10, columnspan=3, sticky="nsew")
# Run App
root.mainloop()
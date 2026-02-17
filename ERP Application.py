# Import tkinter library
import tkinter as tk
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter import ttk
from tkinter.ttk import *
from ctypes import windll

# Import MatplotLib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

# Import SQL Library
import sqlite3

# Connect to DB
conn = sqlite3.connect('ERP Test.db')
cursor = conn.cursor()

# App window Qualities
root = tk.Tk()
# window = Tk()
root.geometry("1000x500")
root.resizable(True, True)
root.title("ERP Application")

# Frames
# Sidebar
sidebarFrame = tk.Frame(root, width=200)
sidebarFrame.grid(row=0, column=0, sticky="ns")

# Main Window
mainFrame = tk.Frame(root)
mainFrame.grid(row=0, column=1, sticky="nsew")
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# App Widgets
# Sidebar Button
dashboardButton = ttk.Button(sidebarFrame, text="Dashboard")
dashboardButton.pack(fill="x", pady=5)

updateInventoryButton = ttk.Button(sidebarFrame, text="Update Inventory and Orders")
updateInventoryButton.pack(fill="x", pady=5)

updateFinancialButton = ttk.Button(sidebarFrame, text="Update Financials")
updateFinancialButton.pack(fill="x", pady=5)

# Tables
# Frame for Tables
tablesFrame = tk.Frame(mainFrame)
tablesFrame.pack(fill="both", expand=True)

# Table Definitions
revenueTable = ttk.Treeview(tablesFrame)
expenseTable = ttk.Treeview(tablesFrame)
retailTable = ttk.Treeview(root)
supplierTable = ttk.Treeview(root)
orderTable = ttk.Treeview(root)

def createRevenueTable():
    # Assign Table Columns
    revenueTable['columns'] = ('tID', 'Amount', 'Time', 'pID')
    revenueTable.column('#0', width=0, stretch=tk.NO)
    revenueTable.column('tID', anchor=tk.W, width=100)
    revenueTable.column('Amount', anchor=tk.W, width=60)
    revenueTable.column('Time', anchor=tk.W, width=125)
    revenueTable.column('pID', anchor=tk.W, width=45)

    # Create Table headers
    revenueTable.heading('#0', text="", anchor=tk.W)
    revenueTable.heading('tID', text="Transaction ID", anchor=tk.W)
    revenueTable.heading('Amount', text="Amount", anchor=tk.W)
    revenueTable.heading('Time', text="Time Recorded", anchor=tk.W)
    revenueTable.heading('pID', text="Party", anchor=tk.W)

    cursor.execute('SELECT * FROM revenue')
    data = cursor.fetchall()

    revenueTable.tag_configure('oddrow', background="#EBEBEB")
    revenueTable.tag_configure('evenrow', background="#C8C8C8")

    # Add data to Revenue Table
    for i in range(len(data)):
        if i % 2:
            revenueTable.insert(parent='', index=i, values=data[i], tags=('evenrow',))
        else:
            revenueTable.insert(parent='', index=i, values=data[i], tags=('oddrow',))

    revenueTable.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    tablesFrame.grid_columnconfigure(0, weight=1)

def createExpenseTable():
    # Assign Table Columns
    expenseTable['columns'] = ('tID', 'Amount', 'Time', 'pID')
    expenseTable.column('#0', width=0, stretch=tk.NO)
    expenseTable.column('tID', anchor=tk.W, width=100)
    expenseTable.column('Amount', anchor=tk.W, width=60)
    expenseTable.column('Time', anchor=tk.W, width=125)
    expenseTable.column('pID', anchor=tk.W, width=45)

    # Create Table headers
    expenseTable.heading('#0', text="", anchor=tk.W)
    expenseTable.heading('tID', text="Transaction ID", anchor=tk.W)
    expenseTable.heading('Amount', text="Amount", anchor=tk.W)
    expenseTable.heading('Time', text="Time Recorded", anchor=tk.W)
    expenseTable.heading('pID', text="Party", anchor=tk.W)

    cursor.execute('SELECT * FROM expense')
    data = cursor.fetchall()

    expenseTable.tag_configure('oddrow', background="#EBEBEB")
    expenseTable.tag_configure('evenrow', background="#C8C8C8")

    # Add data to Revenue Table
    for i in range(len(data)):
        if i % 2:
            expenseTable.insert(parent='', index=i, values=data[i], tags=('evenrow',))
        else:
            expenseTable.insert(parent='', index=i, values=data[i], tags=('oddrow',))

    expenseTable.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    tablesFrame.grid_columnconfigure(1, weight=1)

# Sales Projection Graph
# Graph Frame
salesGraphFrame = tk.Frame(mainFrame)
salesGraphFrame.pack(fill="both", expand=True, pady=10)
def plot():
    # the figure that will contain the plot
    fig = Figure(figsize = (7, 5), dpi = 100)
    
    # Sales Data
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    sales = [7300, 6900, 6400, 5600, 5100, 5700, 5400, 4800, 3600, 4500, 5100, 3800]

    # Add subplot
    plot1 = fig.add_subplot(111)

    # Plot graph
    plot1.plot(months, sales, marker="o", linestyle="-", color="blue")

    #Graph Labels
    plot1.set_xlabel("Month")
    plot1.set_ylabel("Sales ($)")
    plot1.set_title("Monthly Sales Projection")
    plot1.tick_params(axis="x", rotation=45)

    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master = salesGraphFrame)  
    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # creating the Matplotlib toolbar
    #toolbarFrame = tk.Frame(root)
    #toolbarFrame.grid(row=20, column=10)
    toolbar = NavigationToolbar2Tk(canvas, salesGraphFrame)
    toolbar.update()

# Run App
createRevenueTable()
createExpenseTable()
plot()
root.mainloop()

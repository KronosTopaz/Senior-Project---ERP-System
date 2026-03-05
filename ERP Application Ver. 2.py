# Import tkinter library
import tkinter as tk
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter import ttk
from tkinter.ttk import *
from ctypes import windll
from tkcalendar import Calendar

# Import MatplotLib Library
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

# Import SQL Library
import sqlite3

# Connect to DB
conn = sqlite3.connect('ERP Test.db')
cursor = conn.cursor()

class app(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ERP App")
        self.geometry("1000x700")
        self.resizable(True, True)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (dashboardPage, inventoryPage, financePage):
            pageName = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[pageName] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame("dashboardPage")

    def showFrame(self, pageName):
        frame = self.frames[pageName]
        frame.tkraise()

class dashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Sidebar Frame
        sidebarFrame = tk.Frame(self, width=200)
        sidebarFrame.grid(row=0, column=0, sticky="ns")

        # Sidebar Buttons
        #dashboardButton = ttk.Button(sidebarFrame, text="Dashboard", command=lambda: controller.showFrame("dashboardPage"))
        #dashboardButton.pack(fill="x", pady=5)

        updateInventoryButton = ttk.Button(sidebarFrame, text="Update Inventory and Orders", command=lambda: controller.showFrame("inventoryPage"))
        updateInventoryButton.pack(fill="x", pady=5)

        updateFinancialButton = ttk.Button(sidebarFrame, text="Update Financials", command=lambda: controller.showFrame("financePage"))
        updateFinancialButton.pack(fill="x", pady=5)

        # Main Window
        mainFrame = tk.Frame(self)
        mainFrame.grid(row=0, column=1, sticky="nsew")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Table SubFrame
        tablesFrame = tk.Frame(mainFrame)
        tablesFrame.pack(fill="both", expand=True)

        # Tables Defined
        revenueTable = ttk.Treeview(tablesFrame)
        expenseTable = ttk.Treeview(tablesFrame)
        retailTable = ttk.Treeview(self)
        supplierTable = ttk.Treeview(self)
        orderTable = ttk.Treeview(self)

        # region - Create Revenue Table
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
        # endregion

        # region - Create Expense Table
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
        # endregion

        # region - Sales Projection Graph
        # Graph Frame
        salesGraphFrame = tk.Frame(mainFrame)
        salesGraphFrame.pack(fill="both", expand=True, pady=10)

        # The figure that will contain the plot
        fig = Figure(figsize = (7,5), dpi = 100)
        
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
        toolbar = NavigationToolbar2Tk(canvas, salesGraphFrame)
        toolbar.update()
        # endregion

class inventoryPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Sidebar
        sidebarFrame = tk.Frame(self, width=200)
        sidebarFrame.grid(row=0, column=0, sticky="ns")

        # Sidebar Buttons
        dashboardButton = ttk.Button(sidebarFrame, text="Dashboard", command=lambda: controller.showFrame("dashboardPage"))
        dashboardButton.pack(fill="x", pady=5)

        #updateInventoryButton = ttk.Button(sidebarFrame, text="Update Inventory and Orders", command=lambda: controller.showFrame("inventoryPage"))
        #updateInventoryButton.pack(fill="x", pady=5)

        updateFinancialButton = ttk.Button(sidebarFrame, text="Update Financials", command=lambda: controller.showFrame("financePage"))
        updateFinancialButton.pack(fill="x", pady=5)

        # Main Window
        mainFrame = tk.Frame(self)
        mainFrame.grid(row=0, column=1, sticky="nsew")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Table SubFrame
        tablesFrame = tk.Frame(mainFrame)
        tablesFrame.pack(fill="both", expand=True)

        # Tables Defined
        currInventoryTable = ttk.Treeview(tablesFrame)
        orderdetailsTable = ttk.Treeview(tablesFrame)
        cartTable = ttk.Treeview(tablesFrame)
        
        # region - Create Current Inventory Table
            # Assign Table Columns
        currInventoryTable['columns'] = ('Part', 'Quantity', 'Supplier')
        currInventoryTable.column('#0', width=0, stretch=tk.NO)
        currInventoryTable.column('Part', anchor=tk.W, width=50)
        currInventoryTable.column('Quantity', anchor=tk.W, width=40)
        currInventoryTable.column('Supplier', anchor=tk.W, width=50)

        # Create Table headers
        currInventoryTable.heading('#0', text="", anchor=tk.W)
        currInventoryTable.heading('Part', text="Part", anchor=tk.W)
        currInventoryTable.heading('Quantity', text="Quantity", anchor=tk.W)
        currInventoryTable.heading('Supplier', text="Supplier", anchor=tk.W)

        currInventoryQuery = '''SELECT inventory.partName, inventory.quantity, party.partyName, inventory.pID
                    FROM inventory
                    JOIN party ON inventory.pID = party.pID'''
        cursor.execute(currInventoryQuery)
        inventoryData = cursor.fetchall()

        currInventoryTable.tag_configure('oddrow', background="#EBEBEB")
        currInventoryTable.tag_configure('evenrow', background="#C8C8C8")

        # Add data to Revenue Table
        for i in range(len(inventoryData)):
            if i % 2:
                currInventoryTable.insert(parent='', index=i, values=inventoryData[i], tags=('evenrow',))
            else:
                currInventoryTable.insert(parent='', index=i, values=inventoryData[i], tags=('oddrow',))

        currInventoryTable.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        tablesFrame.grid_columnconfigure(0, weight=1)
        # endregion

        # region - Create Cart Table
        # Assign Table Columns
        cartTable['columns'] = ('Item', 'Quantity', 'Subtotal')
        cartTable.column('#0', width=0, stretch=tk.NO)
        cartTable.column('Item', anchor=tk.W, width=50)
        cartTable.column('Quantity', anchor=tk.W, width=60)
        cartTable.column('Subtotal', anchor=tk.W, width=100)

        # Create Table headers
        cartTable.heading('#0', text="", anchor=tk.W)
        cartTable.heading('Item', text="Item", anchor=tk.W)
        cartTable.heading('Quantity', text="Quantity", anchor=tk.W)
        cartTable.heading('Subtotal', text="Subtotal ($)", anchor=tk.W)

        cartTable.tag_configure('oddrow', background="#EBEBEB")
        cartTable.tag_configure('evenrow', background="#C8C8C8")

        cartTable.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        tablesFrame.grid_columnconfigure(0, weight=1)
        # endregion

        # region - Add a new order
        inputFrame = tk.Frame(mainFrame)
        inputFrame.pack(fill="both", expand=True, pady=10)

        tk.Label(inputFrame, text="Add a new order", pady=10).pack()
        
        # Select mode
        # Dropdown menu options
        partOptions = []
        parts = cursor.execute('''SELECT partName FROM inventory''')
        for i in parts:
            partOptions.append(i[0])
        
        retailerOptions = []
        retailers = cursor.execute('''SELECT partyName FROM party WHERE pType = 2''')
        for i in retailers:
            retailerOptions.append(i[0])

        # Changing dropdown menus
        # Default mode
        mode = "Parts"

        # Default value selected
        selectedPart = StringVar(value="Battery")
        selectedRetailer = StringVar(value="Best Buy")
        
        # Functions to change dropdown menu
        def orderPartSelected():
            global mode
            mode = "Parts"
            for widget in dropdownFrame.winfo_children():
                widget.destroy()
            tk.OptionMenu(dropdownFrame, selectedPart, *partOptions).pack(anchor=tk.W)

        def shipPhoneSelected():
            global mode
            mode = "Phones"
            for widget in dropdownFrame.winfo_children():
                widget.destroy()
            tk.OptionMenu(dropdownFrame, selectedRetailer, *retailerOptions).pack(anchor=tk.W)

        # Add values to cart table
        def createOrder():          
            # Grab quantity
            quantity = amountInput.get()

            # Grab retailer or supplier
            if mode == "Parts":
                selectedDropdownOutput = selectedPart.get()

                # Dollar cost
                cursor.execute('''SELECT pricePerUnit FROM inventory WHERE partName = ?''', (selectedDropdownOutput,))
                result = cursor.fetchone()

                if result:
                    unitCost = result[0]
                    totalPartCost = unitCost * int(quantity)
                    print(f"You selected {selectedDropdownOutput} and it will cost {totalPartCost}")
            elif mode == "Phones":
                selectedDropdownOutput = selectedRetailer.get()

                # Dollar cost
                cursor.execute('''SELECT pricePerUnit FROM inventory WHERE partName = ?''', (selectedDropdownOutput,))
                result = cursor.fetchone()

                if result:
                    unitCost = result[0]
                    totalPartCost = unitCost * int(quantity)


            # Grab dollar amount

        # Button to confirm mode
        tk.Button(inputFrame, text="Order Parts", command=orderPartSelected).pack(anchor=tk.W)
        tk.Button(inputFrame, text="Shipping Phones", command=shipPhoneSelected).pack(anchor=tk.W)
        
        # Dropdown menu frame
        dropdownFrame = tk.Frame(inputFrame)
        dropdownFrame.pack(pady=10, anchor=tk.W)

        orderPartSelected()

        # Enter Quantity
        tk.Label(inputFrame, text="Quantity:").pack(anchor=tk.W)
        amountInput = tk.Entry(inputFrame)
        amountInput.pack()

        # Enter order arrival date
        #tk.Label(inputFrame, text="When will the order arrive?").pack(pady=5)
        #cal = Calendar(inputFrame, selectmode='day')
        #cal.pack()

        # Button to confirm order
        tk.Button(inputFrame, text="Add to Cart", command=createOrder).pack()

        # endregion
        
class financePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Sidebar
        sidebarFrame = tk.Frame(self, width=200)
        sidebarFrame.grid(row=0, column=0, sticky="ns")

        # Sidebar Buttons
        dashboardButton = ttk.Button(sidebarFrame, text="Dashboard", command=lambda: controller.showFrame("dashboardPage"))
        dashboardButton.pack(fill="x", pady=5)

        updateInventoryButton = ttk.Button(sidebarFrame, text="Update Inventory and Orders", command=lambda: controller.showFrame("inventoryPage"))
        updateInventoryButton.pack(fill="x", pady=5)

        #updateFinancialButton = ttk.Button(sidebarFrame, text="Update Financials", command=lambda: controller.showFrame("financePage"))
        #updateFinancialButton.pack(fill="x", pady=5)

        # Main Window
        mainFrame = tk.Frame(self)
        mainFrame.grid(row=0, column=1, sticky="nsew")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Table SubFrame
        tablesFrame = tk.Frame(mainFrame)
        tablesFrame.pack(fill="both", expand=True)

        # Tables Defined
        revenueTable = ttk.Treeview(tablesFrame)
        expenseTable = ttk.Treeview(tablesFrame)
        
        
        # region - Create Retailer Revenue Table
            # Assign Table Columns
        revenueTable['columns'] = ('Retailer', 'tID', 'Amount', 'Time')
        revenueTable.column('#0', width=0, stretch=tk.NO)
        revenueTable.column('Retailer', anchor=tk.W, width=100)
        revenueTable.column('tID', anchor=tk.W, width=100)
        revenueTable.column('Amount', anchor=tk.W, width=60)
        revenueTable.column('Time', anchor=tk.W, width=125)

        # Create Table headers
        revenueTable.heading('#0', text="", anchor=tk.W)
        revenueTable.heading('Retailer', text="Retailer", anchor=tk.W)
        revenueTable.heading('tID', text="Transaction ID", anchor=tk.W)
        revenueTable.heading('Amount', text="Amount", anchor=tk.W)
        revenueTable.heading('Time', text="Time Recorded", anchor=tk.W)

        retailerQuery = '''SELECT party.partyName, revenue.tID, revenue.amount, revenue.timeRecorded
                    FROM revenue
                    JOIN party ON revenue.pID = party.pID'''
        cursor.execute(retailerQuery)
        revenueData = cursor.fetchall()

        revenueTable.tag_configure('oddrow', background="#EBEBEB")
        revenueTable.tag_configure('evenrow', background="#C8C8C8")

        # Add data to Revenue Table
        for i in range(len(revenueData)):
            if i % 2:
                revenueTable.insert(parent='', index=i, values=revenueData[i], tags=('evenrow',))
            else:
                revenueTable.insert(parent='', index=i, values=revenueData[i], tags=('oddrow',))

        revenueTable.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        tablesFrame.grid_columnconfigure(0, weight=1)
        # endregion
        
        # region - Create Supplier Expense Table
            # Assign Table Columns
        expenseTable['columns'] = ('Supplier', 'tID', 'Amount', 'Time')
        expenseTable.column('#0', width=0, stretch=tk.NO)
        expenseTable.column('Supplier', anchor=tk.W, width=100)
        expenseTable.column('tID', anchor=tk.W, width=100)
        expenseTable.column('Amount', anchor=tk.W, width=60)
        expenseTable.column('Time', anchor=tk.W, width=125)

        # Create Table headers
        expenseTable.heading('#0', text="", anchor=tk.W)
        expenseTable.heading('Supplier', text="Supplier", anchor=tk.W)
        expenseTable.heading('tID', text="Transaction ID", anchor=tk.W)
        expenseTable.heading('Amount', text="Amount", anchor=tk.W)
        expenseTable.heading('Time', text="Time Recorded", anchor=tk.W)

        supplierQuery = '''SELECT party.partyName, expense.tID, expense.amount, expense.timeRecorded
                    FROM expense
                    JOIN party ON expense.pID = party.pID'''

        cursor.execute(supplierQuery)
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
        # endregion

        # region - Input Frame
        inputFrame = tk.Frame(mainFrame)
        inputFrame.pack(fill="both", expand=True, pady=10)

        tk.Label(inputFrame, text="Add a new transaction", pady=10).pack()
        
        #Dropdown Selection
        tk.Label(inputFrame, text="Retail or Supplier transaction?").pack()
        
        partyOptions = ["Samsung", "TSMC", "Qualcomm", "LG", "Foxconn", "Arduino", "AAC Technologies",
                        "AKG", "InvenSense Inc.", "EEJA LTD.", "Innovatronix", "Behringer",
                        "Agood Company, Vishay", "Anker", "SK Hynix", "Packlane", "Best Buy",
                        "Microcenter", "Fry's Electronics", "Radioshack"]
        
        selectedValue = StringVar(value="Samsung")
        tk.OptionMenu(inputFrame, selectedValue, *partyOptions).pack()
        
        # Input a number
        tk.Label(inputFrame, text="Amount:").pack()
        amountInput = tk.Entry(inputFrame)
        amountInput.pack()

        # Input a Date & Time
        tk.Label(inputFrame, text="Select a date").pack()
        cal = Calendar(inputFrame, selectmode='day')
        cal.pack()

        #tk.Label(inputFrame, text="Enter a time (Format: HH:MM:SS)").pack()
        #timeInput = tk.Entry(inputFrame)
        #timeInput.pack()

        # Add values to DB & table
        def getTransaction():
            # Grab Date & Time
            dateOutput = cal.get_date()
            #timeOutput = timeInput.get()
            
            # Grab retailer or supplier
            partyOutput = selectedValue.get()

            # Grab dollar amount
            amountOutput = amountInput.get()

            cursor.execute('''
                            ''')
        
        tk.Button(inputFrame, text="Update", command = getTransaction).pack()
        # endregion

#----
# Main
App = app()
App.mainloop()
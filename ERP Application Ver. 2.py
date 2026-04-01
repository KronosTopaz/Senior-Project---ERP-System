# Import tkinter library
import tkinter as tk
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter import ttk
from tkinter.ttk import *
from ctypes import windll
from tkcalendar import Calendar
from tkinter import messagebox

# Import datetime library
from datetime import datetime, timedelta

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

        if hasattr(frame, 'refreshData'):
            frame.refreshData()

class dashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Sidebar Frame
        sidebarFrame = tk.Frame(self, width=200)
        sidebarFrame.grid(row=0, column=0, sticky="ns")

        updateInventoryButton = ttk.Button(sidebarFrame, text="Update Inventory and Orders", command=lambda: controller.showFrame("inventoryPage"))
        updateInventoryButton.pack(fill="x", pady=5)

        updateFinancialButton = ttk.Button(sidebarFrame, text="Update Financials", command=lambda: controller.showFrame("financePage"))
        updateFinancialButton.pack(fill="x", pady=5)

        # Main Window
        mainFrame = tk.Frame(self)
        mainFrame.grid(row=0, column=1, sticky="nsew")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Dashboard Header
        tk.Label(mainFrame, text="Dashboard").pack(pady=10)

        # Table SubFrame
        tablesFrame = tk.Frame(mainFrame)
        tablesFrame.pack(fill="both", expand=True)

        # Table titles
        tk.Label(tablesFrame, text="Recent Orders (Top 5)").grid(row=0, column=0, pady=(0, 5))
        tk.Label(tablesFrame, text="Low Inventory Alerts (< 500)").grid(row=0, column=1, pady=(0, 5))

        # Tables Defined
        self.recentOrdersTable = ttk.Treeview(tablesFrame, height=5)
        self.lowInventoryTable = ttk.Treeview(tablesFrame, height=5)

        # region - Create Recent Orders Table
            # Assign Table Columns
        self.recentOrdersTable['columns'] = ('Order #', 'Company', 'Total Cost', 'Date')
        self.recentOrdersTable.column('#0', width=0, stretch=tk.NO)
        self.recentOrdersTable.column('Order #', anchor=tk.W, width=100)
        self.recentOrdersTable.column('Company', anchor=tk.W, width=120)
        self.recentOrdersTable.column('Total Cost', anchor=tk.W, width=100)
        self.recentOrdersTable.column('Date', anchor=tk.W, width=100)

        # Create Table headers
        self.recentOrdersTable.heading('#0', text="", anchor=tk.W)
        self.recentOrdersTable.heading('Order #', text="Order Number", anchor=tk.W)
        self.recentOrdersTable.heading('Company', text="Company", anchor=tk.W)
        self.recentOrdersTable.heading('Total Cost', text="Total Amount", anchor=tk.W)
        self.recentOrdersTable.heading('Date', text="Date", anchor=tk.W)

        # Define row colors
        self.recentOrdersTable.tag_configure('oddrow', background="#EBEBEB")
        self.recentOrdersTable.tag_configure('evenrow', background="#C8C8C8")

        self.recentOrdersTable.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        tablesFrame.grid_columnconfigure(0, weight=1)
        # endregion

        # region - Create Low Part Inventory Table
        # Assign Table Columns
        self.lowInventoryTable['columns'] = ('Part', 'Quantity', 'Supplier')
        self.lowInventoryTable.column('#0', width=0, stretch=tk.NO)
        self.lowInventoryTable.column('Part', anchor=tk.W, width=120)
        self.lowInventoryTable.column('Quantity', anchor=tk.W, width=80)
        self.lowInventoryTable.column('Supplier', anchor=tk.W, width=120)

        # Assign Table Headers
        self.lowInventoryTable.heading('#0', text="", anchor=tk.W)
        self.lowInventoryTable.heading('Part', text="Part Name", anchor=tk.W)
        self.lowInventoryTable.heading('Quantity', text="Quantity Left", anchor=tk.W)
        self.lowInventoryTable.heading('Supplier', text="Supplier", anchor=tk.W)

        # Assign row colors
        self.lowInventoryTable.tag_configure('oddrow', background="#EBEBEB")
        self.lowInventoryTable.tag_configure('evenrow', background="#C8C8C8")

        # Place table
        self.lowInventoryTable.grid(row=1, column=1, sticky="nsew", padx=10, pady=5)
        tablesFrame.grid_columnconfigure(1, weight=1)
        # endregion

        # region - Sales Projection Graph
        # Graph Frame
        salesGraphFrame = tk.Frame(mainFrame)
        salesGraphFrame.pack(fill="both", expand=True, padx=20, pady=20)

        # The figure that will contain the plot
        fig = Figure(figsize = (7,4), dpi = 100)
        
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
        
        # Shrinks graph as needed
        fig.tight_layout()

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

        # Run refresh data
        self.refreshData()
    
    # Function to refresh data
    def refreshData(self):
        for item in self.recentOrdersTable.get_children():
            self.recentOrdersTable.delete(item)
        for item in self.lowInventoryTable.get_children():
            self.lowInventoryTable.delete(item)
        
        # Query DB for Recent Orders
        recentOrdersQuery = '''SELECT orders.orderNumber, party.partyName, orders.totalCost, orders.destinationDate FROM orders
                            JOIN party ON orders.pID = party.pID
                            ORDER BY orders.orderNumber DESC LIMIT 5'''
        cursor.execute(recentOrdersQuery)
        orderData = cursor.fetchall()

        # Add data to Recent Orders Table
        for i in range(len(orderData)):
            if i % 2:
                self.recentOrdersTable.insert(parent='', index=i, values=orderData[i], tags=('evenrow',))
            else:
                self.recentOrdersTable.insert(parent='', index=i, values=orderData[i], tags=('oddrow',))
        
        # Query DB for parts with low inventory (below 500 units)
        lowInventoryQuery = '''SELECT inventory.partName, inventory.quantity, party.partyName FROM inventory
                            JOIN party ON inventory.pID = party.pID WHERE inventory.quantity < 500
                            ORDER BY inventory.quantity ASC'''
        cursor.execute(lowInventoryQuery)
        lowInventoryData = cursor.fetchall()
        
        # Add data to Low Inventory Table
        for i in range(len(lowInventoryData)):
            if i % 2:
                self.lowInventoryTable.insert(parent='', index=i, values=lowInventoryData[i], tags=('evenrow',))
            else:
                self.lowInventoryTable.insert(parent='', index=i, values=lowInventoryData[i], tags=('oddrow',)) 

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

        updateFinancialButton = ttk.Button(sidebarFrame, text="Update Financials", command=lambda: controller.showFrame("financePage"))
        updateFinancialButton.pack(fill="x", pady=5)

        # Main Window
        mainFrame = tk.Frame(self)
        mainFrame.grid(row=0, column=1, sticky="nsew")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Table SubFrame
        tablesFrame = tk.Frame(mainFrame)
        tablesFrame.pack(fill="both", expand=True, padx=10, pady=10)

        # Add titles to tables
        tk.Label(tablesFrame, text="Current Inventory").grid(row=0, column=0, pady=(0, 5))
        tk.Label(tablesFrame, text="Shopping Cart").grid(row=0, column=1, pady=(0, 5))

        # Tables Defined
        currInventoryTable = ttk.Treeview(tablesFrame)
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

        currInventoryTable.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        tablesFrame.grid_columnconfigure(0, weight=1)
        tablesFrame.grid_rowconfigure(1, weight=1)
        # endregion

        # region - Create Cart Table
        # Assign Table Columns
        cartTable['columns'] = ('Item', 'Quantity', 'Subtotal', 'Company', 'Arrival Date')
        cartTable.column('#0', width=0, stretch=tk.NO)
        cartTable.column('Item', anchor=tk.W, width=110)
        cartTable.column('Quantity', anchor=tk.W, width=70)
        cartTable.column('Subtotal', anchor=tk.W, width=100)
        cartTable.column('Company', anchor=tk.W, width=100)
        cartTable.column('Arrival Date', anchor=tk.W, width=100)

        # Create Table headers
        cartTable.heading('#0', text="", anchor=tk.W)
        cartTable.heading('Item', text="Item", anchor=tk.W)
        cartTable.heading('Quantity', text="Quantity", anchor=tk.W)
        cartTable.heading('Subtotal', text="Subtotal ($)", anchor=tk.W)
        cartTable.heading('Company', text="Company", anchor=tk.W)
        cartTable.heading('Arrival Date', text="Arrival Date", anchor=tk.W)

        cartTable.tag_configure('oddrow', background="#EBEBEB")
        cartTable.tag_configure('evenrow', background="#C8C8C8")

        cartTable.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        tablesFrame.grid_columnconfigure(0, weight=1)
        tablesFrame.grid_rowconfigure(1, weight=1)
        # endregion

        # region - Add a new order
        inputFrame = tk.Frame(mainFrame, relief=tk.GROOVE, borderwidth=2)
        inputFrame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(inputFrame, text="Order Management").pack(pady=(10, 5))
        
        # Select mode
        # Mode Selection Frame
        modeFrame = tk.Frame(inputFrame)
        modeFrame.pack(pady=5)

        # Dropdown menu options
        partOptions = []
        parts = cursor.execute('''SELECT partName FROM inventory WHERE sku < (SELECT MAX(sku) FROM inventory)''')
        for i in parts:
            partOptions.append(i[0])
        
        retailerOptions = []
        retailers = cursor.execute('''SELECT partyName FROM party WHERE pType = 2''')
        for i in retailers:
            retailerOptions.append(i[0])
        
        # Bill of Materials
        bom = {part: 1 for part in partOptions if part != "Completed Phone"}
        bom["Microphone"] = 2
        bom["Magnets"] = 2

        # Dropdown menus
        # Default mode
        mode = tk.StringVar(value="Parts")

        # Default value selected
        selectedPart = StringVar(value="Battery")
        selectedRetailer = StringVar(value="Best Buy")
        
        # Functions to change dropdown menu
        def orderPartSelected():
            mode.set("Parts")
            for widget in dropdownFrame.winfo_children():
                widget.destroy()
            tk.OptionMenu(dropdownFrame, selectedPart, *partOptions).pack(anchor=tk.W)

        def shipPhoneSelected():
            mode.set("Phones")
            for widget in dropdownFrame.winfo_children():
                widget.destroy()
            tk.OptionMenu(dropdownFrame, selectedRetailer, *retailerOptions).pack(anchor=tk.W)

        # Add values to Cart Table
        def createOrder():          
            # Grab quantity
            quantity_string = amountInput.get()

            if not quantity_string.isdigit() or int(quantity_string) <= 0:
                showinfo("Error", "You did not enter a valid value for Quantity")
                return
            
            # Make quantity a int
            quantity = int(quantity_string)

            # Make Cart Table aware of parts promised previously
            cartIncoming = {}
            cartPromised = {}
            for child in cartTable.get_children():
                rowValues = cartTable.item(child, 'values')
                cartItemName = rowValues[0]
                cartItemQty = int(rowValues[1])

                if cartItemName == "Completed Phone":
                    cartPromised[cartItemName] = cartPromised.get(cartItemName, 0) + cartItemQty
                    
                    for part, multiplier in bom.items():
                        cartPromised[part] = cartPromised.get(part, 0) + (cartItemQty * multiplier)
                
                else:
                    cartIncoming[cartItemName] = cartIncoming.get(cartItemName, 0) + cartItemQty
            
            # Grab Item Name or use phone inventory depending on selected mode
            if mode.get() == "Parts":
                itemName = selectedPart.get()

                # Look up supplier name for selected part
                cursor.execute('''SELECT party.partyName FROM inventory JOIN party ON inventory.pID = party.pID WHERE inventory.partName = ?''', (itemName,))
                supplierResult = cursor.fetchone()
                # Check if it is a valid value
                if supplierResult:
                    companyName = supplierResult[0]
                
                # Estimated arrival date
                arrivalDate = (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')

            # region - Shipping phones to retailers
            elif mode.get() == "Phones":
                itemName = "Completed Phone"
                
                # Grab retailer name
                companyName = selectedRetailer.get()
                
                # See if phone quantity is sufficient
                cursor.execute('''SELECT quantity FROM inventory WHERE partName = ?''', (itemName,))
                db_PhoneInventory = cursor.fetchone()[0]

                # Subtract phones promised in cart table
                currentPhoneInventory = max(0, db_PhoneInventory + cartIncoming.get(itemName, 0) - cartPromised.get(itemName, 0))
                
                # List of parts that are low & need to be reordered
                partShortage = []

                # Checks if current inventory is enough to fulfill retailer order
                if currentPhoneInventory >= quantity:
                    daysToArrive = 9

                # If not, calculate number of phones needed and see if any parts are short for assembly
                else:
                    phonesNeeded = quantity-currentPhoneInventory
                    
                    for part, multiplier in bom.items():
                        partsNeeded = phonesNeeded * multiplier
                        cursor.execute('''SELECT quantity, pricePerUnit, pID FROM inventory WHERE partName = ?''', (part,))
                        partData = cursor.fetchone()

                        db_PartInventory = partData[0]
                        partInventory = max(0, db_PartInventory + cartIncoming.get(part, 0) - cartPromised.get(part, 0))
                        
                        unit_cost = partData[1]
                        supplier_id = partData[2]
                        
                        # Keep track of which parts are short, and by how much
                        if partInventory < partsNeeded:
                            deficit = partsNeeded - partInventory
                            
                            # Find supplier name for part
                            cursor.execute('''SELECT partyName FROM party WHERE pID = ?''', (supplier_id,))
                            supplier_name = cursor.fetchone()[0]
                            
                            partSubtotal = round((unit_cost * deficit), 2)

                            partShortage.append(f"{part} (Short: {deficit}) from {supplier_name}")

                            # Estimated arrival date
                            arrivalDate = (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')

                            # Adding parts to cart
                            # Checks what row number is next
                            currentItemRow = len(cartTable.get_children())
                            
                            rowTag = 'evenrow'
                            if currentItemRow % 2 != 0:
                                rowTag = 'oddrow'
                            # Add parts to Cart Table
                            cartTable.insert(parent='', index='end', values=(part, deficit, partSubtotal, supplier_name, arrivalDate), tags=(rowTag))
                            
                    if partShortage:
                        daysToArrive = 44
                        msg = '''We found parts short of what is needed to fulfill this order and the following parts have been added to the cart automatically:\n'''
                        msg += "\n".join(partShortage)
                        msg += f'''\n\nBecause of this, the order will be delayed by {daysToArrive} days.'''

                        messagebox.showwarning("Parts Auto-reordered", msg)
                    else:
                        daysToArrive = 29

                # Estimated arrival date
                arrivalDate = (datetime.now() + timedelta(days=daysToArrive)).strftime('%Y-%m-%d')
            # endregion

            # Calculate dollar cost
            cursor.execute('''SELECT pricePerUnit FROM inventory WHERE partName = ?''', (itemName,))
            result = cursor.fetchone()

            if result:
                unitCost = result[0]
                subtotal = round((unitCost * int(quantity)), 2)
                
                # Checks what row number is next
                currentItemRow = len(cartTable.get_children())
                
                rowTag = 'evenrow'
                if currentItemRow % 2 != 0:
                    rowTag = 'oddrow'
                
                # Add item to table
                cartTable.insert(parent='', index='end', values=(itemName, quantity, subtotal, companyName, arrivalDate), tags=(rowTag))

                # Empty quantity input for next item
                amountInput.delete(0, tk.END)

        # Button to confirm mode
        tk.Button(modeFrame, text="Order Parts", width=15, command=orderPartSelected).grid(row=0, column=0, padx=10)
        tk.Button(modeFrame, text="Shipping Phones", width=15, command=shipPhoneSelected).grid(row=0, column=1, padx=10)
        
        # Order Form Frame
        formFrame = tk.Frame(inputFrame)
        formFrame.pack(pady=15)

        # Dropdown menu frame
        tk.Label(formFrame, text="Select an Item:").grid(row=0, column=0, padx=(10, 2))
        dropdownFrame = tk.Frame(formFrame)
        dropdownFrame.grid(row=0, column=1, padx=(0, 20))

        # Generate dropdown menu
        orderPartSelected()

        # Enter Quantity
        tk.Label(formFrame, text="Quantity:").grid(row=0, column=2, padx=(0, 2))
        amountInput = tk.Entry(formFrame, width=15)
        amountInput.grid(row=0, column=3, padx=(0, 20))

        # Button to Add to Card
        tk.Button(formFrame, text="Add to Cart", command=createOrder, width=15).grid(row=0, column=4, padx=10)
        # endregion

        # region - Calculate new inventory amounts
        def confirmOrder():
            # Check if cart is empty, display message if it is
            if not cartTable.get_children():
                messagebox.showinfo("No items", "The cart is empty")
                return
            
            # Grab items from cart and add to a dictionary, grouped by company
            ordersFromCompany = {}

            for child in cartTable.get_children():
                # Get data in a row
                rowValues = cartTable.item(child, 'values')

                itemName = rowValues[0]
                quantity = int(rowValues[1])
                subtotal = float(rowValues[2])
                companyName = rowValues[3]
                arrivalDate = rowValues[4]

                # If a company name isn't in the dictionary, add it in
                if companyName not in ordersFromCompany:
                    ordersFromCompany[companyName] = []
                
                # Adding items & details to where a company name shows up
                ordersFromCompany[companyName].append({
                    'Name' : itemName,
                    'Quantity' : quantity,
                    'Subtotal' : subtotal,
                    'Date' : arrivalDate
                })
            
            # Get today's date for finance table
            today = datetime.now().strftime('%Y-%m-%d')

            for company, items in ordersFromCompany.items():
                # Grab Party ID and Party Type depending on company name
                cursor.execute('''SELECT pID, pType FROM party WHERE partyName = ?''', (company,))
                partyData = cursor.fetchone()
                pID = partyData[0]
                pType = partyData[1]

                # Calculate the Total Cost and latest Arrival Date for the order
                totalCost = sum(item['Subtotal'] for item in items)
                orderDate = max(item['Date'] for item in items)

                # Adding the order cost & date to the "orders" table
                cursor.execute('''INSERT INTO orders (destinationDate, pID, totalCost) VALUES (?, ?, ?)''', (orderDate, pID, totalCost))

                # Grab orderNumber primary key to add into "orderDetails" table
                orderID = cursor.lastrowid

                # Go through items and put into orderDetails
                for item in items:
                    # Find item SKU
                    cursor.execute('''SELECT sku FROM inventory WHERE partName = ?''', (item['Name'],))
                    sku = cursor.fetchone()[0]

                    # Inserting into "orderDetails" table
                    cursor.execute('''INSERT INTO orderDetails (orderNumber, sku, productQuantity, itemCost) VALUES (?, ?, ?, ?)''',
                                   (orderID, sku, item['Quantity'], item['Subtotal']))
                    
                    # Updating Inventory table
                    # If supplier, add parts to inventory
                    if pType == 1:
                        cursor.execute('UPDATE inventory SET quantity = quantity + ? WHERE sku = ?', (item['Quantity'], sku))
                    # If retailer, subtract parts from inventory
                    elif pType == 2:
                        cursor.execute('UPDATE inventory SET quantity = quantity - ? WHERE sku = ?', (item['Quantity'], sku))
                
                # Update Revenue & Expense tables
                # If Supplier, update Expense
                if pType == 1:
                    cursor.execute('INSERT INTO expense (amount, timeRecorded, pID) VALUES (?, ?, ?)', (totalCost, today, pID))
                # If Retailer, update Revenue
                elif pType == 2:
                    cursor.execute('INSERT INTO revenue (amount, timeRecorded, pID) VALUES (?, ?, ?)', (totalCost, today, pID))
            
            # Save changes to DB
            conn.commit()

            # Clear cart table & display confirmation message
            for child in cartTable.get_children():
                cartTable.delete(child)
            
            messagebox.showinfo("Success", "All orders have been successfully updated in the database")        

        # Submit Button Frame
        submitFrame = tk.Frame(inputFrame)
        submitFrame.pack(pady=(5, 15))

        # Button to confirm orders
        tk.Button(inputFrame, text="Confirm Orders", command=confirmOrder, width=25).pack()
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

        # Main Window
        mainFrame = tk.Frame(self)
        mainFrame.grid(row=0, column=1, sticky="nsew")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # region - Profit & Loss Summary
        summaryFrame = tk.Frame(mainFrame, relief=tk.RIDGE, borderwidth=2)
        summaryFrame.pack(fill="x", padx=10, pady=(10, 0))

        # Revenue Label
        tk.Label(summaryFrame, text="Total Revenue").grid(row=0, column=0, pady=(10, 0))
        self.labelTotalRevenue = tk.Label(summaryFrame, text="$0.00")
        self.labelTotalRevenue.grid(row=1, column=0, pady=(0, 10))

        # Expenses Label
        tk.Label(summaryFrame, text="Total Expenses").grid(row=0, column=1, pady=(10, 0))
        self.labelTotalExpense = tk.Label(summaryFrame, text="$0.00")
        self.labelTotalExpense.grid(row=1, column=1, pady=(0,10))

        # Net Profit/Loss Label
        tk.Label(summaryFrame, text="Net Profit").grid(row=0, column=2, pady=(10,0))
        self.labelNetProfit = tk.Label(summaryFrame, text="$0.00")
        self.labelNetProfit.grid(row=1, column=2, pady=(0,10))

        # Center columns
        summaryFrame.grid_columnconfigure(0, weight=1)
        summaryFrame.grid_columnconfigure(1, weight=1)
        summaryFrame.grid_columnconfigure(2, weight=1)
        # endregion

        # Table SubFrame
        tablesFrame = tk.Frame(mainFrame)
        tablesFrame.pack(fill="both", expand=True)

        # Table Labels
        tk.Label(tablesFrame, text="Revenue (Retailers)",).grid(row=0, column=0, pady=(0, 5))
        tk.Label(tablesFrame, text="Expenses (Suppliers)",).grid(row=0, column=1, pady=(0, 5))

        # Tables Defined
        self.revenueTable = ttk.Treeview(tablesFrame)
        self.expenseTable = ttk.Treeview(tablesFrame)
        
        # region - Create Retailer Revenue Table
            # Assign Table Columns
        self.revenueTable['columns'] = ('Retailer', 'tID', 'Amount', 'Time')
        self.revenueTable.column('#0', width=0, stretch=tk.NO)
        self.revenueTable.column('Retailer', anchor=tk.W, width=100)
        self.revenueTable.column('tID', anchor=tk.W, width=100)
        self.revenueTable.column('Amount', anchor=tk.W, width=60)
        self.revenueTable.column('Time', anchor=tk.W, width=125)

        # Create Table headers
        self.revenueTable.heading('#0', text="", anchor=tk.W)
        self.revenueTable.heading('Retailer', text="Retailer", anchor=tk.W)
        self.revenueTable.heading('tID', text="Transaction ID", anchor=tk.W)
        self.revenueTable.heading('Amount', text="Amount", anchor=tk.W)
        self.revenueTable.heading('Time', text="Time Recorded", anchor=tk.W)

        retailerQuery = '''SELECT party.partyName, revenue.tID, revenue.amount, revenue.timeRecorded
                    FROM revenue
                    JOIN party ON revenue.pID = party.pID'''
        cursor.execute(retailerQuery)
        revenueData = cursor.fetchall()

        self.revenueTable.tag_configure('oddrow', background="#EBEBEB")
        self.revenueTable.tag_configure('evenrow', background="#C8C8C8")

        # Add data to Revenue Table
        for i in range(len(revenueData)):
            if i % 2:
                self.revenueTable.insert(parent='', index=i, values=revenueData[i], tags=('evenrow',))
            else:
                self.revenueTable.insert(parent='', index=i, values=revenueData[i], tags=('oddrow',))

        self.revenueTable.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        tablesFrame.grid_columnconfigure(0, weight=1)
        # endregion
        
        # region - Create Supplier Expense Table
            # Assign Table Columns
        self.expenseTable['columns'] = ('Supplier', 'tID', 'Amount', 'Time')
        self.expenseTable.column('#0', width=0, stretch=tk.NO)
        self.expenseTable.column('Supplier', anchor=tk.W, width=100)
        self.expenseTable.column('tID', anchor=tk.W, width=100)
        self.expenseTable.column('Amount', anchor=tk.W, width=60)
        self.expenseTable.column('Time', anchor=tk.W, width=125)

        # Create Table headers
        self.expenseTable.heading('#0', text="", anchor=tk.W)
        self.expenseTable.heading('Supplier', text="Supplier", anchor=tk.W)
        self.expenseTable.heading('tID', text="Transaction ID", anchor=tk.W)
        self.expenseTable.heading('Amount', text="Amount", anchor=tk.W)
        self.expenseTable.heading('Time', text="Time Recorded", anchor=tk.W)

        supplierQuery = '''SELECT party.partyName, expense.tID, expense.amount, expense.timeRecorded
                    FROM expense
                    JOIN party ON expense.pID = party.pID'''

        cursor.execute(supplierQuery)
        expenseData = cursor.fetchall()

        self.expenseTable.tag_configure('oddrow', background="#EBEBEB")
        self.expenseTable.tag_configure('evenrow', background="#C8C8C8")

        # Add data to Revenue Table
        for i in range(len(expenseData)):
            if i % 2:
                self.expenseTable.insert(parent='', index=i, values=expenseData[i], tags=('evenrow',))
            else:
                self.expenseTable.insert(parent='', index=i, values=expenseData[i], tags=('oddrow',))

        self.expenseTable.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        tablesFrame.grid_columnconfigure(1, weight=1)
        tablesFrame.grid_rowconfigure(1, weight=1)
        # endregion

        # Call function to refresh tables
        self.refreshData()
    
    # Function to refresh tables
    def refreshData(self):
        for item in self.revenueTable.get_children():
            self.revenueTable.delete(item)
        for item in self.expenseTable.get_children():
            self.expenseTable.delete(item)
        
        # Query DB again for Retailers
        retailerQuery = '''SELECT party.partyName, revenue.tID, revenue.amount, revenue.timeRecorded
                FROM revenue
                JOIN party ON revenue.pID = party.pID'''
        cursor.execute(retailerQuery)
        revenueData = cursor.fetchall()

        # Add data to Revenue Table
        for i in range(len(revenueData)):
            if i % 2:
                self.revenueTable.insert(parent='', index=i, values=revenueData[i], tags=('evenrow',))
            else:
                self.revenueTable.insert(parent='', index=i, values=revenueData[i], tags=('oddrow',))
        
        # Query DB again for Suppliers
        supplierQuery = '''SELECT party.partyName, expense.tID, expense.amount, expense.timeRecorded
                FROM expense
                JOIN party ON expense.pID = party.pID'''

        cursor.execute(supplierQuery)
        expenseData = cursor.fetchall()
        
        # Add data to Revenue Table
        for i in range(len(expenseData)):
            if i % 2:
                self.expenseTable.insert(parent='', index=i, values=expenseData[i], tags=('evenrow',))
            else:
                self.expenseTable.insert(parent='', index=i, values=expenseData[i], tags=('oddrow',))

        # Calculate Profit & Loss
        # Grab total revenue
        cursor.execute('''SELECT SUM(amount) FROM revenue''')
        revenueResult = cursor.fetchone()[0]
        totalRevenue = revenueResult if revenueResult else 0.0

        # Grab Total Expenses
        cursor.execute('''SELECT SUM(amount) FROM expense''')
        expenseResult = cursor.fetchone()[0]
        totalExpense = expenseResult if expenseResult else 0.0

        # Calculate Profit/Loss
        netProfit = totalRevenue - totalExpense

        # Update Labels
        self.labelTotalRevenue.config(text=f"${totalRevenue:,.2f}")
        self.labelTotalExpense.config(text=f"${totalExpense:,.2f}")
        self.labelNetProfit.config(text=f"${netProfit:,.2f}")

#----
# Main
App = app()
App.mainloop()
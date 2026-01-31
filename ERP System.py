import sqlite3
import tkinter

def main():
    # Drop Table SQL
    dropUserTable = ('DROP TABLE IF EXISTS users')
    dropGroupTable = ('DROP TABLE IF EXISTS groups')
    dropUserGroupTable = ('DROP TABLE IF EXISTS userToGroups')
    dropInventoryTable = ('DROP TABLE IF EXISTS inventory')
    dropSupplierTable = ('DROP TABLE IF EXISTS suppliers')
    dropOrderTable = ('DROP TABLE IF EXISTS orders')

    # Create Table SQL
    createUserTable = ('''CREATE TABLE IF NOT EXISTS users
                       (uID INTEGER PRIMARY KEY AUTOINCREMENT,
                       userName TEXT,
                       password VARCHAR,
                       lastLogin DATETIME
                       )''')
    
    createGroupTable = ('''CREATE TABLE IF NOT EXISTS groups
                        (gID INTEGER PRIMARY KEY AUTOINCREMENT,
                        role TEXT
                        )''')
    
    createUserGroupTable = ('''CREATE TABLE IF NOT EXISTS userToGroups
                            (uID INTEGER,
                            gID INTEGER,
                            FOREIGN KEY (uID) REFERENCES users(uID),
                            FOREIGN KEY (gID) REFERENCES groups(gID)
                            )''')
    
    createInventoryTable = ('''CREATE TABLE IF NOT EXISTS inventory
                            (sku INTEGER PRIMARY KEY AUTOINCREMENT,
                            partName TEXT NOT NULL,
                            currentAmount INTEGER NOT NULL,
                            pricePerUnit REAL NOT NULL
                            )''')
    
    createSupplierTable = ('''CREATE TABLE IF NOT EXISTS suppliers
                           (sID INTEGER PRIMARY KEY AUTOINCREMENT,
                           supplierName TEXT NOT NULL
                           )''')
    
    createOrdersTable = ('''CREATE TABLE IF NOT EXISTS orders
                         (orderNumber INTEGER PRIMARY KEY AUTOINCREMENT,
                         estimatedArrival DATE,
                         sku INTEGER NOT NULL,
                         sID INTEGER NOT NULL,
                         incomingAmount INTEGER NOT NULL,
                         orderCost REAL NOT NULL,
                         FOREIGN KEY (sku) REFERENCES inventory(sku),
                         FOREIGN KEY (sID) REFERENCES suppliers(sID)
                         )''')
    
    # Inserting Data
    userData = [("Jimmy", "I_Love_Working", "2026-01-01 13:00:07"),
                ("Jane", "passwordispassword", "2026-01-08 19:04:37"),
                ("Bob", "bobbyboy", "2025-12-29 15:24:58"),
                ("Daisy", "Flowers", "2025-12-23 11:29:50"),
                ("Mark", "suppliesareL0w", "2025-12-31 14:23:13")
                ]
    
    groupData = [("Administrator",),
                 ("Employee",),
                 ("Consultant",)
                 ]

    userGroupData = [(1, 1),
                     (1, 2),
                     (2, 2),
                     (3, 2),
                     (4, 3),
                     (5, 3)]
    
    supplierData = [("Samsung",),
                    ("TSMC",),
                    ("Qualcomm",),
                    ("LG",),
                    ("Foxconn",),
                    ("Arduino",),
                    ("AAC Technologies",),
                    ("AKG",),
                    ("InvenSense Inc.",),
                    ("EEJA LTD.",),
                    ("Innovatronix",),
                    ("Behringer",),
                    ("Agood Company",),
                    ("Vishay",),
                    ("Anker",),
                    ("SK Hynix",)]
    
    inventoryData = [("Battery", 10038, 0.48),
                     ("CPU", 25740, 0.68),
                     ("Motherboard", 7058, 0.12),
                     ("Screen", 39490, 0.26),
                     ("Power Button", 24291, 0.10),
                     ("Volume Rocker", 21503, 0.12),
                     ("Frame", 43047, 0.43),
                     ("Back Glass", 17412, 0.35),
                     ("Wide Camera", 21028, 0.41),
                     ("Ultrawide Camera", 17371, 0.42),
                     ("Telephoto Camera", 19129, 0.50),
                     ("Front Camera", 34153, 0.39),
                     ("USB-C Controller", 13791, 0.25),
                     ("Camera Flash", 12837, 0.10),
                     ("Speaker", 303, 0.19),
                     ("Earpiece Speaker", 434, 0.19),
                     ("Microphone", 43857, 0.15),
                     ("Vibration Motor", 3232, 0.27),
                     ("Wireless Charging Coil", 895, 0.09),
                     ("Magnets", 134, 0.11),
                     ("Gyroscope Sensor", 693, 0.20),
                     ("Accelerometer", 908, 0.19),
                     ("NFC Sensor", 1228, 0.17),
                     ("Box", 60937, 0.02),
                     ("Cable", 9573, 0.02),
                     ("RAM", 1855, 1.27)]
    
    orderData = [("2026-02-23", 1, 1,20, 9.60),
                 ("2026-02-16", 3, 2, 30, 3.60),
                 ("2026-01-31", 8, 1, 23, 8.05),
                 ("2026-03-02", 10, 4, 32, 13.44),
                 ("2026-02-21", 15, 8, 33, 6.27),
                 ("2026-03-12", 16, 8, 42, 7.98),
                 ("2026-03-09", 19, 14, 52, 4.68),
                 ("2026-04-01", 20, 13, 27, 2.97),
                 ("2026-04-30", 21, 9, 54, 10.80),
                 ("2026-01-10", 22, 9, 21, 3.99),
                 ("2026-04-30", 23, 9, 35, 5.95)]

    # Connect to DB & Create Cursor
    conn = sqlite3.connect('MRP Test.db')
    cursor = conn.cursor()

    # Drop existing tables
    cursor.execute(dropUserTable)
    cursor.execute(dropGroupTable)
    cursor.execute(dropUserGroupTable)
    cursor.execute(dropInventoryTable)
    cursor.execute(dropSupplierTable)
    cursor.execute(dropOrderTable)

    # Create tables
    cursor.execute(createUserTable)
    cursor.execute(createGroupTable)
    cursor.execute(createUserGroupTable)
    cursor.execute(createInventoryTable)
    cursor.execute(createSupplierTable)
    cursor.execute(createOrdersTable)

    # Insert Data
    cursor.executemany('INSERT INTO users (username, password, lastLogin) VALUES (?, ?, ?)', userData)
    cursor.executemany('INSERT INTO groups (role) VALUES (?)', groupData)
    cursor.executemany('INSERT INTO userToGroups (uID, gID) VALUES (?, ?)', userGroupData)
    cursor.executemany('INSERT INTO suppliers (supplierName) VALUES (?)', supplierData)
    cursor.executemany('INSERT INTO inventory (partName, currentAmount, pricePerUnit) VALUES (?, ?, ?)', inventoryData)
    cursor.executemany('INSERT INTO orders (estimatedArrival, sku, sID, incomingAmount, orderCost) VALUES (?, ?, ?, ?, ?)', orderData)

    #Save changes
    conn.commit()

#--------------------------------
# Run Main Function
main()
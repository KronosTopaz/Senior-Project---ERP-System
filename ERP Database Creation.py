import sqlite3

def main():
    # Drop Table SQL
    dropUserTable = ('DROP TABLE IF EXISTS users')
    dropGroupTable = ('DROP TABLE IF EXISTS groups')
    dropUserGroupTable = ('DROP TABLE IF EXISTS userToGroups')
    dropInventoryTable = ('DROP TABLE IF EXISTS inventory')
    dropPartyTable = ('DROP TABLE IF EXISTS party')
    dropOrderTable = ('DROP TABLE IF EXISTS orders')
    dropRevenueTable = ('DROP TABLE IF EXISTS revenue')
    dropExpenseTable = ('DROP TABLE IF EXISTS expense')

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
    
    createPartyTable = ('''CREATE TABLE IF NOT EXISTS party
                        (pID INTEGER PRIMARY KEY AUTOINCREMENT,
                        partyName TEXT NOT NULL,
                        pType INTEGER NOT NULL
                        )''')
    
    createInventoryTable = ('''CREATE TABLE IF NOT EXISTS inventory
                            (sku INTEGER PRIMARY KEY AUTOINCREMENT,
                            partName TEXT NOT NULL,
                            quantity INTEGER NOT NULL,
                            pricePerUnit REAL NOT NULL,
                            pID INTEGER NOT NULL,
                            FOREIGN KEY (pID) REFERENCES party(pID)
                            )''')
    
    createOrdersTable = ('''CREATE TABLE IF NOT EXISTS orders
                         (orderNumber INTEGER PRIMARY KEY AUTOINCREMENT,
                         destinationDate DATE,
                         pID INTEGER NOT NULL,
                         totalCost NUMERIC NOT NULL,
                         FOREIGN KEY (pID) REFERENCES party(pID)
                         )''')
    
    createOrderDetailsTable = ('''CREATE TABLE IF NOT EXISTS orderDetails
                                (lineID INTEGER PRIMARY KEY AUTOINCREMENT,
                                orderNumber INTEGER NOT NULL,
                                sku INTEGER NOT NULL,
                                productQuantity INTEGER NOT NULL,
                                itemCost NUMERIC NOT NULL,
                                FOREIGN KEY (orderNumber) REFERENCES orders(orderNumber),
                                FOREIGN KEY (sku) REFERENCES inventory(sku)
                                )''')
    
    createRevenueTable = ('''CREATE TABLE IF NOT EXISTS revenue
                        (tID INTEGER PRIMARY KEY AUTOINCREMENT,
                        amount NUMERIC NOT NULL,
                        timeRecorded DATETIME NOT NULL,
                        pID INTEGER NOT NULL,
                        FOREIGN KEY (pID) REFERENCES party(pID)
                        )''')
    
    createExpenseTable = ('''CREATE TABLE IF NOT EXISTS expense
                        (tID INTEGER PRIMARY KEY AUTOINCREMENT,
                        amount NUMERIC NOT NULL,
                        timeRecorded DATETIME NOT NULL,
                        pID INTEGER NOT NULL,
                        FOREIGN KEY (pID) REFERENCES party(pID)
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
    
    partyData = [("Samsung", 1),
                ("TSMC", 1),
                ("Qualcomm", 1),
                ("LG", 1),
                ("Foxconn", 1),
                ("Arduino", 1),
                ("AAC Technologies", 1),
                ("AKG", 1),
                ("InvenSense Inc.", 1),
                ("EEJA LTD.", 1),
                ("Innovatronix", 1),
                ("Behringer", 1),
                ("Agood Company", 1),
                ("Vishay", 1),
                ("Anker", 1),
                ("SK Hynix", 1),
                ("Packlane", 1),
                # Retailers:
                ("Best Buy", 2),
                ("Microcenter", 2),
                ("Fry's Electronics", 2),
                ("Radioshack", 2)]
    
    inventoryData = [("Battery", 10038, 0.48, 5),
                     ("CPU", 25740, 0.68, 3),
                     ("Motherboard", 7058, 0.12, 2),
                     ("Screen", 39490, 0.26, 1),
                     ("Power Button", 24291, 0.10, 10),
                     ("Volume Rocker", 21503, 0.12, 10),
                     ("Frame", 43047, 0.43, 4),
                     ("Back Glass", 17412, 0.35, 1),
                     ("Wide Camera", 21028, 0.41, 4),
                     ("Ultrawide Camera", 17371, 0.42, 4),
                     ("Telephoto Camera", 19129, 0.50, 4),
                     ("Front Camera", 34153, 0.39, 4),
                     ("USB-C Controller", 13791, 0.25, 10),
                     ("Camera Flash", 12837, 0.10, 11),
                     ("Speaker", 303, 0.19, 8),
                     ("Earpiece Speaker", 434, 0.19, 8),
                     ("Microphone", 43857, 0.15, 12),
                     ("Vibration Motor", 3232, 0.27, 7),
                     ("Wireless Charging Coil", 895, 0.09, 14),
                     ("Magnets", 134, 0.11, 13),
                     ("Gyroscope Sensor", 693, 0.20, 9),
                     ("Accelerometer", 908, 0.19, 9),
                     ("NFC Sensor", 128, 0.17, 9),
                     ("Box", 60937, 0.02, 17),
                     ("Cable", 9573, 0.02, 15),
                     ("RAM", 1855, 1.27, 16)]
    
    # Date, pID, totalCost
    orderData = [("2026-02-23", 14, 108.45),
                 ("2026-02-16", 8, 662.91),
                 ("2026-01-31", 9, 554.14),
                 ("2026-03-02", 13, 328.35),
                 ("2026-02-21", 16, 4785.36),
                 ]

    # orderNumber, sku, productQuantity, itemCost 
    orderDetailData = [(1, 19, 1205, 108.45),
                       (2, 16, 1543, 293.17),
                       (2, 15, 1946, 369.74),
                       (3, 21, 947, 189.40),
                       (3, 22, 285, 54.15),
                       (3, 23, 1827, 310.59),
                       (4, 20, 2958, 328.35),
                       (5, 26, 3768, 4785.36)
                       ]
    
    revenueData = [(120.54, "2026-01-05 09:03:01", 18),
                   (221.40, "2026-01-09 12:25:27", 19),
                   (324.98, "2026-01-09 13:28:54", 21),
                   (635.63, "2026-01-11 22:38:41", 20),
                   (50.12, "2026-01-11 22:47:11", 21)]
    
    expenseData = [(108.45, "2026-01-04 02:41:12", 1),
                   (293.17, "2026-01-05 15:35:06", 2),
                   (189.40, "2026-01-07 21:12:35", 3),
                   (328.35, "2026-01-07 10:43:11", 4),
                   (54.15, "2026-01-07 17:22:14", 3)]

    # Connect to DB & Create Cursor
    conn = sqlite3.connect('ERP Test.db')
    cursor = conn.cursor()

    # Drop existing tables
    cursor.execute(dropUserTable)
    cursor.execute(dropGroupTable)
    cursor.execute(dropUserGroupTable)
    cursor.execute(dropInventoryTable)
    cursor.execute(dropPartyTable)
    cursor.execute(dropOrderTable)
    cursor.execute(dropRevenueTable)
    cursor.execute(dropExpenseTable)

    # Create tables
    cursor.execute(createUserTable)
    cursor.execute(createGroupTable)
    cursor.execute(createUserGroupTable)
    cursor.execute(createInventoryTable)
    cursor.execute(createPartyTable)
    cursor.execute(createOrdersTable)
    cursor.execute(createOrderDetailsTable)
    cursor.execute(createRevenueTable)
    cursor.execute(createExpenseTable)

    # Insert Data
    cursor.executemany('INSERT INTO users (username, password, lastLogin) VALUES (?, ?, ?)', userData)
    cursor.executemany('INSERT INTO groups (role) VALUES (?)', groupData)
    cursor.executemany('INSERT INTO userToGroups (uID, gID) VALUES (?, ?)', userGroupData)
    cursor.executemany('INSERT INTO party (partyName, pType) VALUES (?, ?)', partyData)
    cursor.executemany('INSERT INTO inventory (partName, quantity, pricePerUnit, pID) VALUES (?, ?, ?, ?)', inventoryData)
    cursor.executemany('INSERT INTO orders (destinationDate, pID, totalCost) VALUES (?, ?, ?)', orderData)
    cursor.executemany('INSERT INTO orderDetails (orderNumber, sku, productQuantity, itemCost) VALUES (?, ?, ?, ?)', orderDetailData)
    cursor.executemany('INSERT INTO revenue (amount, timeRecorded, pID) VALUES (?, ?, ?)', revenueData)
    cursor.executemany('INSERT INTO expense (amount, timeRecorded, pID) VALUES (?, ?, ?)', expenseData)

    #Save changes
    conn.commit()

#--------------------------------
# Run Main Function
main()
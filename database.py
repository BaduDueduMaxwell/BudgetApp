import sqlite3

DATABASE = "database.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

connect_db = get_db()
cursor = connect_db.cursor()
cursor.execute('''
                CREATE TABLE IF NOT EXISTS User(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                User_First_Name TEXT NOT NULL,
                User_Last_Name TEXT NOT NULL,
                User_Email TEXT  UNIQUE NOT NULL,
                User_Password TEXT NOT NULL
                )''')
connect_db.commit()

connect_db = get_db()
cursor = connect_db.cursor()
cursor.execute('''
                CREATE TABLE IF NOT EXISTS Income(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                SOURCE TEXT NOT NULL,
                VALUE INTEGER NOT NULL,
                MONTH INTEGER NOT NULL,
                User_id INTEGER,
                FOREIGN KEY (User_id) REFERENCES User (id)
                )''')
connect_db.commit()


connect_db = get_db()
cursor = connect_db.cursor()
cursor.execute('''
                CREATE TABLE IF NOT EXISTS Expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Category TEXT NOT NULL,
                Expense INTEGER NOT NULL,
                Date INTEGER NOT NULL,
                User_id INTEGER ,
                FOREIGN KEY (User_id) REFERENCES User (id)
                )''')
connect_db.commit()



connect_db = get_db()
cursor = connect_db.cursor()
cursor.execute('''
                CREATE TABLE IF NOT EXISTS Budget(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Category TEXT UNIQUE NOT NULL,
                Percentage INTEGER NOT NULL,
                Color TEXT NOT NULL
                )''')
connect_db.commit()
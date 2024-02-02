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
                User_Email TEXT NOT NULL,
                User_Password TEXT NOT NULL,
                )''')
connect_db.commit()

connect_db = get_db()
cursor = connect_db.cursor()
cursor.execute('''
                CREATE TABLE IF NOT EXISTS Income(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                SOURCE TEXT NOT NULL,
                VALUE INTEGER NOT NULL,
                User_id INTEGER NOT NULL,
                FOREIGN KEY (User_id) REFERENCES User (id)
                )''')
connect_db.commit()


connect_db = get_db()
cursor = connect_db.cursor()
cursor.execute('''
                CREATE TABLE IF NOT EXISTS Expense(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                SOURCE TEXT NOT NULL,
                VALUE INTEGER NOT NULL,
                User_id INTEGER NOT NULL,
                FOREIGN KEY (User_id) REFERENCES User (id)
                )''')
connect_db.commit()
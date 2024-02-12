import sqlite3
import hashlib
import random,datetime
db = sqlite3.connect('database.db')
with db:
    #db.row_factory = sqlite3.Row
    cursor = db.cursor()
    email = ["mofosuhene@gmail.com"]
    cursor.execute("SELECT User_Password, id FROM User WHERE User_Email = ?", (email))
    rows = cursor.fetchone()
    print(rows[0])

def hash_text(parameter):
    h=hashlib.new("SHA256")
    h.update(parameter.encode())
    hashed_password = h.hexdigest()
    return hashed_password

print((hash_text("still@88")) == rows[0])

Date = str(datetime.datetime.now()).split(" ")[0]
datee = datetime.datetime.strptime(Date, "%Y-%m-%d").month
print(datee)

income_details = ["Salary",500,2,1]
cursor = db.cursor()
cursor.executemany('INSERT INTO Income (SOURCE, VALUE, MONTH, User_id) VALUES (?, ?, ?, ?)', (income_details,))
db.commit()
#user_data = cursor.fetchone()
#print(user_data[2::])
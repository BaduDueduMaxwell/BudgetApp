from flask import Flask, render_template,request
import sqlite3, hashlib

DATABASE = "database.db"

def get_db():
    connection = sqlite3.connect(DATABASE)
    return connection

def hash_text(parameter):
    h=hashlib.new("SHA256")
    h.update(parameter.encode())
    hashed_password = h.hexdigest()
    return hashed_password

app = Flask(__name__)

@app.get("/")
def welcome():
    return render_template("index.html")

@app.get("/signup.html")
def signup_page():
    return render_template("signup.html")

@app.post("/signup.html")
def signup():
    first_name = request.form["first name"]
    last_name = request.form["last name"]
    email= request.form["email"]
    password = request.form["password"]
    hashed_password = hash_text(password)
    user_credentials = [first_name,last_name,email,hashed_password]
    db_connection = get_db()
    cursor = db_connection.cursor()
    cursor.executemany('INSERT INTO User (User_First_Name, User_Last_Name, User_Email, User_Password) VALUES (?, ?, ?, ?)', (user_credentials,))
    db_connection.commit()
    return render_template("login.html")


@app.get("/login.html")
def login():
    email= request.form["email"]
    password = request.form["password"]
    hashed_password = hash_text(password)

    db_connection = get_db()
    cursor = db_connection.cursor()
    cursor.executemany("SELECT User_Password, id FROM User WHERE User_Email = ?", (email))
    user_data = cursor.fetchall()
    user_password = user_data[0]

    if hashed_password == user_password:
        return render_template("dashboard.html")
    else:
        return render_template("login.html") 

if __name__ == 'main':
    app.run(debug=True)
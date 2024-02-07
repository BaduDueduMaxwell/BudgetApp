from flask import Flask, render_template,request
import sqlite3, hashlib, datetime

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

@app.route("/")
def welcome():
    return render_template("index.html")

@app.get("/signup")
def signup_page():
    return render_template("signup.html")

@app.post("/signup")
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
    return render_template("index.html")

@app.get("/login")
def get_login():
    return render_template("login.html")


@app.post("/login")
def login():
    email= request.form["email"]
    password = request.form["password"]
    hashed_password = hash_text(password)
    email = [email]

    db_connection = get_db()
    cursor = db_connection.cursor()
    cursor.execute("SELECT User_Password, id FROM User WHERE User_Email = ?", (email))
    user_data = cursor.fetchone()
    user_password = user_data[0]
    if hashed_password == user_password:
        return render_template("dashboard.html")
    
    return render_template("login.html")
    
@app.get("/dashboard")
def get_dashboard():
    return render_template("dashboard.html")

@app.get("/expenses/<int:id>")
def get_expenses(id):
    db_connection = get_db()
    cursor = db_connection.cursor()
    cursor.execute("SELECT DESCRIPTION, VALUE FROM Expense JOIN User on Expense.User_id == User.id WHERE User_id = ?", id)
    user_data = cursor.fetchone()
    return render_template("expenses.html")

@app.post("/expenses/<int:id>")
def add_expense(id):
    expense = request.form["expenseItem"]
    amount = request.form["expenseAmount"]
    Date = str(datetime.datetime.now()).split(" ")[0]
    datee = datetime.datetime.strptime(Date, "%Y-%m-%d").month
    expense_details = [expense,amount,datee,id]
    db_connection = get_db()
    cursor = db_connection.cursor()
    cursor.executemany('INSERT INTO Expense (DESCRIPTION, VALUE, MONTH, User_id) VALUES (?, ?, ?, ?)', (expense_details,))
    db_connection.commit()
    return render_template("expenses.html")

@app.post("/expenses/<int:id>")
def add_expense(id):
    income = request.form["incomeItem"]
    amount = request.form["incomeAmount"]
    Date = str(datetime.datetime.now()).split(" ")[0]
    datee = datetime.datetime.strptime(Date, "%Y-%m-%d").month
    income_details = [income,amount,datee,id]
    db_connection = get_db()
    cursor = db_connection.cursor()
    cursor.executemany('INSERT INTO Income (DESCRIPTION, VALUE, MONTH, User_id) VALUES (?, ?, ?, ?)', (income_details,))
    db_connection.commit()
    return render_template("income.html")


@app.get("/income")
def get_income():
    return render_template("income.html")
    

    

if __name__ == 'main':
    app.run(debug=True)
from flask import Flask, render_template,request,url_for,redirect,flash
import sqlite3, hashlib, datetime

app = Flask(__name__)

DATABASE = "database.db"
app.secret_key = 'secret'

def get_db():
    connection = sqlite3.connect(DATABASE)
    return connection

def hash_text(parameter):
    h=hashlib.new("SHA256")
    h.update(parameter.encode())
    hashed_password = h.hexdigest()
    return hashed_password



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
        return render_template("dashboard.html",email = email)
    
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



    
@app.route('/addexpense', methods=['GET', 'POST'])
def addexpense():
    # If we send POST request to create user
    # add logic
    if request.method == 'POST':
        category = request.form['category']
        expense = request.form['expense']
        date = request.form['date']
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Expenses (Category, Expense, Date) VALUES (?, ?, ?)', (category, expense, date))
        conn.commit()
        conn.close()
        flash('Details added successfully', 'success')
        return redirect(url_for('addexpense'))
    
# If we send GET request to get all users
    # add logic
    if request.method == 'GET':
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Expenses')
            entries = cursor.fetchall()
        conn.close()

        return render_template('add_expenses.html', entries=entries)
def get_all_entries():
    with get_db() as conn:
        cursor = conn.cursor()
        myqueries = f'SELECT * FROM Expenses'
        cursor.execute(myqueries)
        entries = cursor.fetchall()
    return entries

def get_all_income():
    with get_db() as conn:
        cursor = conn.cursor()
        myqueries = f'SELECT * FROM Income'
        cursor.execute(myqueries)
        entries = cursor.fetchall()
    return entries

@app.route('/expenses')
def expenses():
    entries = get_all_entries()
    return render_template('expenses.html', entries=entries)

@app.route('/income')
def income():
    entries = get_all_income()
    return render_template('income.html', entries=entries)
    

@app.route('/addincome', methods=['GET', 'POST'])
def addincome():
    # If we send POST request to create user
    # add logic
    if request.method == 'POST':
        source = request.form['source']
        income = request.form['income']
        date = request.form['date']
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Income (SOURCE, VALUE, MONTH) VALUES (?, ?, ?)', (source, income, date))
        conn.commit()
        conn.close()
        flash('Details added successfully', 'success')
        return redirect(url_for('addincome'))
    
# If we send GET request to get all users
    # add logic
    if request.method == 'GET':
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Income')
            entries = cursor.fetchall()
        conn.close()

        return render_template('add_income.html', entries=entries)


if __name__ == '__main__':
    app.run(debug=True)
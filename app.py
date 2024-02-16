from flask import Flask, render_template,request,flash,url_for,redirect,session
import sqlite3, hashlib
from datetime import datetime

DATABASE = "database.db"
app = Flask(__name__)
app.secret_key = 'your_unique_secret_key_here'

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

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("welcome"))


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
    user_id = user_data[1]
    if hashed_password == user_password:
        return redirect(url_for('get_dashboard', user_id=user_id))   
    return render_template("login.html")

def calculate_total_expenses(user_id):
    db_connection = get_db()
    cursor = db_connection.cursor()
    cursor.execute("SELECT SUM(Expense) FROM Expenses WHERE User_id = ?", (user_id,))
    total_expenses = cursor.fetchone()[0]
    db_connection.close()
    return total_expenses if total_expenses else 0

def get_expenses_data(user_id):
    db_connection = get_db()
    cursor = db_connection.cursor()
    cursor.execute("SELECT Category, SUM(Expense) FROM Expenses WHERE User_id = ? GROUP BY Category", (user_id,))
    expense_data = cursor.fetchall()
    db_connection.close()

    # Process the data for the chart
    labels = [entry[0] for entry in expense_data]
    expenses = [entry[1] for entry in expense_data]
    background_colors = ["#051b6b", "#2980b9", "#21618c"] 

    return {
        "labels": labels,
        "expensesData": expenses,
        "backgroundColor": background_colors
    }


@app.get("/dashboard/<int:user_id>")
def get_dashboard(user_id):
    db_connection = get_db()
    cursor = db_connection.cursor()
    cursor.execute("SELECT User_First_Name, User_Last_Name, User_Email FROM User WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()
    first_name = user_data[0]
    last_name = user_data[1]
    user_email = user_data[2]
    total_expenses = calculate_total_expenses(user_id)
    percentage_savings = calculate_percentage_savings(user_id)
    savings = calculate_savings(user_id)
    total_income = calculate_total_income(user_id)
    expenses_data = get_expenses_data(user_id)
    daily_labels, daily_expenses = get_daily_expenses_data(user_id)
    expenses_data["dailyLabels"] = daily_labels
    expenses_data["dailyExpenses"] = daily_expenses
    financial_data = get_financial_data(user_id)
    return render_template("dashboard.html", user_id=user_id, first_name=first_name, last_name=last_name, user_email=user_email, total_expenses=total_expenses,percentage_savings=percentage_savings,savings = savings,
                           total_income = total_income, expenses_data=expenses_data, financial_data=financial_data)

def get_financial_data(user_id):
    total_expenses = calculate_total_expenses(user_id)
    savings = calculate_savings(user_id)
    total_income = calculate_total_income(user_id)

    return {
        "totalIncome": total_income,
        "totalExpenses": total_expenses,
        "savings": savings
    }

def calculate_total_income(user_id):
    db_connection = get_db()
    cursor = db_connection.cursor()
    cursor.execute("SELECT SUM(Income) FROM Incomes WHERE User_id = ?", (user_id,))
    total_income = cursor.fetchone()[0]
    db_connection.close()
    return total_income if total_income else 0

def calculate_percentage_savings(user_id):
    total_income = calculate_total_income(user_id)
    total_expenses = calculate_total_expenses(user_id)
    if total_income == 0:
        return 0  
    percentage_savings = ((total_income - total_expenses) / total_income) * 100
    return round(percentage_savings, 2)

def calculate_savings(user_id):
    total_income = calculate_total_income(user_id)
    total_expenses = calculate_total_expenses(user_id)
    savings = total_income - total_expenses
    return savings if savings >= 0 else 0

def get_daily_expenses_data(user_id):
    db_connection = get_db()
    cursor = db_connection.cursor()
    cursor.execute("SELECT DayOfWeek, SUM(Expense) FROM Expenses WHERE User_id = ? GROUP BY DayOfWeek", (user_id,))
    daily_data = cursor.fetchall()
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    daily_expenses = [0] * 7
    
    for entry in daily_data:
        day_name = entry[0]
        day_index = days_of_week.index(day_name)
        daily_expenses[day_index] = entry[1]
    
    return days_of_week, daily_expenses




@app.get("/expenses/<int:id>")
def expenses(id):
    db_connection = get_db()
    cursor = db_connection.cursor()
    entries = cursor.execute("SELECT User_First_Name,User_Email,Category, Expense, Date FROM Expenses JOIN User on Expenses.User_id == User.id WHERE User_id = ?", (id,))
    return render_template("expenses.html",id = id, entries = entries )

@app.route('/addexpenses/<int:id>', methods=['GET', 'POST'])
def addexpense(id):
    if request.method == 'POST':
        category = request.form['category']
        expense = request.form['expense']
        date_now = datetime.now()
        string = '%A, %d. %B %Y %I:%M%p'
        day_of_week = date_now.strftime('%A') 
        date = date_now.strftime(string)
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Expenses (User_id, Category, Expense, Date, DayOfWeek) VALUES (?, ?, ?, ?, ?)', (id, category, expense, date, day_of_week))
            conn.commit()
        flash('Details added successfully', 'success')
        return redirect(url_for('addexpense', id = id))
   
    if request.method == 'GET':
        db_connection = get_db()
        cursor = db_connection.cursor()
        return render_template("add_expenses.html", id = id)
    
@app.route('/addincome/<int:id>', methods=['GET', 'POST'])
def addincome(id):
    if request.method == 'POST':
        source = request.form['source']
        income = request.form['income']
        date_now = datetime.now()
        string = '%A, %d. %B %Y %I:%M%p'
        date = date_now.strftime(string)
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO  Incomes(User_id, Source, Income, Date) VALUES (?, ?, ?, ?)', (id, source, income, date))
            conn.commit()
        flash('Details added successfully', 'success')
        return redirect(url_for('addincome', id = id))

    if request.method == 'GET':
        db_connection = get_db()
        cursor = db_connection.cursor()
        return render_template("add_incomes.html", id = id)

    
@app.get("/income/<int:id>")
def income(id):
    db_connection = get_db()
    cursor = db_connection.cursor()
    entries = cursor.execute("SELECT User_First_Name,User_Email,Source, Income, Date FROM Incomes JOIN User on Incomes.User_id == User.id WHERE User_id = ?", (id,))
    return render_template("income.html",id = id,entries = entries )
      
if __name__ == '__main__':
    app.run(debug=True)
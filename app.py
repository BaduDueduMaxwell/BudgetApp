from flask import Flask, render_template,request,flash,url_for,redirect,session
import sqlite3, hashlib
import random
from datetime import datetime
from helper_functions import *


Income_color = {
    'Allowance': '#051b6b',
    'Bonus': 'purple',
    'Investment': 'green',
    'Lottery': 'blue',
    'Salary': 'orange',
    'Tips': 'cyan',
    'Family': 'yellow',
    'Others': '#3498d',
}

DATABASE = "database.db"
app = Flask(__name__)
app.secret_key = 'your_unique_secret_key_here'

def get_db():
    connection = sqlite3.connect(DATABASE)
    return connection  

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
    return render_template("login.html")

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
    error = None
    db_connection = get_db()
    cursor = db_connection.cursor()
    cursor.execute("SELECT User_Password, id FROM User WHERE User_Email = ?", (email))
    user_data = cursor.fetchone()
    if user_data:
        user_password = user_data[0]
        user_id = user_data[1]
        if hashed_password == user_password:
            return redirect(url_for('get_dashboard', user_id=user_id))
        else:
            error = "Incorrect password/email"
            return render_template("login.html",error = error)
    error = "You don't have an account.Create one" 
    return render_template("login.html",error = error)

@app.get("/dashboard/<int:user_id>")
def get_dashboard(user_id):
    date_now = datetime.now()
    Month = date_now.strftime('%B')
    db_connection = get_db()
    cursor = db_connection.cursor()
    cursor.execute("SELECT User_First_Name, User_Last_Name, User_Email FROM User WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()
    first_name = user_data[0]
    last_name = user_data[1]
    user_email = user_data[2]
    quote, author = get_quote()
    total_expenses = calculate_total_expenses(user_id)
    percentage_savings = calculate_percentage_savings(user_id)
    savings = calculate_savings(user_id)
    total_percentages = find_total_percentage(user_id)
    total_income = calculate_total_income(user_id)
    expenses_data = get_expenses_data(user_id)
    daily_labels, daily_expenses = get_daily_expenses_data(user_id)
    expenses_data["dailyLabels"] = daily_labels
    expenses_data["dailyExpenses"] = daily_expenses
    financial_data = get_financial_data(user_id)
    return render_template("dashboard.html", user_id=user_id, first_name=first_name, last_name=last_name, user_email=user_email, total_expenses=total_expenses,percentage_savings=percentage_savings,savings = savings,
                           total_income = total_income, expenses_data=expenses_data, financial_data=financial_data,Month=Month,total_percentages=total_percentages, quote=quote, author=author)


@app.get("/expenses/<int:id>")
def expenses(id):
    db_connection = get_db()
    cursor = db_connection.cursor()

    # Fetch user details
    cursor.execute("SELECT User_First_Name, User_Last_Name, User_Email FROM User WHERE id = ?", (id,))
    user_data = cursor.fetchone()
    first_name = user_data[0]
    user_email = user_data[2]

    # Fetch expense entries
    entries = cursor.execute("SELECT User_First_Name,User_Email,Category, Expense, Date FROM Expenses JOIN User on Expenses.User_id == User.id WHERE User_id = ?", (id,))
    return render_template("expenses.html", id=id, entries=entries, first_name=first_name, user_email=user_email)


@app.route('/addexpenses/<int:id>', methods=['GET', 'POST'])
def addexpense(id):
    if request.method == 'POST':
        category = request.form['category']
        expense = request.form['expense']
        date_now = datetime.now()
        string = '%A, %d. %B %Y %I:%M%p'
        day_of_week = date_now.strftime('%A') 
        date = date_now.strftime(string)
        Current_Month_And_Year = date_now.strftime('%B, %Y')
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Expenses (User_id, Category, Expense, Date, DayOfWeek, MonthAndYear) VALUES (?, ?, ?, ?, ?, ?)', (id, category, expense, date, day_of_week, Current_Month_And_Year))
            conn.commit()
        flash('Details added successfully', 'success')
        return redirect(url_for('addexpense', id = id))
   
    if request.method == 'GET':
        db_connection = get_db()
        cursor = db_connection.cursor()
        cursor.execute("SELECT User_First_Name, User_Last_Name, User_Email FROM User WHERE id = ?", (id,))
        user_data = cursor.fetchone()
        first_name = user_data[0]
        user_email = user_data[2]
        return render_template("add_expenses.html", id = id,first_name=first_name, user_email=user_email)
    
@app.route('/addincome/<int:id>', methods=['GET', 'POST'])
def addincome(id):
    if request.method == 'POST':
        source = request.form['source']
        income = request.form['income']
        date_now = datetime.now()
        string = '%A, %d. %B %Y %I:%M%p'
        date = date_now.strftime(string)
        Current_Month_And_Year = date_now.strftime('%B, %Y')
        expense_color = Income_color.get(source, 'default_color')
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO  Incomes(User_id, Source, Income, Date, MonthAndYear,Percent, Color) VALUES (?, ?, ?, ?, ?, 0, ?)', (id, source, income, date, Current_Month_And_Year,expense_color))
            conn.commit()
          # Addition here
        expense_color = Income_color.get(source, 'default_color')
        with get_db() as conn:
            income_percentages(id)

        flash('Details added successfully', 'success')
        return redirect(url_for('addincome', id = id))

    if request.method == 'GET':
        db_connection = get_db()
        cursor = db_connection.cursor()
        cursor.execute("SELECT User_First_Name, User_Last_Name, User_Email FROM User WHERE id = ?", (id,))
        user_data = cursor.fetchone()
        first_name = user_data[0]
        user_email = user_data[2]
        return render_template("add_incomes.html", id = id,first_name=first_name, user_email=user_email )

    
@app.get("/income/<int:id>")
def income(id):
    db_connection = get_db()
    cursor = db_connection.cursor()

    cursor.execute("SELECT User_First_Name, User_Last_Name, User_Email FROM User WHERE id = ?", (id,))
    user_data = cursor.fetchone()
    first_name = user_data[0]
    user_email = user_data[2]

    entries = cursor.execute("SELECT User_First_Name,User_Email,Source, Income, Date FROM Incomes JOIN User on Incomes.User_id == User.id WHERE User_id = ?", (id,))
    return render_template("income.html", id=id, entries=entries, first_name=first_name, user_email=user_email)

@app.route('/summary/<int:id>', methods=['GET', 'POST'])
def summary(id):
    if request.method == 'GET':
        db_connection = get_db()
        cursor = db_connection.cursor()
        cursor.execute("SELECT User_First_Name, User_Last_Name, User_Email FROM User WHERE id = ?", (id,))
        user_data = cursor.fetchone()
        first_name = user_data[0]
        user_email = user_data[2]

        cursor.execute("SELECT User_First_Name, User_Email, Source, Income, Date FROM Incomes JOIN User on Incomes.User_id == User.id WHERE User_id = ?", (id,))
        incomes = cursor.fetchall()

        cursor.execute("SELECT User_First_Name, User_Email, Category, Expense, Date FROM Expenses JOIN User on Expenses.User_id == User.id WHERE User_id = ?", (id,))
        entries = cursor.fetchall()

        return render_template("summary.html", id=id, first_name=first_name, incomes=incomes, user_email=user_email, entries=entries)

    if request.method == 'POST':
        Month = request.form['month']
        selected_month = Month
        date_now = datetime.now()
        Current_Year = date_now.strftime('%Y')
        date = f"{Month}, {Current_Year}"
        db_connection = get_db()
        cursor = db_connection.cursor()
        cursor.execute("SELECT User_First_Name, User_Last_Name, User_Email FROM User WHERE id = ?", (id,))
        user_data = cursor.fetchone()
        first_name = user_data[0]
        user_email = user_data[2]
        cursor.execute("SELECT User_First_Name, User_Email, Source, Income, Date FROM Incomes JOIN User on Incomes.User_id == User.id WHERE User_id = ? AND MonthAndYear = ?", (id, date))
        incomes = cursor.fetchall()

        cursor.execute("SELECT User_First_Name, User_Email, Category, Expense, Date FROM Expenses JOIN User on Expenses.User_id == User.id WHERE User_id = ? AND MonthAndYear = ?", (id, date))
        entries = cursor.fetchall()

        return render_template('summary.html', id=id, entries=entries, first_name=first_name, user_email=user_email, incomes=incomes, date=date,selected_month=selected_month)
@app.route('/settings/<int:id>', methods=['GET', 'POST'])
def settings(id):
    if request.method == 'GET':
        db_connection = get_db()
        cursor = db_connection.cursor()
        cursor.execute("SELECT User_First_Name, User_Last_Name, User_Email FROM User WHERE id = ?", (id,))
        user_data = cursor.fetchone()
        first_name = user_data[0]
        user_email = user_data[2]
        return render_template('settings.html', id=id,first_name=first_name, user_email=user_email)
    if request.method == 'POST':
        First_name = request.form['first name']
        Surname = request.form['surname']
        email = request.form['email']
        db_connection = get_db()
        cursor = db_connection.cursor()
        cursor.execute('UPDATE User SET User_First_Name = ?, User_Last_Name = ?, User_Email = ? WHERE id = ?', (First_name, Surname, email, id))
        db_connection.commit()
        flash('Details added successfully', 'success')
        return redirect(url_for('settings', id = id))

@app.route('/change_email/<int:id>', methods=['GET', 'POST'])
def change_email(id):
    if request.method == 'GET':
        return render_template("change_email.html",id = id)
    
    if request.method == "POST":
        error = None
        old_email = request.form["email"]
        new_email = request.form["new_email"]
        password = request.form["password"]
        hashed_password = hash_text(password)
        db_connection = get_db()
        cursor = db_connection.cursor()
        cursor.execute("SELECT User_Password FROM User WHERE User_Email = ?", (old_email,))
        user_data = cursor.fetchone()
        user_password = user_data[0]
        if hashed_password == user_password:
            cursor.execute("UPDATE User SET User_Email = ? WHERE User_Email = ?",(new_email,old_email,)) 
            db_connection.commit()   
            return render_template("settings.html",id = id, error = error)
        else:
            error = "Incorrect password"
            return render_template("settings.html",id = id, error = error)
        
@app.route('/changepassword/<int:id>', methods=['GET', 'POST'])
def change_password(id):
    if request.method == 'GET':
        return render_template("changepassword.html",id = id)
    
    if request.method == "POST":
        error = None
        old_password = request.form["password"]
        new_password = request.form["new_password"]
        email = request.form["email"]
        old_hashed_password = hash_text(old_password)
        new_hashed_password = hash_text(new_password)
        db_connection = get_db()
        cursor = db_connection.cursor()
        cursor.execute("SELECT User_Password FROM User WHERE User_Email = ?", (email,))
        user_data = cursor.fetchone()
        user_password = user_data[0]
        if old_hashed_password == user_password:
            cursor.execute("UPDATE User SET User_Password = ? WHERE User_Email = ?",(new_hashed_password,email,))
            db_connection.commit()   
            return render_template("settings.html",id = id, error = error)
        else:
            error = "Incorrect password or email"
            return render_template("settings.html",id = id, error = error)



if __name__ == '__main__':
    app.run(debug=True)
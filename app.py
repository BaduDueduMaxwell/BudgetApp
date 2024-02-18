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

def get_progress_data_from_database():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT Percentage, Color FROM Budget')
        progress_data = cursor.fetchall()
    return progress_data 

def get_name_data():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT Color, Category, Percentage FROM Budget')
        get_name_data = cursor.fetchall()
    return get_name_data


@app.get("/dashboard")
def get_dashboard():
    progress_data = get_progress_data_from_database()
    get_data = get_name_data()
    return render_template("dashboard.html", progress_data=progress_data, get_data = get_data)

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


# Dictionary
Income_color = {
    'Allowance': 'red',
    'Bonus': 'purple',
    'Investment': 'green',
    'Investment': 'green',
    'Lottery': 'green',
    'Salary': 'green',
    'Tips': 'green',
    'Family': 'green',
    'Others': 'green',
}
# Dictionary end

def calculate_total_income():
    db_connection = get_db()
    cursor = db_connection.cursor()
    cursor.execute("SELECT SUM(VALUE) FROM Income")
    total_income = cursor.fetchone()[0]
    db_connection.close()
    return total_income if total_income else 0

def income_percentages():
    db_connection = get_db()
    cursor = db_connection.cursor()
    cursor.execute("SELECT SUM(VALUE) FROM Income")
    total_income = cursor.fetchone()[0] or 1
    cursor.execute("SELECT id, VALUE FROM Income")
    incomes = cursor.fetchall()
    for income_id, income_value in incomes:
        percentage = (income_value / total_income) * 100 if total_income else 0
        cursor.execute("UPDATE Income SET Percent = ? WHERE id = ?", (percentage, income_id))
    db_connection.commit()
    db_connection.close()




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
            
            cursor.execute('SELECT * FROM Budget WHERE Category = ?', (category,))


            # if budget_row:
            #     total_expenses = calculate_expense_sum_by_category(category)
            #     total = calculate_total_expenses()
            #     new_percentage = (total_expenses / total) * 100
            #     cursor.execute('UPDATE Budget SET Percentage = ?, Color = ? WHERE Category = ?', (new_percentage, expense_color, category))
            # else:
            #     total_expenses_category = int(expense)
            #     total_expenses_all = calculate_total_expenses()
            #     new_percentage = (total_expenses_category / total_expenses_all) * 100
            #     cursor.execute('INSERT INTO Budget (Category, Percentage, Color) VALUES (?, ?, ?)', (category, new_percentage, expense_color))
            
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
        expense_color = Income_color.get(source, 'default_color')
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Income (SOURCE, VALUE, MONTH, Percent, Color) VALUES (?, ?, ?, 0, ?)', (source, income, date, expense_color))
            income_percentages()
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
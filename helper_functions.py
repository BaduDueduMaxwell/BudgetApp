from flask import Flask, render_template,request,flash,url_for,redirect,session
import sqlite3, hashlib
import random
from datetime import datetime


quotes_dict = {
    "Being rich is having money; being wealthy is having time.": "Margaret Bonanno",
    "The only man who never makes mistakes is the man who never does anything.": "Theodore Roosevelt",
    "A dream doesn't become reality through magic; it takes sweat, determination and hard work.": "Colin Powell",
    "Money, like emotions, is something you must control to keep your life on the right track.": "Natasha Munson",
    "All our dreams can come true if we have the courage to pursue them.": "Walt Disney",
    "A formal education will make you a living; self-education will make you a fortune.": "Jim Rohn",
    "Timing, perseverance, and 10 years of trying will eventually make you look like an overnight success.": "Biz Stone",
    "Your work is going to fill a large part of your life, and the only way to be truly satisfied is to do what you believe is great work. And the only way to do great work is to love what you do.": "Steve Jobs",
    "There is no passion to be found playing small—in settling for a life that is less than the one you are capable of living.": "Nelson Mandela",
    "Patience and diligence, like faith, remove mountains.": "William Penn",
    "The only thing that overcomes hard luck is hard work.": "Harry Golden",
    "Don’t live the same day over and over again and call that a life. Life is about evolving mentally, spiritually, and emotionally.": "Germany Kent",
    "To live is to choose. But to choose well, you must know who you are and what you stand for, where you want to go and why you want to get there.": "Kofi Annan",
    "Financial freedom is available to those who learn about it and work for it.": "Robert Kiyosaki",
    "The greatest wealth is to live content with little.": "Plato",
    "Stay committed to your decisions, but stay flexible in your approach.": "Tony Robbins",
    "We all have dreams. But in order to make dreams come into reality, it takes an awful lot of determination, dedication, self-discipline, and effort.": "Jesse Owens",
    "Without leaps of imagination or dreaming, we lose the excitement of possibilities. Dreaming, after all, is a form of planning.": "Gloria Steinem",
    "If you want to be financially free, you need to become a different person than you are today and let go of whatever has held you back in the past.": "Robert Kiyosaki",
    "It’s not the man who has too little, but the man who craves more, that is poor.": "Seneca",
    "Do one thing every day that scares you.": "Eleanor Roosevelt","All successful people men and women are big dreamers. They imagine what their future could be, ideal in every respect, and then they work every day toward their distant vision, that goal or purpose.": "Brian Tracy",
    "The secret of getting ahead is getting started. The secret to getting started is breaking your complex overwhelming tasks into small manageable tasks and then starting on the first one.": "Mark Twain",
    "Our goals can only be reached through a vehicle of a plan, in which we must fervently believe, and upon which we must vigorously act. There is no other route to success.": "Pablo Picasso",
    "It’s better to look ahead and prepare than to look back and regret.": "Jackie Joyner-Kersee",
    "A good plan, violently executed now, is better than a perfect plan next week.": "George Patton",
    "Before you can become a millionaire, you must learn to think like one. You must learn how to motivate yourself to counter fear with courage.": "Thomas J. Stanley",
    "Be bold enough to use your voice, brave enough to listen to your heart, and strong enough to live the life you have always imagined.": "Anonymous",
    "Knowledge is power: you hear it all the time but knowledge is not power. It’s only potential power. It only becomes power when we apply it and use it. Somebody who reads a book and doesn’t apply it, they’re at no advantage over someone who’s illiterate. None of it works unless you work. We have to do our part. If knowing is half the battle, action is the second half of the battle.": "Jim Kwik",
    "Belief in oneself and knowing who you are … that's the foundation for everything great.": "Jay-Z",
    "To get rich, you have to be making money while you're asleep.": "David Bailey",
    "Diligence is the mother of good luck.": "Benjamin Franklin",
    "What you do speaks so loudly that I cannot hear what you say.": "Ralph Waldo Emerson",
    "The greater danger for most of us lies not in setting our aim too high and falling short; but in setting our aim too low, and achieving our mark.": "Michelangelo",
    "Don’t look for the needle in the haystack. Just buy the haystack.": "Jack Bogle",
    "There is a gigantic difference between earning a great deal of money and being rich.": "Marlene Dietrich",
    "Give me six hours to chop down a tree and I will spend the first four sharpening the axe.": "Abraham Lincoln",
    "If we command our wealth, we shall be rich and free. If our wealth commands us, we are poor indeed.": "Edmund Burke",
    "Follow your passion; it will lead you to your purpose.": "Oprah Winfrey",
    "A journey of a thousand miles must begin with a single step.": "Lao Tzu",
    "Forget about the fast lane. If you really want to fly, harness your power to your passion. Honor your calling. Everybody has one. Trust your heart, and success will come to you.": "Oprah Winfrey",
    "No one has ever become poor by giving.": "Anne Frank",
    "Everything is negotiable. Whether or not the negotiation is easy is another thing.": "Carrie Fisher",
    "Yesterday ended last night. Today is a brand-new day.": "Zig Ziglar",
    "Buy land. They’re not making it anymore.": "Mark Twain",
    "Don’t wait to buy real estate. Buy real estate and wait.": "Will Rogers",
    "Wealth is largely the result of habit.": "John Jacob Astor",
    "Making money is a hobby that will complement any other hobbies you have, beautifully.": "Scott Alexander",
    "Our greatest glory is not in never failing, but in rising every time we fall.": "Confucius",
    "Buying real estate is not only the best way, the quickest way, the safest way, but the only way to become wealthy.": "Marshall Field",
    "Passion is the genesis of genius.": "Tony Robbins",
    "The stock market is designed to transfer money from the active to the patient.": "Warren Buffett",
    "The major fortunes in America have been made in land.": "John D. Rockefeller",
    "Making money is certainly the one addiction I cannot shake.": "Felix Dennis","If you haven’t found it yet, keep looking. Don’t settle. As with all matters of the heart, you’ll know when you find it.": "Steve Jobs",
    "Do what you love. When you love your work, you become the best worker in the world.": "Uri Geller",
    "We should remember that good fortune often happens when opportunity meets with preparation.": "Thomas A. Edison",
    "If you want to live a happy life, tie it to a goal, not to people or things.": "Albert Einstein",
    "The key to making money is to stay invested.": "Suze Orman",
    "The way to achieve your own success is to be willing to help somebody else get it first.": "Iyanla Vanzant",
    "All you need is the plan, the road map, and the courage to press on to your destination.": "Earl Nightingale",
    "You can’t build a reputation on what you’re going to do.": "Confucius",
    "The best way to predict the future is to create it.": "Abraham Lincoln",
    "Making money from money is like aerobatics.": "Alisher Usmanov",
    "It takes as much energy to wish as it does to plan.": "Eleanor Roosevelt",
    "Making money is art and working is art and good business is the best art.": "Andy Warhol",
    "Making money is easy. It is. The difficult thing in life is not making it; it's keeping it.": "John McAfee",
    "Nothing wrong with making money.": "Adam Levine",
    "I don't believe in spending money lavishly, now that I'm making money.": "Ansel Elgort",
    "Make sure to save for the future and keep making money!": "Jam Master Jay",
    "I like the art of making money more than making money.": "Richard Rawlings",
    "The only point in making money is, you can tell some big shot where to go.": "Humphrey Bogart",
    "Focus on solving real problems and not on making money. There will be enough takers for your solutions. You will help make lives of some people better, and money will follow.": "Bhavish Aggarwal",
    "Succeeding in business is not just about making money.": "Daniel Snyder"
}

DATABASE = "database.db"

def get_db():
    connection = sqlite3.connect(DATABASE)
    return connection 

def hash_text(parameter):
    h=hashlib.new("SHA256")
    h.update(parameter.encode())
    hashed_password = h.hexdigest()
    return hashed_password

def calculate_total_expenses(user_id):
    db_connection = get_db()
    cursor = db_connection.cursor()
    date_now = datetime.now()
    Current_Month_And_Year = date_now.strftime('%B, %Y')
    cursor.execute("SELECT SUM(Expense) FROM Expenses WHERE User_id = ? AND MonthAndYear = ?", (user_id, Current_Month_And_Year))
    total_expenses = cursor.fetchone()[0]
    db_connection.close()
    return total_expenses if total_expenses else 0

def income_percentages(user_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(Income) FROM Incomes WHERE user_id = ?", (user_id,))
        total_income = cursor.fetchone()[0] or 1
        cursor.execute("SELECT id, Income FROM Incomes WHERE user_id = ?", (user_id,))
        incomes = cursor.fetchall()
        for income_id, income_value in incomes:
            percentage = (income_value / total_income) * 100 if total_income else 0
            percentage = round(percentage, 2)
            cursor.execute("UPDATE Incomes SET Percent = ? WHERE id = ?", (percentage, income_id))
        conn.commit()

def find_total_percentage(user_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT Source, Color FROM Incomes WHERE user_id = ?", (user_id,))
        sources = cursor.fetchall()
        total_percentages = {}
        for source, color in sources:
            cursor.execute("SELECT SUM(Percent) FROM Incomes WHERE Source = ? AND user_id = ?", (source,user_id))
            total_percentage = cursor.fetchone()[0] or 0
            total_percentages[source] = {'percentage': total_percentage, 'color': color}
    return total_percentages

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
    date_now = datetime.now()
    Current_Month_And_Year = date_now.strftime('%B, %Y')
    cursor.execute("SELECT SUM(Income) FROM Incomes WHERE User_id = ? AND MonthAndYear = ?", (user_id, Current_Month_And_Year))
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

def get_quote():
    quote, author = random.choice(list(quotes_dict.items()))
    return quote, author
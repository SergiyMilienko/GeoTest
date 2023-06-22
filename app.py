import os
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from database import create_database, create_table
from random_country import get_random_country
import sqlite3

create_database()
create_table()

# Configure application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
        return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Connect to database 
    with sqlite3.connect('geofact.db') as db:
        # User reached route via POST (as by submitting a form via POST)
        if request.method == "POST":

            # Ensure username was submitted
            if not request.form.get("username"):
                apology_message = "Enter your username"
                error_field = "username"

                return render_template("login.html", apology_message=apology_message, error_field=error_field)

            # Ensure password was submitted
            elif not request.form.get("password"):
                apology_message = "Enter your password"
                error_field = "password"

                return render_template("login.html", apology_message=apology_message, error_field=error_field)
            
            # Check if entered password is correct 
            rows = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
            row = rows.fetchone()
            if not row or not check_password_hash(row[2], request.form.get("password")):
                apology_message = "Invalid username/password"
                error_field = "password" and "username"
                return render_template("login.html", apology_message=apology_message, error_field=error_field)
            
            # Log user in
            session["user_id"] = row[0]
            session["username"] = row[1]

            # Redirect to main page
            return redirect("/")

        # User reached route via GET (as by clicking a link or via redirect)
        else:
            return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Connect to database 
    with sqlite3.connect('geofact.db') as db:
        # User reached route via POST (as by submitting a form via POST)
        if request.method == "POST":

            # Ensure username was submitted
            if not request.form.get("username"):
                apology_message = "Enter your username"
                error_field = "username"

                return render_template("register.html", apology_message=apology_message, error_field=error_field)

            # Ensure password was submitted
            elif not request.form.get("password"):
                apology_message = "Enter your password"
                error_field = "password"

                return render_template("register.html", apology_message=apology_message, error_field=error_field)
            
            # Ensure confirmation was submitted
            elif not request.form.get("confirmation"):
                apology_message = "Repeat your password"
                error_field = "confirmation"

                return render_template("register.html", apology_message=apology_message, error_field=error_field)

            # Variables to store username, password and confirmation
            username = request.form.get("username")
            password = request.form.get("password")
            confirmation = request.form.get("confirmation")
            hash = generate_password_hash(request.form.get("password"))
            
            # Check if the password and confirmation match
            if password != confirmation:
                apology_message = "Passwords don't match"
                error_field = "confirmation"

                return render_template("register.html", apology_message=apology_message, error_field=error_field)

            # Variable to store first row from result of command
            username_taken = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
            # Check if the username already exists
            if username_taken:
                apology_message = "Username is already taken"
                error_field = "username"
                return render_template("register.html", apology_message=apology_message, error_field=error_field)
            
            # Insert data in table
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash))

            # Redirect to main page
            return redirect("/")

        # User reached route via GET (as by clicking a link or via redirect)
        else:
            return render_template("register.html")

@app.route("/main")
def main():
        return render_template("main.html")

@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
    
@app.route("/play", methods=["GET", "POST"])
def play():
    if request.method == "POST":
        difficulty = request.form.get("difficulty")
        session["difficulty"] = difficulty
    
    country = get_random_country()
    session["score"] = 0
    session["count"] = 0
    session["guessed_countries"] = []
    session["random_country"] = country
    return render_template("mode1.html", country=country)

@app.route("/process_country", methods=["POST"])
def process_country():
    guessed_country = request.form.get("country")
    random_country = session.get("random_country")
    result = "❌" if guessed_country != random_country else "✅"
    if guessed_country == random_country:
        session["score"] += 1
        session["count"] += 1
        session["guessed_countries"].append(guessed_country)
    else:
        session["count"] += 1
    country = get_random_country()
    session["random_country"] = country  # Store the new random country in the session
    score = session.get("score")
    count = session.get("count")
    max_score = session.get("max_score")
    guessed_countries = session.get("guessed_countries")
    return render_template("mode1.html", country=country, random_country=random_country, result=result, score=score, guessed_countries=guessed_countries, max_score=max_score, count=count)

if __name__ == '__main__':
    app.run()
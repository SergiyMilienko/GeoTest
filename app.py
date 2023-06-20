import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, apology
import sqlite3
import random

# Create database or create it if it does not exist
conn = sqlite3.connect('geofact.db')

# Create a cursor object
cursor = conn.cursor()

# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    hash TEXT NOT NULL
                )''')

# Configure application
app = Flask(__name__)

popular_countries = ["Argentina", "Armenia", "Australia", "Austria", "Belgium", "Brazil", 
                     "Canada", "Chile", "China", "Czech Republic", "Denmark", "Finland", 
                     "France", "Germany", "Greece", "Hungary", "Iceland", "India", "Indonesia", 
                     "North Korea", "South Korea", "Mexico", "Mongolia", "Netherlands", "New Zealand", 
                     "Norway", "Pakistan", "Poland", "Portugal", "Russian Federation", "Saudi Arabia", "Slovakia", 
                     "Slovenia", "Spain", "Sweden", "Switzerland", "Syria", "South Africa", "Venezuela", 
                     "Vietnam", "United States", "United Kingdom", "Ukraine", "Turkey", "Iran", "Iraq", 
                     "Ireland", "Israel", "Italy", "Japan", "Latvia", "Lithuania", "Romania"]

less_popular_countries = ["Afghanistan", "Albania", "Algeria", "Azerbaijan", "Bangladesh", "Belarus", 
                          "Belize", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Bulgaria", 
                          "Cambodia", "Cameroon", "Central African Republic", "Chad", "Colombia", 
                          "Congo", "Croatia", "Cuba", "Ecuador", "Egypt", "El Salvador", "Estonia", 
                          "Ethiopia", "Georgia", "Ghana", "Guatemala", "Honduras", "Jamaica", "Jordan", 
                          "Kazakhstan", "Kenya", "Kyrgyzstan", "Kosovo", "Kuwait", "Laos", "Lebanon", 
                          "Liberia", "Libya", "Luxembourg", "Madagascar", "Malaysia", "Moldova", "Monaco", 
                          "Montenegro", "Morocco", "Namibia", "Nepal", "Nicaragua", "Nigeria", 
                          "North Macedonia", "Panama", "Papua New Guinea", "Paraguay", "Peru", 
                          "Philippines", "Qatar", "Serbia", "Zambia", "Zimbabwe", "United Arab Emirates", 
                          "Uzbekistan", "Yemen", "Singapore", "Somalia", "Sri Lanka", "Taiwan", 
                          "Tajikistan", "Tanzania", "Thailand", "Tunisia", "Turkmenistan", "Uganda", "Uruguay"]


least_popular_countries = ["Andorra", "Angola", "Antigua and Barbuda", "Bahamas", "Bahrain", "Barbados", "Benin", 
                           "Bhutan", "Brunei", "Burkina Faso", "Burundi", "Cabo Verde", "Comoros", "Costa Rica", 
                           "Cyprus", "Djibouti", "Dominica", "Dominican Republic", "Equatorial Guinea", "Eritrea", 
                           "Eswatini", "Fiji", "Gabon", "Gambia", "Grenada", "Guinea", "Guinea-Bissau", "Guyana", 
                           "Haiti", "Kiribati", "Lesotho", "Liechtenstein", "Malawi", "Maldives", "Mali", "Malta", 
                           "Marshall Islands", "Mauritania", "Mauritius", "Micronesia", "Mozambique", "Myanmar", 
                           "Nauru", "Niger", "Oman", "Palau", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", 
                           "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", 
                           "Senegal", "Seychelles", "Vatican City", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", 
                           "Suriname", "Sierra Leone", "Solomon Islands", "South Sudan", "Sudan", "Tuvalu", "Vanuatu"]

def get_random_country():
    guessed_countries = session.get("guessed_countries", [])
    all_countries = ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", 
    "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", 
    "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", 
    "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", 
    "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica", 
    "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic", 
    "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", 
    "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", 
    "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", 
    "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", 
    "Kenya", "Kiribati", "North Korea", "South Korea", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", 
    "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", 
    "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", 
    "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", 
    "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Macedonia", 
    "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", 
    "Poland", "Portugal", "Qatar", "Romania", "Russian Federation", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", 
    "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", 
    "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", 
    "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", 
    "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", 
    "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", 
    "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", 
    "Zambia", "Zimbabwe"]  # List of all countries
    available_countries = [country for country in all_countries if country not in guessed_countries]
    
    if available_countries:
        return random.choice(available_countries)
    else:
        return None

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

@app.route("/resetpassword")
def reset_password():
        return render_template("reset.html")

@app.route("/settings")
def settings():
        return render_template("reset.html")

@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
    
@app.route("/play", methods=["GET", "POST"])
def play():
    country = get_random_country()
    session["score"] = 0
    session["guessed_countries"] = []
    return render_template("mode1.html", country=country)

@app.route("/process_country", methods=["POST"])
def process_country():
    guessed_country = request.form.get("country")
    random_country = session.get("random_country")
    result = "❌" if guessed_country != random_country else "✅"
    if guessed_country == random_country:
        session["score"] += 1
        session["guessed_countries"].append(guessed_country)
    country = get_random_country()
    session["random_country"] = country  # Store the new random country in the session
    score = session.get("score")
    guessed_countries = session.get("guessed_countries")
    return render_template("mode1.html", country=country, random_country=random_country, result=result, score=score, guessed_countries=guessed_countries)



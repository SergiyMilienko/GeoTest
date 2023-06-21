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
                     "Ireland", "Israel", "Italy", "Japan", "Latvia", "Lithuania", "Romania", "Kazakhstan", 
                     "Estonia", "Belarus"]

less_popular_countries = ["Afghanistan", "Albania", "Algeria", "Azerbaijan", "Bangladesh",
                          "Belize", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Bulgaria", 
                          "Cambodia", "Cameroon", "Central African Republic", "Chad", "Colombia", 
                          "Congo", "Croatia", "Cuba", "Ecuador", "Egypt", "El Salvador", 
                          "Ethiopia", "Georgia", "Ghana", "Guatemala", "Honduras", "Jamaica", "Jordan", 
                          "Kenya", "Kyrgyzstan", "Kosovo", "Kuwait", "Laos", "Lebanon", 
                          "Liberia", "Libya", "Luxembourg", "Madagascar", "Malaysia", "Moldova", 
                          "Montenegro", "Morocco", "Namibia", "Nepal", "Nicaragua", "Nigeria", 
                          "North Macedonia", "Panama", "Papua New Guinea", "Paraguay", "Peru", 
                          "Philippines", "Qatar", "Serbia", "Zambia", "Zimbabwe", "United Arab Emirates", 
                          "Uzbekistan", "Yemen", "Singapore", "Somalia", "Sri Lanka", "Taiwan", 
                          "Tajikistan", "Tanzania", "Thailand", "Tunisia", "Turkmenistan", "Uganda", "Uruguay"]


least_popular_countries = ["Angola", "Antigua and Barbuda", "Bahamas", "Bahrain", "Barbados", "Benin", 
                           "Bhutan", "Brunei", "Burkina Faso", "Burundi", "Cabo Verde", "Comoros", "Costa Rica", 
                           "Cyprus", "Djibouti", "Dominica", "Dominican Republic", "Equatorial Guinea", "Eritrea", 
                           "Eswatini", "Fiji", "Gabon", "Gambia", "Grenada", "Guinea", "Guinea-Bissau", "Guyana", 
                           "Haiti", "Kiribati", "Lesotho", "Malawi", "Maldives", "Mali", "Malta", 
                           "Marshall Islands", "Mauritania", "Mauritius", "Micronesia", "Mozambique", "Myanmar", 
                           "Nauru", "Niger", "Oman", "Palau", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", 
                           "Saint Vincent and the Grenadines", "Samoa", "Sao Tome and Principe", 
                           "Senegal", "Seychelles", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", 
                           "Suriname", "Sierra Leone", "Solomon Islands", "South Sudan", "Sudan", "Tuvalu", "Vanuatu"]

all_countries = ["Afghanistan", "Albania", "Algeria", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", 
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
    "Lebanon", "Lesotho", "Liberia", "Libya", "Lithuania", "Luxembourg", "Madagascar", 
    "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", 
    "Mexico", "Micronesia", "Moldova", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", 
    "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Macedonia", 
    "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", 
    "Poland", "Portugal", "Qatar", "Romania", "Russian Federation", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", 
    "Saint Vincent and the Grenadines", "Samoa", "Sao Tome and Principe", "Saudi Arabia", 
    "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", 
    "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", 
    "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", 
    "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", 
    "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Yemen", 
    "Zambia", "Zimbabwe"]

africa = [
    "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi",
    "Cabo Verde", "Cameroon", "Central African Republic", "Chad", "Comoros",
    "Congo", "Côte d'Ivoire", "Djibouti", "Egypt", "Equatorial Guinea", "Eritrea",
    "Eswatini", "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau",
    "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania",
    "Mauritius", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda",
    "São Tomé and Príncipe", "Senegal", "Seychelles", "Sierra Leone", "Somalia",
    "South Africa", "South Sudan", "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda",
    "Zambia", "Zimbabwe"
]

asia = [
    "Afghanistan", "Armenia", "Azerbaijan", "Bahrain", "Bangladesh", "Bhutan",
    "Brunei", "Cambodia", "China", "Cyprus", "Georgia", "India", "Indonesia",
    "Iran", "Iraq", "Israel", "Japan", "Jordan", "Kazakhstan", "Kuwait", "Kyrgyzstan",
    "Laos", "Lebanon", "Malaysia", "Maldives", "Mongolia", "Myanmar", "Nepal",
    "North Korea", "Oman", "Pakistan", "Palestine", "Philippines", "Qatar", "Russia",
    "Saudi Arabia", "Singapore", "South Korea", "Sri Lanka", "Syria", "Taiwan",
    "Tajikistan", "Thailand", "Timor-Leste", "Turkey", "Turkmenistan", "United Arab Emirates",
    "Uzbekistan", "Vietnam", "Yemen"
]

europe = [
    "Albania", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina",
    "Bulgaria", "Croatia", "Czech Republic", "Denmark", "Estonia", "Finland", "France",
    "Germany", "Greece", "Hungary", "Iceland", "Ireland", "Italy", "Kosovo", "Latvia",
    "Lithuania", "Luxembourg", "Malta", "Moldova", "Montenegro",
    "Netherlands", "North Macedonia", "Norway", "Poland", "Portugal", "Romania",
    "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine",
    "United Kingdom"
]

north_america = [
    "Antigua and Barbuda", "Bahamas", "Barbados", "Belize", "Canada", "Costa Rica",
    "Cuba", "Dominica", "Dominican Republic", "El Salvador", "Grenada", "Guatemala",
    "Haiti", "Honduras", "Jamaica", "Mexico", "Nicaragua", "Panama", "Saint Kitts and Nevis",
    "Saint Lucia", "Saint Vincent and the Grenadines", "Trinidad and Tobago", "United States"
]

oceania = [
    "Australia", "Fiji", "Kiribati", "Marshall Islands", "Micronesia", "Nauru",
    "New Zealand", "Palau", "Papua New Guinea", "Samoa", "Solomon Islands", "Tonga",
    "Tuvalu", "Vanuatu"
]

south_america = [
    "Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Guyana",
    "Paraguay", "Peru", "Suriname", "Uruguay", "Venezuela"
]

def get_random_country():
    difficulty = session.get("difficulty")
    guessed_countries = session.get("guessed_countries", [])
    available_countries = [country for country in all_countries if country not in guessed_countries]
    
    if difficulty == "easy":
        available_countries = popular_countries
        session["max_score"] = len(popular_countries)
    elif difficulty == "medium":
        available_countries = less_popular_countries
        session["max_score"] = len(less_popular_countries)
    elif difficulty == "hard":
        available_countries = least_popular_countries
        session["max_score"] = len(least_popular_countries)
    elif difficulty == "all":
        available_countries = all_countries
        session["max_score"] = len(all_countries)
    elif difficulty == "europe":
        available_countries = europe
        session["max_score"] = len(europe)
    elif difficulty == "asia":
        available_countries = asia
        session["max_score"] = len(asia)
    elif difficulty == "oceania":
        available_countries = oceania
        session["max_score"] = len(oceania)
    elif difficulty == "north_america":
        available_countries = north_america
        session["max_score"] = len(north_america)
    elif difficulty == "south_america":
        available_countries = south_america
        session["max_score"] = len(south_america)
    elif difficulty == "africa":
        available_countries = africa
        session["max_score"] = len(africa)


    available_countries = [country for country in available_countries if country not in guessed_countries]

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
    if request.method == "POST":
        difficulty = request.form.get("difficulty")
        session["difficulty"] = difficulty
    
    country = get_random_country()
    session["score"] = 0
    session["count"] = 0
    session["guessed_countries"] = []
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



import os
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from database import create_database, create_table
from random_country import get_random_country
import sqlite3

create_database()
create_table()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
        return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    with sqlite3.connect('geotest.db') as db:
        if request.method == "POST":
            if not request.form.get("username"):
                apology_message = "Enter your username"
                error_field = "username"
                return render_template("login.html", apology_message=apology_message, error_field=error_field)
            elif not request.form.get("password"):
                apology_message = "Enter your password"
                error_field = "password"
                return render_template("login.html", apology_message=apology_message, error_field=error_field)
            rows = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
            row = rows.fetchone()
            if not row or not check_password_hash(row[2], request.form.get("password")):
                apology_message = "Invalid username/password"
                error_field = "password" and "username"
                return render_template("login.html", apology_message=apology_message, error_field=error_field)
            session["user_id"] = row[0]
            session["username"] = row[1]
            return redirect("/")
        else:
            return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    with sqlite3.connect('geotest.db') as db:
        if request.method == "POST":
            if not request.form.get("username"):
                apology_message = "Enter your username"
                error_field = "username"
                return render_template("register.html", apology_message=apology_message, error_field=error_field)
            elif not request.form.get("password"):
                apology_message = "Enter your password"
                error_field = "password"
                return render_template("register.html", apology_message=apology_message, error_field=error_field)
            elif not request.form.get("confirmation"):
                apology_message = "Repeat your password"
                error_field = "confirmation"
                return render_template("register.html", apology_message=apology_message, error_field=error_field)
            username = request.form.get("username")
            password = request.form.get("password")
            confirmation = request.form.get("confirmation")
            hash = generate_password_hash(request.form.get("password"))
            if password != confirmation:
                apology_message = "Passwords don't match"
                error_field = "confirmation"
                return render_template("register.html", apology_message=apology_message, error_field=error_field)
            username_taken = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
            if username_taken:
                apology_message = "Username is already taken"
                error_field = "username"
                return render_template("register.html", apology_message=apology_message, error_field=error_field)
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash))
            return redirect("/")
        else:
            return render_template("register.html")

@app.route("/mode")
def mode():
        return render_template("mode.html")

@app.route("/logout")
def logout():
    session.clear()
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
    return render_template("play.html", country=country)

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
    session["random_country"] = country
    score = session.get("score")
    count = session.get("count")
    max_score = session.get("max_score")
    guessed_countries = session.get("guessed_countries")
    return render_template("play.html", country=country, random_country=random_country, result=result, score=score, guessed_countries=guessed_countries, max_score=max_score, count=count)

if __name__ == '__main__':
    app.run()
# GeoTest
## Introduction:
GeoTest is a Flask-based web application that allows users to play a game where they have to locate countries on a map. It incorporates features such as user registration, login/logout functionality, game scoring, and random country generation. The application is built using Python, SQLite, HTML, CSS, and JavaScript.

## Routes
GeoTest defines the following routes:

1. GET "/": Renders the home page with a link to the game.
2. GET/POST "/login": Renders the login page and handles user login.
3. GET/POST "/register": Renders the registration page and handles user registration.
4. GET "/mode": Renders the game mode selection page.
5. GET "/logout": Logs out the user and redirects to the login page.
6. GET/POST "/play": Renders the game page and handles game difficulty selection.
7. POST "/process_country": Handles the form submission from the game page and processes the guessed country.

## Static Files
The static files used in GeoTest, such as CSS and JavaScript files, are stored in the static directory. The static files include the following:

## Database
GeoTest uses SQLite for its database management. The database is created using the create_database() function from the database.py module, and the necessary table is created using the create_table() function from the same module. The SQLite database file is named geotest.db and is located in the project directory.

The database schema consists of a single table named "users" with the following columns:

id: An auto-incrementing integer primary key.
username: A string representing the user's username.
hash: A string representing the hashed password.
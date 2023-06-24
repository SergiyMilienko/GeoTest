# **GeoTest**
Hello! My name is Serhii Milienko and this is my final project for CS50 course. 
## **Introduction**:
This is my Flask-based web application that allows users to test their knowledge of world geography through an interactive game. Users can register an account, log in, and play the game where they have to locate countries on a map. The application is built using Python, SQLite, HTML, CSS, and JavaScript.

## **Project Structure**
- **app.py:** The main Python file containing the Flask application and the routes for handling different endpoints.
- **random_country.py:** A module containing a function to retrieve a random country for the game.
- **database.py:** A module containing functions to create the SQLite database and table.
- **countries_lists.py:** A module containing lists of countries based on their continent or recognizability 
- **geotest.db:** SQlite database for storing usernames and hashed passwords 
- **index.html:** The HTML template for the index page, which serves as the landing page of the application.
- **map.html:** The HTML template for the page that displays the map and handles country selection.
- **mode.html:** The HTML template for the mode selection page, where users can choose the difficulty level of the game.
- **play.html:** The HTML template for the game page, which displays the country to be identified and the user's score.
- **login.html:** The HTML template for the login page, where users can enter their credentials to log in.
- **register.html:** The HTML template for the registration page, where users can create a new account.
- **static/index.css:** The CSS file for styling the index page.
- **static/login.css:** The CSS file for styling the login page.
- **static/register.css:** The CSS file for styling the register page.
- **static/mode.css:** The CSS file for styling the mode selection page.
- **static/play.css:** The CSS file for styling the game page.
- **static/play.js:** The JavaScript file for handling interactions on the game page.
- **static/login&register.js:** The JavaScript file for handling interactions on the login and register pages.


### **app.py**
### **random_country.py**
### **database.py:**
### **countries_lists.py:**
### **geotest.db:**
### **index.html:**
### **map.html:**
### **mode.html:**
### **play.html:**
### **login.html:**
### **register.html:**
### **static/mode.css:**
### **static/play.css:**
### **static/play.js:**
### **static/login&register.js:**

## **Routes**

The GeoTest application includes the following routes:
- /: The index route, which serves as the landing page of the application.
- /login: The route for user login. Accepts both GET and POST requests.
- /register: The route for user registration. Accepts both GET and POST requests.
- /mode: The route for selecting the difficulty level of the game.
- /logout: The route for user logout.
- /play: The route for playing the game. Accepts both GET and POST requests.
- /process_country: The route for processing the user's guess in the game. Accepts POST requests.

## **Libraries**

- **os**: 
- **Flask**: 
- **Flask-Session**: 
- **werkzeug.security**: 
- **sqlite3**: 
- **random**: 
# **GeoTest**
Hello! My name is Serhii Milienko and this is my final project for CS50 course. 
## **Introduction**:
This is my Flask-based web application that allows users to test their knowledge of world geography through an interactive game. Users can register an account, log in, and play the game where they have to locate countries on a map. The application is built using Python, SQLite, HTML, CSS, and JavaScript.

## **Project Structure**
### **app.py**
The main Python file containing the Flask application and the routes for handling different endpoints including: 
- **/:** The index route, which serves as the landing page of the application.
- **/login:** The route for user login. Accepts both GET and POST requests.
- **/register:** The route for user registration. Accepts both GET and POST requests.
- **/mode:** The route for selecting the difficulty level of the game.
- **/logout:** The route for user logout.
- **/play:** The route for playing the game. Accepts both GET and POST requests.
- **/process_country:** The route for processing the user's guess in the game. Accepts POST requests.

Several libraries are used for different purposes:

- **os:** used here to generate a random secret key for the Flask application.

- **Flask:** used to create the Flask application instance and define routes and views:

- - **render_template:** used to render the HTML templates and pass data to them.

- -  **request:** used to handle data submitted through forms and retrieve values from HTTP requests.

- - **session:** used to store and retrieve session data, such as user IDs, usernames, and game score.

- **Flask-Session:** used to configure and manage sessions in the Flask application.

- **sqlite3:** used here to interact with an SQLite database, create tables, execute queries, and fetch data.

- **werkzeug.security:** provides password hashing utilities: 
- - **check_password_hash:**  used to compare hashed passwords
- - **generate_password_hash:** used to hash passwords before storing them in the database.

**Code Summary:** After importing all the necessary modules and libraries, we call externally defined `create_database()` and `create_table()` to create SQdatabase and table. Then we create a Flask application instance: `app = Flask(__name__)` and set random secret key using `os.urandom(24)`. After this we set `SESSION_PERMANENT` to `False` to make the session temporary.
Set `SESSION_TYPE` to `"filesystem"` to store session data on the server's filesystem. Initialize Session with the Flask application - `Session(app)`. Then we define `after_request` decorator 
By decorating the `after_request` function with `@app.after_request`, we ensure that it is automatically called after each request and can modify the response headers It also ensures that the responses from the Flask application are not cached by the client. After this we define the route handlers including `/`, `/login`, `/register`, `/mode`, `/logout`, `/play`, `/process_country`. The code is ending with `if __name__ == '__main__': app.run()`, a conditional block which makes sure the Flask application is only runned when executed directly, not as a module. 
### **random_country.py**
A module containing a function get_random_country() to retrieve a random country for the game. Uses the "session" object from Flask to store and retrieve data.

First it retrieves the difficulty level ans list of countries which are already guessed. Based on user choice of difficulty, it selects corresponding list of countries from countries_lists.py where all the lists are stored. Selected list is stored in available_countries variable. 

Next the function randomly selects one country from list and returns it. If user correctly located it on the map it gets gemoved from the available_countries list.It happens until list is empty. 

Empty available_countries list is indicating that user guessed all the  countries. In this case list guessed_countries resets and random country is no longer displayed until user will start a new game 


### **database.py:**
A module containing functions to create the SQLite database and table.

**create_database():** This function is responsible for creating the SQLite database file (geotest.db) if it doesn't already exist. It utilizes the sqlite3 library to establish a connection to the database file and executes a SQL query to create the necessary table.

**create_table():** This function creates the table users within the database. It defines the table's schema, including the columns for id (auto-incrementing integer), username (text), and password (text).
### **countries_lists.py:**
A module containing lists of countries based on their continent or recognizability 

**popular_countries:** This list contains popular and well-known countries from different continents.

**less_popular_countries:** This list contains countries that are less popular or less commonly known compared to the popular_countries list.

**least_popular_countries:** This list contains countries that are relatively less recognized or known compared to the popular_countries and less_popular_countries lists.

**all_countries:** This list contains all countries from around the world, regardless of their popularity or recognizability.

**africa:** This list contains countries that belong to the African continent.

**asia:** This list contains countries that belong to the Asian continent.

**europe:** This list contains countries that belong to the European continent.

**north_america:** This list contains countries that belong to the North American continent.

**oceania:** This list contains countries that belong to the Oceania region.

**south_america:** This list contains countries that belong to the South American continent.
### **geotest.db:**
SQlite database for storing usernames and hashed password for user authentication and registration.

### **index.html:**
The HTML template for the index page, which serves as the landing page of the application.

It sets the background, defines headings, styles the start button, and provides a navigation bar. The styles are also adjusted for responsive design 

### **map.html:**
The HTML template for the page that displays the map and handles country selection.

It contains an interactive SVG map (source: https://simplemaps.com/) with zoom controls and clickable country shapes. It includes a form to capture the selected country and submit it to the server for further processing.
### **mode.html:**
The HTML template for the mode selection page, where users can choose the difficulty level of the game.

It represents a page for the GeoTest application's gameplay section, providing navigation links, a form for selecting game options, and a basic layout using CSS styles.

- The available difficulty levels are "easy," "medium," and "hard."

- The available regions include "all countries," "Europe," "Asia," "Africa," "North America," "South America," and "Oceania."

### **play.html:**
The HTML template for the game page, which displays the country to be identified and the user's score.

It includes navigation links, conditional rendering of game-related elements based on the game state, and the inclusion of external CSS and JavaScript files for styling and interactivity.

### **login.html:**
The HTML template for the login page, where users can enter their credentials to log in. Represents a simple login page with input fields for username and password, a login button, and links for registration and going back.

### **register.html:**
The HTML template for the registration page, where users can create a new account. Represents a registration page with input fields for username, password, and password confirmation, a registration button, and a button to go back.

### **static/index.css:**
The CSS file for styling the index page. Includes styling rules for the body element, h1 headings, text highlighting, start button, top navigation bar, and media queries for responsiveness.

### **static/login.css:**
The CSS file for styling the login page. Includes styling rules for the body element, h1 headings, text highlighting, start button, top navigation bar, and media queries for responsiveness.

### **static/register.css:**
The CSS file for styling the register page.Includes styling rules for the body element, h1 headings, text highlighting, start button, top navigation bar, and media queries for responsiveness.

### **static/mode.css:**
The CSS file for styling the mode selection page. Includes styling rules for the body element, h1 headings, text highlighting, start button, top navigation bar, and media queries for responsiveness.

### **static/play.css:**
The CSS file for styling the game page. Includes styling rules for the body element, h1 headings, text highlighting, start button, top navigation bar, and media queries for responsiveness.

### **static/play.js:**
The JavaScript file for handling interactions on the game page.

### **static/login&register.js:**
The JavaScript file for handling interactions on the login and register pages.

## **Libraries**

- **os**: 
- **Flask**: 
- **Flask-Session**: 
- **werkzeug.security**: 
- **sqlite3**: 
- **random**: 
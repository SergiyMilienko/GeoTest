# **GeoTest**
Hello! My name is Serhii Milienko and this is my final project for CS50 course. 
## **Introduction**:
This is my Flask-based web application that allows users to test their knowledge of world geography through an interactive game. Users can register an account, log in, and play the game where they have to locate countries on a map. The application is built using Python, SQLite, HTML, CSS, and JavaScript.

The project can be accessed via the following website: http://sergiymilienko.pythonanywhere.com/
## **How to play**
1. Click on the "Register" link on the landing page.
2. Fill in the required information, including a username and password.
3. Click the "Register" button to create your account.
4. After registering, you can log in by clicking on the "Login" link on the landing page.
5. Enter your username and password
6. Click the "Login" button.
7. Once logged in, you will be redirected to the mode selection page.
8. Choose the difficulty level you prefer or the region you want to focus on to start the game. 
9. On the game page, you will see the name of a country displayed.
10. Use the interactive map to locate the country based on its shape and position. You can zoom in and zoom out the map. 
11. Click on the correct location on the map to make your guess.
12. After each guess, your score will be displayed on the game page.
13. If your guess is correct, the country shape will be colored in turquoise and "✅" will pop up.
14. If your guess is incorrect, "❌" will pop up.
15. The game will continue until you've used all of given attempts to guess all the countries (attempts = number of countries in chosen area or difficulty).
16. After game is over you'll be able to see your final score and start a new game by clicking "Play Again" button.

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

**Code Summary:** After importing all the necessary modules and libraries, we call externally defined `create_database()` and `create_table()` to create SQdatabase and table. Following this,a Flask application instance is created: `app = Flask(__name__)`. To enhance security random secret key is set using `os.urandom(24)` for securely signing the session cookie. After this `SESSION_PERMANENT` is set to `False` to make the session temporary. Also `SESSION_TYPE` is set to `"filesystem"` to store session data on the server's filesystem. Session with the Flask application is initialized with `Session(app)`. Next `after_request` decorator  is defined. By decorating the `after_request` function with `@app.after_request`, we ensure that it is automatically called after each request and can modify the response headers. It also ensures that the responses from the Flask application are not cached by the client. After this the route handlers is defined, including `/`, `/login`, `/register`, `/mode`, `/logout`, `/play`, `/process_country`. The code is ending with `if __name__ == '__main__': app.run()`, a conditional block which makes sure the Flask application is only runned when executed directly, not as a module. 
### **random_country.py**
A module containing a function `get_random_country()` to retrieve a random country for the game using. Uses the "session" object from Flask to store and retrieve data.

First it retrieves the difficulty level and list of countries which are already guessed using `session.get`. Based on user choice of difficulty, it selects corresponding list of countries from `countries_lists.py` where all the lists are stored. Selected list is stored in `available_countries` variable. Also the maximal score possible is difined for chosen list 

Next the function randomly selects one country from list and returns it. If user correctly located it on the map it gets gemoved from the `available_countries` list. It happens until used used all of given attempts.

Empty `available_countries` list is indicating that user guessed all the countries. In this case list guessed_countries resets and random country is no longer displayed until user will start a new game.

### **database.py:**
A module containing functions to create the SQLite database and table.

**create_database():** This function is responsible for creating the SQLite database file (geotest.db) if it doesn't already exist. It utilizes the sqlite3 library to establish a connection to the database file and executes a SQL query to create the necessary table.

**create_table():** This function creates the table users within the database. It defines the table's schema, including the columns for id (auto-incrementing integer), username (text), and password (text).

### **countries_lists.py:**
A module containing python lists of countries based on their continent or recognizability 

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

It sets the background, defines headings, styles the start button, and provides a navigation bar. The styles are also adjusted for responsive design.

Viewport Meta Tag: `meta name="viewport" content="width=device-width, initial-scale=1.0"` sets the viewport properties for responsive web design.

 `nav class="topnav"`defines a navigation bar at the top of the page. It contains a logo and menu links.

 The logo and page title are represented by the `<a>` element and styled using CSS classes. The logo consists of the words "Geo" and "Test". They are colored in white and turquoise using `<span class="">`

The menu links are represented by `<a>` elements inside the `<div class="topnav-right">` container. The links include "Login" and "Register" if the user is not logged in, and "Logout" if the user is logged in.

Heading: `<h1>` displays a heading for the page with the text "Test your Geo Knowledge". The heading uses CSS classes for styling.

 `<form action="/mode">` creates a form that submits to the "/mode" URL when the button is clicked. The button is represented by `<button class="start" type="submit">` with the text "Play" inside.
### **map.html:**
The HTML template for the page that displays the map and handles country selection.

It contains an interactive SVG map (source: https://simplemaps.com/) with zoom controls and clickable country shapes. It includes a form to capture the selected country and submit it to the server for further processing.

`<div class="mapdiv">` represents a container for the map.

`<div class="zoom-controls">` contains zoom control buttons for the map.

`<form action="/process_country" method="POST">` creates a form that will be submitted to the "/process_country" URL using the POST method.

`<input type="hidden" id="countryInput" name="country">` defines a hidden input field named "country" that will be included in the form submission. The value of this field will be populated when a country is clicked on the map.

When a country is clicked, the `handleCountryClick` function is triggered, passing the country name as an argument.
### **mode.html:**
The HTML template for the mode selection page, where users can choose the difficulty level of the game.

It represents a page for the GeoTest application's gameplay section, providing navigation links, a form for selecting game options, and a basic layout using CSS styles.

- The available difficulty levels are "easy," "medium," and "hard."

- The available regions include "all countries," "Europe," "Asia," "Africa," "North America," "South America," and "Oceania."

`<div class="topnav-centered">` contains navigation items that are centered horizontally.

`{% if session.user_id %}...{% endif %}` is a conditional statement using template tags. If a user is logged in, a username is displayed.

`<form action="/play" method="post">` creates a form that will be submitted to the "/play" URL using the POST method. 

A series of `<button>` elements are used to select different difficulty levels or specific regions for the GeoTest game. Each button has a unique value assigned to the "difficulty" attribute, which will be included in the form submission when clicked.
`<form action="/play" method="post">` creates a form that will be submitted to the "/play" URL using the POST method. 

### **play.html:**
The HTML template for the game page, which displays the country to be identified and the user's score.

It includes navigation links, conditional rendering of game-related elements based on the game state, and the inclusion of external CSS and JavaScript files for styling and interactivity.

`<div class="container">...</div> and <div class="Quiz">...</div>` represent containers for displaying quiz-related information. The content within these sections is conditionally displayed based on the value of the "count" variable.

`<h1>Find <span id="country" class="highlight_tur">{{ country }}</span> on the map! </h1>` displays the prompt for the game, with the name of a country highlighted.

`<h1> Your score: {{ score }}/{{ max_score }} </h1>` displays the user's score if the game has ended (when "count" is equal to "max_score") or if the user has scored higher than or equal to the maximum possible score.

`<a href="/mode" class="start">Play Again</a>` provides a link to start the game again. It is displayed when the quiz has ended.

`<div class="container">...</div> and <div class="Quiz2">...</div>` represent containers for displaying guess result and the user's score.

`<h1>Score: {{ score }}</h1>` displays the user's score.

`<h1>{{ result }} </h1>` displays the result of the guess.

`{% include "map.html" %}` includes an SVG map HTML file named "map.html" in the current position. 
### **login.html:**
The HTML template for the login page, where users can enter their credentials to log in. Represents a simple login page with input fields for username and password, a login button, and links for registration and going back.

`<button id="backButton" onclick="goBack()"></button>` represents a button with the id `"backButton"` that triggers the `goBack()` function when clicked. 

`<form action="/login" method="post">...</form>` represents a form for user login. The form sends a POST request to the "/login" URL when submitted.

`<input autocomplete="off" autofocus class="form-control mx-auto w-auto input" id="username" name="username" placeholder="Username" type="text">` represents an input field for the username.

`<input class="form-control mx-auto w-auto input" id="password" name="password" placeholder="Password" type="password">` represents an input field for the password. 

`<button class="start" type="submit">Login</button>` is a button element that triggers form submission when clicked. It submits the form data to the "/login" URL.

`{% if apology_message %}...</div>{% endif %}` is a conditional block that checks if the `"apology_message"` has to be displayed depending on the user input corectness. 

`<p class="register-now">...</p>` displays a message to register for an account If user doesn't have one.
### **register.html:**
The HTML template for the registration page, where users can create a new account. Represents a registration page with input fields for username, password, and password confirmation, a registration button, and a button to go back.

`<button id="backButton" onclick="goBack()"></button>` represents a button with the id `"backButton"` that triggers the `goBack()` function when clicked. 

`<input autocomplete="off" autofocus class="form-control mx-auto w-auto input" id="username" name="username" placeholder="Username" type="text">` represents an input field for the username. 

`<input class="form-control mx-auto w-auto input" id="password" name="password" placeholder="Password" type="password">` represents an input field for the password.

`<input class="form-control mx-auto w-auto input" id="password" name="password" placeholder="Password" type="password">` represents an input field for the password. It has CSS classes for styling and an attribute for the input type set to "password" for secure text entry.

`<button class="start" type="submit">Register</button>` is a button element that triggers form submission when clicked. It submits the form data to the "/register" URL.

`{% if apology_message %}...</div>{% endif %}` is a conditional block that checks if the `"apology_message"` has to be displayed depending on the user input corectness. 

### **static/index.css | login.css | register.css | mode.css | play.css:**
The CSS files for styling the corresponding HTML pages. They include styling rules for the `body` element, `h1` headings, text `highlighting`, `start` button, top `navigation bar`, `map` design configuration and `media queries` for responsiveness.

### **static/play.js:**
The JavaScript file for handling interactions on the game page.

**Country click detection to check the user's guess:**
function `handleCountryClick(countryName) { ... }`: This function is triggered when a country on the map is clicked. It takes the country name as a parameter,finds an element with the ID "countryInput" and sets its value to the clicked country name. Also it submits the first form on the page using the submit() method.

**Zoom in and Zoom out function:**
`window.addEventListener('DOMContentLoaded', function() { ... });`: This code adds an event listener to the `DOMContentLoaded` event, which fires when the initial HTML document has been completely loaded and parsed.

`var svgElement = document.querySelector('.mapdiv svg');`: It selects the SVG element within an element with the class `"mapdiv"` and assigns it to the `svgElement` variable.

`var zoomLevel = 1;`: It initializes the `zoomLevel` variable to 1, representing the initial zoom level.

`var isDragging = false;`: It initializes the `isDragging` variable to `false`, indicating whether the mouse is being dragged.

`var prevX = 0; and var prevY = 0;`: They initialize the `prevX` and `prevY` variables to 0, representing the previous mouse coordinates.

`var viewBoxX = 0; and var viewBoxY = 0;`: They initialize the `viewBoxX` and `viewBoxY` variables to 0, representing the initial coordinates of the viewBox attribute of the SVG element.

function `zoomIn() { ... }:` It increases the `zoomLevel` by 1 (up to a maximum of 20) and calls the `updateZoom()` function.

`function zoomOut() { ... }`: It decreases the `zoomLevel` by 1 (down to a minimum of 1) and calls the `updateZoom()` function.

`function updateZoom() { ... }`: It applies the current `zoomLevel` to the SVG element by setting the transform CSS property using a template literal.

`function handleMouseWheel(event) { ... }`: This function is triggered when a mouse wheel event occurs. It prevents the default scroll behavior, determines the scroll direction, and calls either the `zoomIn()` or `zoomOut()` function based on the scroll direction.

`function handleMouseDown(event) { ... }`: This function is triggered when the mouse is pressed down. It sets the `isDragging` variable to true and stores the current mouse coordinates in the `prevX` and `prevY` variables.

`function handleMouseUp(event) { ... }`: This function is triggered when the mouse button is released. It sets the `isDragging` variable to false.

`function handleMouseMove(event) { ... }`: This function is triggered when the mouse is moved. If `isDragging` is true, it calculates the distance moved by comparing the current and previous mouse coordinates, updates the `viewBoxX` and `viewBoxY` variables based on the movement, and sets the new `viewBox` attribute of the SVG element using the `setAttribute()` method.

`document.querySelector('.zoom-controls .zoom-in').addEventListener('click', zoomIn);`: It selects the element with the class `"zoom-in"` within an element with the class `"zoom-controls"` and adds a click event listener that calls the `zoomIn()` function when clicked.

`document.querySelector('.zoom-controls .zoom-out').addEventListener('click', zoomOut);`: It selects the element with the class `"zoom-out"` within an element with the class `"zoom-controls"` and adds a click event listener that calls the `zoomOut()` function when clicked.

`document.addEventListener('wheel', handleMouseWheel);`: It adds a wheel event listener to the entire document that calls the `handleMouseWheel()` function when a mouse wheel event occurs.

`document.addEventListener('mousedown', handleMouseDown);`: It adds a mousedown event listener to the entire document that calls the `handleMouseDown()` function when the mouse button is pressed down.

`document.addEventListener('mousemove', handleMouseMove);`: It adds a mousemove event listener to the entire document that calls the `handleMouseMove()` function when the mouse is moved.

`document.addEventListener('mouseup', handleMouseUp);`: It adds a mouseup event listener to the entire document that calls the `handleMouseUp()` function when the mouse button is released.

### **static/login&register.js:**
The JavaScript file for handling interactions on the login and register pages.

The first line declares a variable `errorField` and assigns it the value of the `error_field` variable. This value is ea string representing the field where an error occurred. The if statement checks if the `errorField` exists. If it does, it means an error occurred and needs to be handled. Then the code retrieves the HTML element with the ID stored in the `errorField` variable using the `getElementById` method and assigns it to the `inputField` variable. The `classList.add()` method is then called on the `inputField` element, adding the CSS class name `"error-input"` to it, defined in corresponding CSS stylesheet. 

`goBack()` function is declared, which uses the `window.history.back()` method to navigate back to the previous page in the browser's history.

## **Used Recources**
1. Interactive and customizable maps service SimpleMaps: https://simplemaps.com/ 
2. Youtube Tutorial by TSN soft: https://www.youtube.com/watch?v=6C-GYwxdZd4&list=LL&index=7
3. Login, Registed and Session logic from CS50 submission "Finance": https://cs50.harvard.edu/x/2023/psets/9/finance/
4. SVG map zoom in and zoom out logic: https://itnext.io/javascript-zoom-like-in-maps-for-svg-html-89c0df016d8d, 
5. Youtube tutorial by CSS-Tricks: https://www.youtube.com/watch?v=7Pyb7UpxKMw
6. ChatGPT to analize big sizes of data and to help understand some complicated concepts: https://chat.openai.com/

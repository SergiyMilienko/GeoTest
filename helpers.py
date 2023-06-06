from flask import redirect, session, render_template
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def apology(message, code, field_name=None):
    """Function to display error message and highlight box in red"""
    return render_template("register.html", apology_message=message, error_field=field_name)
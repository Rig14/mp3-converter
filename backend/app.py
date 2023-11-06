"""Main application file"""
from flask import request, Flask
from backend.db import execute

app = Flask(__name__)


@app.route("/api/signup")
def index():
    """
    Test api
    """
    email = request.args.get("email")
    password = request.args.get("password")

    # add values to the database
    execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))

    # get all values from the database
    res = execute("SELECT * FROM users")

    # return the values
    return {"users": res}

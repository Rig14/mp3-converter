"""Main application file"""
import re
import sqlite3
import bcrypt
from flask import Flask, request
from flask_cors import CORS
from backend.db import execute
from backend.token import create_token

app = Flask(__name__)
CORS(app)


@app.route("/api/signup", methods=["POST"])
def signup():
    """
    Signup route. Creates a new user in the database.

    If the user is created successfully, returns a 200 status code and jwt token.
    If there is an error, returns a 400 status code and an error message.
    """

    email = request.get_json().get("email")
    password = request.get_json().get("password")
    password_confirm = request.get_json().get("password_confirm")

    if not email:
        return {"error": "Email is required"}, 400

    if not password:
        return {"error": "Password is required"}, 400

    if password != password_confirm:
        return {"error": "Passwords do not match"}, 400

    # test email with regex
    email_regex = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"

    if not re.match(email_regex, email):
        return {"error": "Invalid email"}, 400

    # password must be at least 8 characters long
    if len(password) < 8:
        return {"error": "Password must be at least 8 characters long"}, 400

    # if email is already in use
    if execute("SELECT * FROM users WHERE email = ?", (email,)):
        return {"error": "Email already in use"}, 400

    # crete a name for user based on email
    name = email.split("@")[0]
    default_motd = "Hello, World!"

    # hashing password
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # insert user into database
    try:
        execute(
            "INSERT INTO users (name, email, password, motd) VALUES (?, ?, ?, ?)",
            (name, email, hashed_pw, default_motd),
        )
    except sqlite3.Error as e:
        return {"error": str(e)}, 500

    # get user id
    user_id = execute("SELECT id FROM users WHERE email = ?", (email,))[0][0]

    # issue a jwt token for user
    token = create_token(user_id)
    return {"token": token}, 200


@app.route("/api/login", methods=["POST"])
def login():
    """
    Login route. Checks if the user exists and if the password is correct.

    If the user exists and the password is correct, returns a 200 status code and jwt token.
    """
    email = request.get_json().get("email")
    password = request.get_json().get("password")

    # check if email and password are provided
    if not email or not password:
        return {"error": "Email and password are required"}, 400

    # check if user exists
    user = execute("SELECT * FROM users WHERE email = ?", (email,))
    if not user:
        return {"error": "User does not exist"}, 400

    # check if password is correct
    hashed_pw = execute("SELECT password FROM users WHERE email = ?", (email,))[0][0]
    if not bcrypt.checkpw(password.encode(), hashed_pw):
        return {"error": "Password is incorrect"}, 400

    # making jwt token:
    user_id = execute("SELECT id FROM users WHERE email = ?", (email,))[0][0]
    token = create_token(user_id)
    return {"token": token}, 200

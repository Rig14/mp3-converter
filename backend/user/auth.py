"""User authentication functions."""
import sqlite3
import bcrypt
from backend.db import execute
from . import validate, token


def create_user(email, password, password_confirmation):
    """
    Creates a new user given the email,
    password and password confirmation.
    If something went wrong returns a tuple with error message and status code.
    When user is successfully created returns a JWT token.
    """
    # email validation
    email_validation = validate.validate_email_signup(email)
    if email_validation is not True:
        return email_validation

    # password validation
    password_validation = validate.validate_password_signup(
        password, password_confirmation
    )
    if password_validation is not True:
        return password_validation

    # crete a name for user based on email
    name = email.split("@")[0]

    # hashing password
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # insert user into database
    try:
        execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, hashed_pw),
        )
    except sqlite3.Error as e:
        return {"error": str(e)}, 500

    # get user id
    user_id = execute("SELECT id FROM users WHERE email = ?", (email,))[0][0]

    # create a jwt token
    t = token.create_token(user_id)
    return {"token": t}, 200


def login_user(email, password):
    """
    Logs in an user.
    If something went wrong returns a tuple with error message and status code.
    When user is successfully logged in returns a JWT token.
    """
    # validate email and password
    validation = validate.validate_login(email, password)

    if validation is not True:
        return validation

    # get user id from database
    user_id = execute("SELECT id FROM users WHERE email = ?", (email,))[0][0]

    # create a jwt token
    t = token.create_token(user_id)
    return {"token": t}, 200

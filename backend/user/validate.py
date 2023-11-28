"""Everything that has to do with user data validation."""
import re

import bcrypt
from backend.db import execute


EMAIL_REGEX = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"


def validate_password_signup(password1, password2):
    """
    Validate user inserted passwords.
    Returns true if passwords are valid,
    otherwise returns a tuple with error message and status code.
    """
    if not password1 or not password2:
        return {"error": "Password is required"}, 400

    if password1 != password2:
        return {"error": "Passwords do not match"}, 400

    # password must be at least 8 characters long
    if len(password1) < 8:
        return {"error": "Password must be at least 8 characters long"}, 400

    return True


def validate_email_signup(email):
    """
    Validate user inserted email.
    Returns true if email is valid,
    otherwise returns a tuple with error message and status code.
    """
    if not email:
        return {"error": "Email is required"}, 400

    # test email with regex
    if not re.match(EMAIL_REGEX, email):
        return {"error": "Please enter a valid email address"}, 400

    # test if email exsists in database
    if execute("SELECT * FROM users WHERE email = ?", (email,)):
        return {"error": "Email already in use"}, 400

    return True


def validate_login(email, password):
    """
    Validates email and password on login.
    Returns true if email and password are valid,
    otherwise returns a tuple with error message and status code.
    """
    if not email:
        return {"error": "Email is required"}, 400

    if not password:
        return {"error": "Password is required"}, 400

    # test if email has an account
    if not execute("SELECT * FROM users WHERE email = ?", (email,)):
        return {"error": "Email or password is incorrect"}, 400

    # test if password is correct
    hashed_pw = execute("SELECT password FROM users WHERE email = ?", (email,))[0][0]

    if not bcrypt.checkpw(password.encode(), hashed_pw):
        return {"error": "Password is incorrect"}, 400

    return True

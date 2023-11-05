"""Main application file"""
import os
import sqlite3
from flask import Flask, request

app = Flask(__name__)


@app.route("/api/signup")
def index():
    """
    Test api
    """
    email = request.args.get("email")
    password = request.args.get("password")
    password_confirm = request.args.get("password_confirm")

    os.chdir(os.path.dirname(__file__))
    with sqlite3.connect(os.path.join(os.path.dirname(__file__), "database.db")) as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO user (email, password) VALUES (?, ?)", (email, password)
        )
        con.commit()
        return "User created successfully"

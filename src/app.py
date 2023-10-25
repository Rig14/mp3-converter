"""Main application file"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    """
    Home page
    """
    return render_template("index.html")

"""Main application file"""

from flask import Flask

app = Flask(__name__)


@app.route("/api")
def index():
    """
    Test api
    """
    return {"message": "Hello, World!"}

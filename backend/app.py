"""Main application file"""
from flask import Flask, request
from flask_cors import CORS
from backend.user import (
    create_user,
    login_user,
    get_user_data,
    change_data,
    change_user_profile_picture,
    add_user_history,
    get_user_history,
    delete_user_account,
)
from backend.downloader import download_to_server, send_file_from_server
from backend.admin import get_blacklist_items, add_blacklist_item


app = Flask(__name__)
CORS(app)


@app.route("/api/signup", methods=["POST"])
def signup():
    """
    User signup route. Creates a new user in the database.
    """
    email = request.get_json().get("email")
    password = request.get_json().get("password")
    password_confirmation = request.get_json().get("password_confirm")

    return create_user(email, password, password_confirmation)


@app.route("/api/login", methods=["POST"])
def login():
    """
    Login route. Checks if the user exists and if the password is correct.

    returns JWT token if the user exists and the password is correct.
    """
    email = request.get_json().get("email")
    password = request.get_json().get("password")

    return login_user(email, password)


@app.route("/api/user_data", methods=["GET"])
def user_data():
    """
    User data route. Returns the user data if the token is valid.
    """
    token = request.headers.get("Authorization")

    return get_user_data(token)


@app.route("/api/download", methods=["POST"])
def download():
    """
    Download content, given a url using yt-dlp.

    Returns a 200 status code and the file name.
    """
    url = request.get_json().get("url")
    format_str = request.get_json().get("format")

    return download_to_server(url, format_str)


@app.route("/api/file", methods=["GET"])
def serve_file():
    """Sends file to frontend."""
    identifier = request.args.get("identifier")
    file_name = request.args.get("file_name")
    get_name_only = request.args.get("get_name_only")

    if get_name_only:
        get_name_only = True

    return send_file_from_server(identifier, file_name, get_name_only)


@app.route("/api/change_user_data", methods=["POST"])
def change_user_data():
    """
    Changes user data.

    Returns 200 status code if successful.
    """
    token = request.headers.get("Authorization")
    name = request.get_json().get("name")
    motd = request.get_json().get("motd")
    password = request.get_json().get("password")
    email = request.get_json().get("email")

    return change_data(token, name, email, password, motd)


@app.route("/api/change_profile_picture", methods=["POST"])
def update_profile_picture():
    """
    Updates the profile picture of the user.
    """
    token = request.headers.get("Authorization")
    image = request.files.get("image")

    return change_user_profile_picture(token, image)


@app.route("/api/add_history", methods=["POST"])
def add_history():
    """Add a history row to the database."""
    token = request.headers.get("Authorization")
    content_title = request.get_json().get("content_title")
    content_url = request.get_json().get("content_url")
    content_format = request.get_json().get("content_format")

    return add_user_history(token, content_title, content_url, content_format)


@app.route("/api/get_history", methods=["GET"])
def get_history():
    """Get user history."""
    token = request.headers.get("Authorization")

    return get_user_history(token)


@app.route("/api/delete_account", methods=["DELETE"])
def delete_account():
    """Delete user account."""
    token = request.headers.get("Authorization")

    return delete_user_account(token)


@app.route("/api/blacklist", methods=["GET"])
def get_blacklist():
    """Get blacklist."""
    token = request.headers.get("Authorization")

    return get_blacklist_items(token)


@app.route("/api/blacklist", methods=["POST"])
def add_blacklist():
    """Add to blacklist."""
    token = request.headers.get("Authorization")
    content_url = request.get_json().get("content_url")

    return add_blacklist_item(token, content_url)

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
from backend.admin import (
    get_blacklist_items,
    add_blacklist_item,
    remove_blacklist_item,
    get_all_users,
    delete_user_history,
    delete_user_account_admin,
)


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
    data_dict = request.args.get("data_dict")
    get_data_only = request.args.get("get_data_only")

    if get_data_only:
        get_data_only = True

    return send_file_from_server(identifier, data_dict, get_data_only)


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


@app.route("/api/blacklist", methods=["GET", "POST", "PATCH"])
def blacklist():
    """Blacklist operations."""
    token = request.headers.get("Authorization")

    if request.method == "GET":
        return get_blacklist_items(token)

    if request.method == "POST":
        content_url = request.get_json().get("content_url")
        return add_blacklist_item(token, content_url)

    if request.method == "PATCH":
        content_id = request.get_json().get("content_id")
        return remove_blacklist_item(token, content_id)


@app.route("/api/users", methods=["GET"])
def users():
    """Get all users."""
    token = request.headers.get("Authorization")
    if request.method == "GET":
        return get_all_users(token)


@app.route("/api/delete_history", methods=["PATCH"])
def delete_history():
    """Delete user history for a given user id."""

    token = request.headers.get("Authorization")
    user_id = request.get_json().get("user_id")

    return delete_user_history(token, user_id)


@app.route("/api/delete_account_id", methods=["PATCH"])
def delete_account_id():
    """Delete user account for a given user id."""

    token = request.headers.get("Authorization")
    user_id = request.get_json().get("user_id")

    return delete_user_account_admin(token, user_id)

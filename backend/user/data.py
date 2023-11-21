"""Everythng that has to do with user data and ist manipulation."""

from backend.db import execute
from . import token


def get_user_data(t):
    """
    Using the JWT token returns user data.
    """

    if not t:
        return {"error": "Token is missing"}, 400

    user_id = token.get_id_from_token(t)

    if not user_id:
        return {"error": "Invalid token"}, 400

    user = execute("SELECT name, motd, image FROM users WHERE id = ?", (user_id,))[0]

    return {
        "id": user_id,
        "name": user[0],
        "motd": user[1],
        "profile_picture": user[2],
    }, 200

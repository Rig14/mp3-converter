"""Everythng that has to do with user data and ist manipulation."""

import os
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

    user = execute(
        "SELECT name, motd, image, email FROM users WHERE id = ?", (user_id,)
    )[0]

    return {
        "id": user_id,
        "name": user[0],
        "motd": user[1],
        "profile_picture": user[2],
        "email": user[3],
    }, 200


def delete_user_account(_token):
    """Delete user account."""
    current_user_id = token.get_id_from_token(_token)

    if not current_user_id:
        return {"error": "Invalid token"}, 400

    # delete profile picture
    profile_picture = execute(
        "SELECT image FROM users WHERE id = ?", (current_user_id,)
    )[0][0]
    if profile_picture and profile_picture != "default_user.svg":
        os.remove(os.path.join("..", "static", profile_picture))

    # delete user
    execute("DELETE FROM users WHERE id = ?", (current_user_id,))

    return {"message": "user deleted sucessfully"}, 200

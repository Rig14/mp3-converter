import os
from backend.db import execute
from backend.user import token


def get_all_users(_token):
    """
    Return all users.

    Returns users name, profile picture and id.
    """
    # check if token is admin
    if not _token:
        return {"error": "Token is missing"}, 400

    user_id = token.get_id_from_token(_token)
    if not user_id:
        return {"error": "Invalid token"}, 400

    is_admin = execute("SELECT admin FROM users WHERE id = ?", (user_id,))[0][0]

    if not is_admin:
        return {"error": "You are not an admin"}, 403

    # get all users
    users = execute("SELECT id, name, image FROM users", ())

    return {"users": users}, 200


def delete_user_history(_token, user_id):
    """Deletes users history."""
    if not _token:
        return {"error": "Invalid token"}, 400

    admin_id = token.get_id_from_token(_token)

    if not admin_id:
        return {"error": "Invalid token"}, 400

    is_admin = execute("SELECT admin FROM users WHERE id = ?", (admin_id))[0][0]
    if not is_admin:
        return {"error": "You are not an admin"}, 403

    execute("DELETE FROM history WHERE user_id = ?", (user_id,))

    return {"message": "history deleted sucessfully"}, 200


def delete_user_account_admin(_token, user_id):
    """Delete an account with a given id."""
    if not _token:
        return {"error": "Invalid token"}, 400

    admin_id = token.get_id_from_token(_token)

    if not admin_id:
        return {"error": "Invalid token"}, 400

    is_admin = execute("SELECT admin FROM users WHERE id = ?", (admin_id))[0][0]

    if not is_admin:
        return {"error": "You are not an admin"}, 403

    # delete profile picture
    profile_picture = execute("SELECT image FROM users WHERE id = ?", (user_id,))[0][0]
    if profile_picture and profile_picture != "default_user.svg":
        os.remove(os.path.join("..", "static", profile_picture))

    # delete user
    execute("DELETE FROM users WHERE id = ?", (user_id,))

    return {"message": "user deleted sucessfully"}, 200

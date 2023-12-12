"""Content blacklisting."""


import sqlite3
from backend.db import execute
from backend.user import get_id_from_token


def validate_admin(token):
    """Validate admin account."""
    # validate token
    user_id = get_id_from_token(token)
    if not user_id:
        return {"error": "Invalid token."}, 401

    # check if user is admin
    is_admin = execute("SELECT admin FROM users WHERE id = ?", (user_id,))[0][0]

    if not is_admin:
        return {"error": "You are not an admin."}, 403


def get_blacklist_items(token):
    """Returns the blacklisted items."""

    validation_failed = validate_admin(token)
    if validation_failed:
        return validation_failed

    # get the blacklisted items
    items = execute("SELECT * FROM blacklist", ())

    return {"items": items}, 200


def add_blacklist_item(token, url):
    """Adds a blacklisted item."""
    validation_failed = validate_admin(token)
    if validation_failed:
        return validation_failed

    # add the item to the blacklist
    try:
        execute("INSERT INTO blacklist (url) VALUES (?)", (url,))
    except sqlite3.Error as e:
        return {"error": str(e)}, 500

    return {"message": "Item added to blacklist."}, 200


def remove_blacklist_item(token, id):
    """Removes a item from the blacklist."""
    validation_failed = validate_admin(token)
    if validation_failed:
        return validation_failed

    # remove the item from the blacklist
    try:
        execute("DELETE FROM blacklist WHERE id = ?", (id,))
    except sqlite3.Error as e:
        return {"error": str(e)}, 500

    return {"message": "Item removed from blacklist."}, 200

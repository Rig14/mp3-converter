"""Content blacklisting."""


from backend.db import execute
from backend.user import get_id_from_token


def get_blacklist_items(token):
    """Returns the blacklisted items."""
    # validate token
    user_id = get_id_from_token(token)
    if not user_id:
        return {"message": "Invalid token."}, 401

    # check if user is admin
    is_admin = execute("SELECT is_admin FROM users WHERE id = ?", (user_id,))[0][0]

    if not is_admin:
        return {"message": "You are not an admin."}, 403

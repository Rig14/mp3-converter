"""Everything to do with history."""


from backend.db import execute
from backend.user.token import get_id_from_token


def add_user_history(token, content_title, content_url, content_format):
    """Add user history."""
    current_user_id = get_id_from_token(token)

    if not current_user_id:
        return {"error": "Invalid token"}, 400

    execute(
        "INSERT INTO history (user_id, content_title, content_url, content_format) VALUES (?, ?, ?, ?)",
        (current_user_id, content_title, content_url, content_format),
    )

    return {"message": "history added sucessfully"}, 200

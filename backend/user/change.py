"""User data changing."""
import bcrypt
from backend.db import execute
from .token import get_id_from_token


def change_data(token, name, email, password, motd):
    """Change user data."""
    current_user_id = get_id_from_token(token)

    if not current_user_id:
        return {"error": "Invalid token"}, 400

    if password:
        if len(password) < 8:
            return {"error": "Password is too short"}, 400
        hashedpw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        execute(
            "UPDATE users SET password = ? WHERE id = ?", (hashedpw, current_user_id)
        )

    if name:
        execute("UPDATE users SET name = ? WHERE id = ?", (name, current_user_id))

    if email:
        execute("UPDATE users SET email = ? WHERE id = ?", (email, current_user_id))

    if motd:
        execute("UPDATE users SET motd = ? WHERE id = ?", (motd, current_user_id))

    return {"message": "user data updated sucessfully"}, 200

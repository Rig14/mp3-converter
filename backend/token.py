"""Everything that has to do with JWT web tokens in the backend."""
import datetime
import os
from dotenv import load_dotenv
import jwt


def create_token(user_id: int):
    """
    Creates a jwt token for the given user id.
    """
    load_dotenv()
    jwt_secret = os.getenv("JWT_SECRET")

    payload = {
        "exp": datetime.datetime.now() + datetime.timedelta(days=10),
        "sub": user_id,
    }

    return jwt.encode(payload, jwt_secret, algorithm="HS256")

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


def get_id_from_token(token) -> int:
    """
    Checks if the given token is valid.

    Returns the user id if the token is valid, otherwise returns False.
    """
    load_dotenv()
    jwt_secret = os.getenv("JWT_SECRET")

    try:
        data = jwt.decode(token, jwt_secret, algorithms=["HS256"])
        return data.get("sub")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

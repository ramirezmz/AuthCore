import jwt
from datetime import datetime, timedelta
from config.settings import Settings


def generate_token(user):
    expiration_time = datetime.utcnow() + timedelta(
        hours=Settings.JWT_EXP_HOURS
    )
    payload = {
        "sub": user.id,
        "email": user.email,
        "role": user.role,
        "exp": expiration_time,
        "iat": datetime.utcnow(),
    }

    token = jwt.encode(payload, Settings.JWT_SECRET,
                       algorithm=Settings.JWT_ALGORITHM)
    return token


def decode_token(token: str):
    try:
        decoded = jwt.decode(
            token, Settings.JWT_SECRET, algorithms=[Settings.JWT_ALGORITHM]
        )
        return decoded
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}

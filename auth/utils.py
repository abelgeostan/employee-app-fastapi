from datetime import datetime, timedelta, timezone
from config import settings
from jose import JWTError, jwt
import bcrypt


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def create_access_token(data: dict) -> str:
    to_encode = {**data, "type": "access"}
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expiry_minutes)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
    except JWTError:
        return None


# def create_refresh_token(data: dict)->str:
#     to_encode = {"id": data.id, "email": data.email, "type": "refresh"}
#     expire = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expiry_days)
#     to_encode["exp"]=expire
#     return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)

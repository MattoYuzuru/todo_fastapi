from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from .config import TIME_ZONE, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(TIME_ZONE) + expires_delta
    else:
        expire = datetime.now(TIME_ZONE) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Fix: Timezone
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

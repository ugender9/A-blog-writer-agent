from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from config import settings
from models import User, TokenData

def verify_password(plain_password, hashed_password):
    # Simple check for demo; in production use proper hashing
    return plain_password == hashed_password

def get_password_hash(password):
    # Return plain for demo; in production hash properly
    return password

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data

# Mock user DB; in production, use real DB
fake_users_db = {
    "admin": {
        "username": "admin",
        "email": "admin@example.com",
    "hashed_password": "admin",  # Plain for demo
        "role": "admin",
    }
}

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return User(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    # Simple check for demo
    if not verify_password(password, user.hashed_password):
        return False
    return user

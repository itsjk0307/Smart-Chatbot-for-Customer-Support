from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "your_secret_key"  # Replace with a strong, random secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    """Generate a JWT token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    """Verify a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise ValueError("Invalid token payload")
        return username
    except JWTError:
        return None


SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

def verify_access_token(token: str):
    """Verify a JWT token and return its payload."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("exp") < datetime.utcnow().timestamp():
            return None  # Token has expired
        return payload
    except JWTError:
        return None


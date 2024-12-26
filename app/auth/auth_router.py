from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from app.auth.jwt_handler import create_access_token, verify_access_token
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User, ChatHistory
from app.schemas import UserCreate

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_user(username: str, password: str, db: Session):
    """Authenticate a user by verifying username and password."""
    user = db.query(User).filter(User.username == username).first()
    if user and pwd_context.verify(password, user.hashed_password):
        return user
    return None

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Endpoint for user login."""
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Endpoint for user registration."""
    # Check if the username already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Hash the password
    hashed_password = pwd_context.hash(user.password)

    # Create a new user
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "user": {"username": new_user.username}}

@router.get("/me")
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Fetch the current authenticated user's profile."""
    payload = verify_access_token(token)  # Verify the JWT token
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"username": user.username}

@router.post("/chat/log", status_code=201)
def log_chat(message: str, response: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Log user-chatbot interaction in the database."""
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create and save chat log
    chat_log = ChatHistory(user_id=user.id, message=message, response=response)
    db.add(chat_log)
    db.commit()
    db.refresh(chat_log)

    return {"message": "Chat log saved successfully", "chat_id": chat_log.id}

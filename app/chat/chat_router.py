from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.auth.jwt_handler import verify_access_token
from app.db.database import get_db
from app.db.models import ChatHistory
from app.chat.bot_logic import generate_bot_response

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

@router.post("/chat")
def chat_with_bot(message: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Interact with the chatbot."""
    # Verify user identity
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = db.query(ChatHistory.user).filter(ChatHistory.user.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate a chatbot response
    response = generate_bot_response(message)

    # Save the interaction to the database
    chat_log = ChatHistory(user_id=user.id, message=message, response=response)
    db.add(chat_log)
    db.commit()

    return {"message": message, "response": response}

@router.get("/history")
def get_chat_history(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10
):
    """Fetch chat history for the authenticated user."""
    # Verify the user's JWT token
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    # Query the chat history for the user
    user_chat_logs = (
        db.query(ChatHistory)
        .filter(ChatHistory.user.username == username)
        .offset(skip)
        .limit(limit)
        .all()
    )

    if not user_chat_logs:
        return {"message": "No chat history found."}

    # Format the chat history
    history = [
        {
            "id": chat.id,
            "message": chat.message,
            "response": chat.response,
            "timestamp": chat.timestamp
        }
        for chat in user_chat_logs
    ]

    return {"username": username, "history": history}

from fastapi import FastAPI
from app.auth.auth_router import router as auth_router
from app.chat.chat_router import router as chat_router

app = FastAPI()

# Include authentication and chat routers
app.include_router(auth_router, prefix="/api/auth")
app.include_router(chat_router, prefix="/api/chat")

@app.get("/")
def root():
    return {"message": "Welcome to the Smart Chatbot Backend!"}

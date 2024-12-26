from fastapi import APIRouter

router = APIRouter()

@router.get("/chatbot")
def chatbot_info():
    return {"message": "Chatbot API is ready!"}

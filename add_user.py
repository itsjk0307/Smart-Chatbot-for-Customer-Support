from app.db.database import SessionLocal
from app.db.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create a new user
db = SessionLocal()
hashed_password = pwd_context.hash("password1")
new_user = User(username="user1", hashed_password=hashed_password)
db.add(new_user)
db.commit()
db.close()

print("User added successfully!")

from app.db.database import Base, engine
from app.db.models import User

# Create database tables
Base.metadata.create_all(bind=engine)

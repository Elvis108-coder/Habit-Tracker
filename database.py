# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base  # ✅ import Base from base.py, not from models

# Set up engine
engine = create_engine("sqlite:///habits.db", echo=True)

# Session maker
SessionLocal = sessionmaker(bind=engine)

# Function to get a new session
def get_session():
    return SessionLocal()

# Function to initialize the database
def init_db():
    import models  # Ensure models are loaded so tables are registered
    Base.metadata.create_all(engine)
def inited():
    return engine

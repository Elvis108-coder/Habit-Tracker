# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base  # ✅ Correct: Base should come from your base.py file

# Create the database engine
engine = create_engine("sqlite:///habits.db", echo=True)  # Changed to "habits.db"

# Create a configured session class
SessionLocal = sessionmaker(bind=engine)

# Function to get a session
def get_session():
    return SessionLocal()

# Function to initialize the database
def init_db():
    import models  # ✅ Important: this ensures models are registered with Base
    Base.metadata.create_all(engine)  # ✅ Create all tables from Base subclasses

# Optional: return the engine for debugging or connection
def inited():
    return engine

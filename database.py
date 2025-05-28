from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base  # Import Base from models.py

# Set up engine
engine = create_engine("sqlite:///habits.db", echo=True)

# Corrected name to match what app.py expects
SessionLocal = sessionmaker(bind=engine)

# Function to get a new session
def get_session():
    return SessionLocal()

# Function to initialize the database
def init_db():
    import models  # Ensure all models are registered
    Base.metadata.create_all(engine)

# Optional CLI initialization
if __name__ == "__main__":
    init_db()
    print("Database initialized.")

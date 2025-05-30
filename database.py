from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Define Base here, so models.py imports from database.py instead of the other way around
Base = declarative_base()

# Set up engine
engine = create_engine("sqlite:///habits.db", echo=True)

# Create session factory
SessionLocal = sessionmaker(bind=engine)


# Function to get a new session
def get_session():
    return SessionLocal()

# Function to initialize the database
def init_db():
    import models  # Import here to register models AFTER Base is defined
    Base.metadata.create_all(engine)

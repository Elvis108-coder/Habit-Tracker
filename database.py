from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Create engine (connect to SQLite database)
engine = create_engine('sqlite:///habits.db', echo=False)

# Create session
Session = sessionmaker(bind=engine)
session = Session()

# Base class for models
Base = declarative_base()

def inited():
    from models import Habit, CheckIn  # Avoid circular imports
    Base.metadata.create_all(engine)

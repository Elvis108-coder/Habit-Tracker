# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///habits.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

def inited():
    from models import Habit, CheckIn
    Base.metadata.create_all(engine)
    print("Database initialized, tables created.")

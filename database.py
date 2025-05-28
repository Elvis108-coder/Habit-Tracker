from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

engine = create_engine("sqlite:///habits.db")
Session = sessionmaker(bind=engine)

def get_session():
    return Session()

def init_db():
    Base.metadata.create_all(engine)
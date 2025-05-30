from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from database import Base
from models import User, Habit, CheckIn

# Use in-memory SQLite for testing
TEST_DB_URL = "sqlite:///:memory:"

engine = create_engine(TEST_DB_URL, echo=False)
SessionTest = sessionmaker(bind=engine)
test_session = SessionTest()

def setup_test_db():
    Base.metadata.create_all(engine)
    return test_session
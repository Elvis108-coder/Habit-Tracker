from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)  # unique username
    email = Column(String(40), unique = True, nullable = False) # email
    password = Column(String(128), nullable=False)              # hashed password
    habits = relationship("Habit", back_populates="user")       # one-to-many relationship to Habit

class Habit(Base):
    __tablename__ = 'habits'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    frequency = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # link to User
    
    user = relationship("User", back_populates="habits")         # back reference to User
    check_ins = relationship("CheckIn", back_populates="habit")

class CheckIn(Base):
    __tablename__ = 'check_ins'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    habit_id = Column(Integer, ForeignKey('habits.id'), nullable=False)
    
    habit = relationship("Habit", back_populates="check_ins")

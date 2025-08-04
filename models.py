from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from base import Base  # Import Base from base.py
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(128), nullable=False)  # hashed password
    habits = relationship("Habit", back_populates="user")

class Habit(Base):
    __tablename__ = 'habits'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    frequency = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    user = relationship("User", back_populates="habits")
    check_ins = relationship("CheckIn", back_populates="habit", cascade="all, delete-orphan")

class CheckIn(Base):
    __tablename__ = 'check_ins'

    id = Column(Integer, primary_key=True)
    habit_id = Column(Integer, ForeignKey('habits.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    note = Column(Text, default="")

    habit = relationship("Habit", back_populates="check_ins")

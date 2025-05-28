# models.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Habit(Base):
    __tablename__ = 'habits'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    frequency = Column(String, nullable=False)  # e.g., daily, weekly

    check_ins = relationship("CheckIn", back_populates="habit")

class CheckIn(Base):
    __tablename__ = 'checkins'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    habit_id = Column(Integer, ForeignKey('habits.id'))

    habit = relationship("Habit", back_populates="check_ins")

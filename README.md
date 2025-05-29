# Habit-Tracker

Created the file called main.py
in this file we are working with SQLAlchemy.
Put SQLAlchemy into the system using the command: pip install sqlalchemy.

In the file created four imports from sqlalchemy: 
-from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
-from sqlalchemy.ext.declarative import declarative_base
-from sqlalchemy.orm import sessionmaker, relationship
-from sqlalchemy.exc import IntegrityError

#1. ##create_engine## function creates the database
#2. ##ForeignKey## is used to allow the different models to interact/speak with each other
#3. The ##declarative_base## is just the base class for any model that is already pre programmed in the sqlAlachemy
#4. The ##session_maker## is going to make the database session from the engine and ##relationship## will allow the different models to have a realtionship together.
#5. ##IntegrityError## might get this if you make database changes without deleting your database before making the final product this will be used to alert us to this kind of error.

Created the class User and Habits

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    names = Column(String, nullable = False)
    email = Column(String, nullable = False, unique = True) 
    habits = relationship('Habits', back_populates= 'user', cascade="all")

class Habits(Base):
    __tablename__ = 'habits'
    id = Column(Integer, primary_key = True)
    title = Column(String(50), nullable = False)
    description = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates= 'habits')
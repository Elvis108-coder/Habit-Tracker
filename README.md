# Habit-Tracker

# Habit-Tracker
                                PART 1
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

                         PART 2

Added Utility Functions to help with deleting of data

def get_user_by_email(email):
    return session.query(User).filter_by(email = email).first()

def confirm_action(prompt: str) -> bool:
    return input(f"{prompt} (yes/no): ").strip().lower() == 'yes'

Created A function for adding a user

def add_user():
    name, email = input("Enter user name: "), input("Enter email: ")
    if get_user_by_email(email):
        print(f"Email already exists: {email}")
        return
    try:
        session.add(User(names=name, email=email))#Add user to the database
        session.commit()
        print(f"User: {name} added!")
    except IntegrityError:
        session.rollback()
        print(f'error')

Created A function for adding habit to the database

def add_habit():
    email = input("Enter email: ")
    user = get_user_by_email(email)

    if not user:
        print(f'No user found by that email!')
        return
    title, description = input("Enter the title: "), input("Enter the description: ")
    session.add(Habits(title=title, description=description, user=user))#Add habit to the database
    session.commit()
    print(f"Added to the database: {title}: {description}")

Added a dictionary and a menu list To add User and Habit
def main()-> None:
    actions= {
        "1":add_user,
        "2":add_habit
        
    }

while True:
        print("\nOptions:\n1. Add User\n2. Add Task\n3. Query Users\n4. Query Tasks\n5. Update User\n6. Delete User\n7. Delete Task\n8. Exit")
        choice = input("Enter an option: ")
        if choice == "8":
            print("Goodbye")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("That is not an option!")
if __name__ == "__main__":

    main()


                        PART 3

Created a query_user and query_habit function

def query_users():
    for user in session.query(User).all():
        print(f"ID: {user.id}, Name: {user.names}, Email: {user.email}")

#Query Habits
def query_habits():
    email=input("Enter email: ")
    user = get_user_by_email(email)
    if not user:
        print("User does not exist, wrong email!")
        return
    for habits in user.habits:
        print(f"Habit ID: {habits.id}, Title: {habits.title}")

Added query_user and query_habits in dictionary. query_user is used to find a user and query_habits is used to find a habit.

def main()-> None:
    actions= {
        "1":add_user,
        "2":add_habit,
        "3":query_users,
        "4":query_habits
        
    }

#imports
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError
from datetime import datetime

# Create database
engine = create_engine("sqlite:///goals.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Define models
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    names = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    goals = relationship('Goal', back_populates='user', cascade="all, delete-orphan")

class Goal(Base):
    __tablename__ = 'goals'
    id = Column(Integer, primary_key=True)
    goal = Column(String, nullable=False)
    day = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='goals')

Base.metadata.create_all(engine)

# Utility functions
def get_user_by_email(email):
    return session.query(User).filter_by(email=email).first()

def get_user_by_username(username):
    return session.query(User).filter_by(username=username).first()

def confirm_action(prompt: str) -> bool:
    return input(f"{prompt} (yes/no): ").strip().lower() == 'yes'

# CRUD Operations
def add_user():
    name = input("Enter name: ")
    username = input("Enter username: ")
    email = input("Enter email: ")

    if get_user_by_email(email):
        print(f"Email already exists: {email}")
    elif get_user_by_username(username):
        print(f"Username already exists: {username}")
    else:
        try:
            session.add(User(names=name, username=username, email=email))
            session.commit()
            print(f"User '{name}' added!")
        except IntegrityError:
            session.rollback()
            print("Error adding user due to integrity constraints.")

def add_goal():
    identifier = input("Enter email or username: ").strip()

    user = get_user_by_email(identifier) or get_user_by_username(identifier)

    if not user:
        print(f"No user found with email or username: {identifier}")
        return

    goal = input("Enter goal: ")
    day = input("Enter day: ")
    date_input = input("Enter the date (YYYY-MM-DD): ")

    try:
        date_obj = datetime.strptime(date_input, "%Y-%m-%d").date()
        session.add(Goal(goal=goal, day=day, date=date_obj, user=user))
        session.commit()
        print(f"Goal added for {user.names}: {goal} {date_input}")
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
    except IntegrityError:
        session.rollback()
        print("Error adding goal due to integrity constraints.")

# Placeholder functions
def query_users():
    users = session.query(User).all()
    for user in users:
        print(f"{user.id}: {user.names} ({user.email})")

def query_tasks():
    goals = session.query(Goal).all()
    for goal in goals:
        print(f"{goal.id}: {goal.goal} on {goal.day}, {goal.date}")


#Update User
def update_user():
    email = input("Enter email: ")
    user = get_user_by_email(email)
    if not user:
        print("User does not exist, wrong email!")
        return

    new_name = input(f"Enter new name (current: {user.names}): ").strip()
    new_email = input(f"Enter new email (current: {user.email}): ").strip()

    if new_email != user.email and get_user_by_email(new_email):
        print("That email is already in use.")
        return

    user.names = new_name or user.names
    user.email = new_email or user.email

    try:
        session.commit()
        print("User updated successfully.")
    except IntegrityError:
        session.rollback()
        print("Error updating user.")


#Delete User
def delete_user():
    email = input("Enter email: ")
    user = get_user_by_email(email)
    if not user:
        print("User not found.")
        return

    if confirm_action(f"Are you sure you want to delete {user.names}? This will delete all their tasks too."):
        session.delete(user)
        session.commit()
        print("User and their habits deleted.")

#Delete Habit
def delete_habit():
    habit_id = input("Enter the task ID to delete: ").strip()
    habit = session.query(Habits).filter_by(id=habit_id).first()
    if not habit:
        print("No task found with that ID.")
        return

    if confirm_action(f"Are you sure you want to delete the task: {habit.goals}?"):

        session.delete(habit)
        session.commit()
        print("Habit deleted.")



# Main Operation
def main()-> None:
    actions= {
        "1":add_user,
        "2":add_habit,
        "3":query_users,
        "4":query_habits,
        "5":update_user,
        "6":delete_user,
        "7":delete_habit
        
    }

    while True:
        print("\nOptions:\n1. Add User\n2. Add Habit\n3. Query Users\n4. Query Tasks\n5. Update User\n6. Delete User\n7. Delete Task\n8. Exit")
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



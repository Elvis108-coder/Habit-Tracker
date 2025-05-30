#imports
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError

#create your database
engine = create_engine("sqlite:///task.db", echo=False) #choosing the type of database we want to use
Base = declarative_base()
Session = sessionmaker(bind=engine) #bind session with the engine
session = Session()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    names = Column(String, nullable = False)
    email = Column(String, nullable = False, unique = True) 
    habits = relationship('Habits', back_populates= 'user', cascade="all, delete-orphan")

class Habits(Base):
    __tablename__ = 'habits'
    id = Column(Integer, primary_key = True)
    title = Column(String(50), nullable = False)
    description = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates= 'habits')

Base.metadata.create_all(engine)

#Utility funtions 
def get_user_by_email(email):
    return session.query(User).filter_by(email = email).first()

def confirm_action(prompt: str) -> bool:
    return input(f"{prompt} (yes/no): ").strip().lower() == 'yes'

#CRUD OPERATIONS

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


#Query User
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

    if confirm_action(f"Are you sure you want to delete the task: {habit.title}?"):
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



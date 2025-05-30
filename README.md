# Habit-Tracker

# Habit-Tracker

USED https://sqlitebrowser.org to View in Database. Process of installing and running the program is down below

sudo apt update
sudo apt install sqlitebrowser
sqlitebrowser & 
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

##Created the class User and Goal which created the table 'users' 'goals'

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    names = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    goals = relationship('Goal', back_populates='user',
                         cascade="all, delete-orphan")


class Goal(Base):
    __tablename__ = 'goals'
    id = Column(Integer, primary_key=True)
    goal = Column(String, nullable=False)
    day = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='goals')

                         PART 2

##Added Utility Functions to help with deleting of data and getting the user by name or username

def get_user_by_email(email):
    return session.query(User).filter_by(email=email).first()


def get_user_by_username(username):
    return session.query(User).filter_by(username=username).first()


def confirm_action(prompt: str) -> bool:
    return input(f"{prompt} (yes/no): ").strip().lower() == 'yes'

##Created A function for adding a user

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

##Created A function for adding goal information to the database

def add_goal():
    identifier = input("Enter email or username: ").strip()

    user = get_user_by_email(identifier) or get_user_by_username(identifier)

    if not user:
        print(f"No user found with email or username: {identifier}")
        return

    goal = input("Enter goal: ")
    day = input("Enter day: ")
    date_input = input("Enter the date (YYYY-MM-DD): ")
    status = input(
        "Enter status of your progress(In progress/Completed/Not completed): ")

    try:
        date_obj = datetime.strptime(date_input, "%Y-%m-%d").date()
        session.add(Goal(goal=goal, day=day, date=date_obj,
                    status=status, user=user))
        session.commit()
        print(f"Goal added for {user.names}: {goal} {date_input} {status}")
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
    except IntegrityError:
        session.rollback()
        print("Error adding goal due to integrity constraints.")


##Added a dictionary and a menu list
def main():
    actions = {
        "1": add_user,
        "2": add_goal,
        "3": query_users,
        "4": query_tasks,
        "5": update_user,
        "6": update_task,
        "7": delete_user,
        "8": delete_task
    }

    while True:
        print("\nOptions:")
        print("1. Add User\n2. Add Goal\n3. Query Users\n4. Query Tasks\n5. Update User\n6. Update Goal\n7. Delete User\n8. Delete Task\n9. Exit")
        choice = input("Enter an option: ").strip()
        if choice == "9":
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

                                            PART 4

Added four functions, update_user, update_task, delete_user and delete_habit

#Update User
def update_user():
    identifier = input(
        "Enter email or username of the user to update: ").strip()
    user = get_user_by_email(identifier) or get_user_by_username(identifier)

    if not user:
        print("User not found.")
        return

    print(
        f"Current details:\nName: {user.names}\nUsername: {user.username}\nEmail: {user.email}")

    new_name = input(
        f"Enter new name (or press Enter to keep '{user.names}'): ").strip()
    new_username = input(
        f"Enter new username (or press Enter to keep '{user.username}'): ").strip()
    new_email = input(
        f"Enter new email (or press Enter to keep '{user.email}'): ").strip()

    if new_username and get_user_by_username(new_username) and new_username != user.username:
        print("Username already taken.")
        return

    if new_email and get_user_by_email(new_email) and new_email != user.email:
        print("Email already taken.")
        return

    if confirm_action("Are you sure you want to update this user?"):
        if new_name:
            user.names = new_name
        if new_username:
            user.username = new_username
        if new_email:
            user.email = new_email
        try:
            session.commit()
            print("User updated successfully.")
        except IntegrityError:
            session.rollback()
            print("Error updating user due to integrity constraints.")
    else:
        print("Update cancelled.")

##Update Task progress

def update_task():
    identifier = input("Enter email or username: ").strip()
    user = get_user_by_email(identifier) or get_user_by_username(identifier)

    if not user:
        print("User not found.")
        return

    print("User's Goals:")
    for task in user.goals:
        print(
            f"Task ID: {task.id}, Goal: {task.goal}, Day: {task.day}, Date: {task.date}, Status: {task.status}")

    try:
        task_id = int(input("Enter the Task ID to update: "))
        task = session.query(Goal).filter_by(
            id=task_id, user_id=user.id).first()

        if not task:
            print("Task not found or does not belong to this user.")
            return

        new_goal = input(
            f"Enter new goal (or press Enter to keep '{task.goal}'): ").strip()
        new_day = input(
            f"Enter new day (or press Enter to keep '{task.day}'): ").strip()
        new_date = input(
            f"Enter new date (YYYY-MM-DD) (or press Enter to keep '{task.date}'): ").strip()
        new_status = input(
            f"Enter new status (or press Enter to keep '{task.status}'): ").strip()

        if confirm_action("Are you sure you want to update this task?"):
            if new_goal:
                task.goal = new_goal
            if new_day:
                task.day = new_day
            if new_date:
                try:
                    task.date = datetime.strptime(new_date, "%Y-%m-%d").date()
                except ValueError:
                    print("Invalid date format. Update cancelled.")
                    return
            if new_status:
                task.status = new_status

            session.commit()
            print("Task updated successfully.")
        else:
            print("Update cancelled.")
    except ValueError:
        print("Invalid Task ID. It must be a number.")

#Delete User
def delete_user():
    identifier = input("Enter email or username to delete: ").strip()
    user = get_user_by_email(identifier) or get_user_by_username(identifier)

    if not user:
        print("User not found.")
        return

    if confirm_action(f"Are you sure you want to delete user '{user.names}' and all their goals?"):
        session.delete(user)
        session.commit()
        print(f"User '{user.names}' and related goals deleted.")
    else:
        print("Delete action cancelled.")

#Delete goal
def delete_task():
    identifier = input("Enter email or username: ").strip()
    user = get_user_by_email(identifier) or get_user_by_username(identifier)

    if not user:
        print("User not found.")
        return

    print("User's Goals:")
    for task in user.goals:
        print(
            f"Task ID: {task.id}, Goal: {task.goal}, Date: {task.date}, Status: {task.status}")

    try:
        task_id = int(input("Enter the Task ID to delete: "))
        task = session.query(Goal).filter_by(
            id=task_id, user_id=user.id).first()

        if not task:
            print("Task not found or does not belong to this user.")
            return

        if confirm_action(f"Are you sure you want to delete the goal: '{task.goal}'?"):
            session.delete(task)
            session.commit()
            print("Task deleted.")
        else:
            print("Delete cancelled.")
    except ValueError:
        print("Invalid input. Task ID must be a number.")




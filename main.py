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


# Main Operation
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



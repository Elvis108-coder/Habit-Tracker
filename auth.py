from models import User
from database import session
from getpass import getpass

#Registration and login functionality 
def register():
    username = input("Enter new username: ")
    if session.query(User).filter_by(username=username).first():
        print("Username already exists.")
        return None
    password = getpass("Enter password: ")
    user = User(username=username, password=password)
    session.add(user)
    session.commit()
    print("✅ Registered successfully!")
    return user

def login():
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    user = session.query(User).filter_by(username=username, password=password).first()
    if user:
        print("✅ Login successful!")
        return user
    print("❌ Invalid credentials.")
    return None

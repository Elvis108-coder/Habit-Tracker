from models import User
from database import get_session
from getpass import getpass

def register(username, password):
    session = get_session()
    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user:
        print("Username already taken. Try another one.")
        return None

    new_user = User(username=username, password=password)
    session.add(new_user)
    session.commit()
    print("✅ Registration successful! You can now login.")
    return new_user

def login(username, password):
    session = get_session()
    user = session.query(User).filter_by(username=username).first()
    if user and user.password == password:
        print("✅ Login successful!")
        return user
    else:
        print("❌ Invalid credentials.")
        return None

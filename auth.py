import bcrypt
from models import User
from database import get_session

def register(username, password):
    session = get_session()
    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user:
        print("Username already taken. Try another one.")
        return None
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    new_user = User(username=username, password=hashed.decode())
    session.add(new_user)
    session.commit()
    print("✅ Registration successful! You can now login.")
    return new_user

def login(username, password):
    session = get_session()
    user = session.query(User).filter_by(username=username).first()
    if user and bcrypt.checkpw(password.encode(), user.password.encode()):
        print("✅ Login successful!")
        return user
    else:
        print("❌ Invalid credentials.")
        return None

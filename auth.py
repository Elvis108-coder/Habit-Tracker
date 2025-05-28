import bcrypt
from models import User
from database import session

def register(username, password):
    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user:
        print("❌ Username already exists.")
        return

    # Hash the password before storing
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    user = User(username=username, password=hashed_pw.decode('utf-8'))  # store as string
    session.add(user)
    session.commit()
    print("✅ Registration successful!")

def login(username, password):
    user = session.query(User).filter_by(username=username).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        print("✅ Login successful!")
        return user
    else:
        print("❌ Invalid username or password.")
        return None

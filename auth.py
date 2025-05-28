# auth.py

users = {}  # This dictionary will store users as {username: password}


def register(username, password):
    if username in users:
        print("⚠️  Username already exists. Please choose another.")
        return False
    users[username] = password
    print("✅ Registration successful!")
    return True


def login(username, password):
    if username in users and users[username] == password:
        print("✅ Login successful!")
        return username
    else:
        print("❌ Invalid username or password.")
        return None

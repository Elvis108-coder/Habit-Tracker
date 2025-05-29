import logging
from sqlalchemy.orm import Session
from auth import register, login
from cli import user_menu
from database import init_db, get_session

logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

def main_menu():
    print("\n🌱 Welcome to Habit Tracker CLI 🌱")
    print("[1] Register")
    print("[2] Login")
    print("[3] Exit")
    return input("Choose an option: ")

def run():
    init_db()
    while True:
        choice = main_menu()
        if choice == "1":
            username = input("Choose a username: ")
            password = input("Choose a password: ")
            session = get_session()
            try:
                register(session, username, password)
                session.commit()
            except Exception as e:
                session.rollback()
                print(f"❌ Registration failed: {e}")
            finally:
                session.close()
        elif choice == "2":
            username = input("Username: ")
            password = input("Password: ")
            session = get_session()
            try:
                user = login(session, username, password)
                if user:
                    print("✅ Login successful!")
                    session.commit()
                    user_id = user.id  # Store ID before closing session
                else:
                    print("❌ Invalid username or password.")
                    user_id = None
            except Exception as e:
                session.rollback()
                print(f"❌ Login failed: {e}")
                user_id = None
            finally:
                session.close()
            
            if user_id:
                user_menu(user_id)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    run()
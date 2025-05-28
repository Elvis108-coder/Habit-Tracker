from database import inited
from auth import register, login
from cli import use_env

def run():
    inited()  # Ensure database tables are created

    while True:
        print("\n🌱 Welcome to Habit Tracker CLI 🌱")
        print("[1] Register")
        print("[2] Login")
        print("[3] Exit")
from cli import add_habit, view_habits, delete_habit
from database import init_db


def main_menu():
    print("\n🌱 Welcome to Habit Tracker CLI 🌱")
    print("[1] Register")
    print("[2] Login")
    print("[3] Exit")
    return input("Choose an option: ")
def user_menu(user):
    while True:
        print(f"\n👤 Logged in as {user.username}")
        print("[1] Add a habit")
        print("[2] View my habits")
        print("[3] Delete a habit")
        print("[4] Logout")
        choice = input("Choose an option: ")

        if choice == "1":
            username = input("Choose a username: ")
            password = input("Choose a password: ")
            user = register(username, password)   # capture returned user
            if user:
                print("✅ Registration successful!")
                use_env(user)                     # immediately log in after registration
            else:
                print("❌ Registration failed. Username may already exist.")

        elif choice == "2":
            username = input("Username: ")
            password = input("Password: ")
            user = login(username, password)       # capture returned user
            if user:
                print("✅ Login successful!")
                use_env(user)
            else:
                print("❌ Invalid username or password.")

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    run()

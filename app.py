from auth import register, login
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
            name = input("Enter habit name: ")
            add_habit(user, name)
        elif choice == "2":
            view_habits(user)
        elif choice == "3":
            habit_id = input("Enter habit ID to delete: ")
            if habit_id.isdigit():
                delete_habit(user, int(habit_id))
            else:
                print("Invalid habit ID.")
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")
def run():
    init_db()  # Ensure tables are created
    while True:
        choice = main_menu()
        if choice == "1":
            username = input("Choose a username: ")
            password = input("Choose a password: ")
            register(username, password)
        elif choice == "2":
            username = input("Username: ")
            password = input("Password: ")
            user = login(username, password)
            if user:
                user_menu(user)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    run()


# app.py

from database import inited
from auth import register, login
from cli import use_env

def main_menu():
    print("\n🌱 Welcome to Habit Tracker CLI 🌱")
    print("[1] Register")
    print("[2] Login")
    print("[3] Exit")
    return input("Choose an option: ")

def run():
    inited()
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
                use_env(user)
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❗ Invalid choice. Try again.")

if __name__ == "__main__":
    run()

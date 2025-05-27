from auth import register, login
from cli import add_habit, view_habits, delete_habit
from database import init_db

def main_menu():
    print("\n🌱 Welcome to Habit Tracker CLI 🌱")
    print("[1] Register")
    print("[2] Login")
    print("[3] Exit")
    return input("Choose an option: ")



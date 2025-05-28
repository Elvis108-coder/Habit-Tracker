# cli.py

def main_menu():
    print("\n🌱 Welcome to Habit Tracker CLI 🌱")
    print("[1] Register")
    print("[2] Login")
    print("[3] Exit")
    return input("Choose an option: ")

def use_env(username):
    print(f"\n🌿 Welcome, {username}! You're now in your Habit Tracker dashboard.")
    input("Press Enter to return to the main menu...")

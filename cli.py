from database import session
from models import Habit

def use_env(user):
    while True:
        print(f"\n👤 Logged in as: {user}")
        print("[1] View Habits")
        print("[2] Delete Habit")
        print("[3] Create Habit")
        print("[4] Logout")
        choice = input("Choose an option: ")

        if choice == "1":
            view_habits()
        elif choice == "2":
            delete_habit()
        elif choice == "3":
            create_habit()
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")

def view_habits():
    habits = session.query(Habit).all()
    if not habits:
        print("\nYou have no habits tracked.")
        return
    print("\n📋 Your Habits:")
    for habit in habits:
        print(f"  [{habit.id}] {habit.name} - {habit.frequency}")

def delete_habit():
    view_habits()
    habit_id = input("\nEnter the ID of the habit to delete: ")
    habit = session.query(Habit).filter_by(id=habit_id).first()
    if habit:
        session.delete(habit)
        session.commit()
        print(f"Habit '{habit.name}' deleted.")
    else:
        print("Habit not found.")

def create_habit():
    name = input("Enter habit name: ")
    frequency = input("Enter frequency (e.g. daily, weekly): ")
    new_habit = Habit(name=name, frequency=frequency)
    session.add(new_habit)
    session.commit()
    print(f"Habit '{name}' added.")

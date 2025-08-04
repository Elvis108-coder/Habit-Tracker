from models import Habit
from datetime import datetime, timedelta
from analytics.tracker import HabitTracker
from analytics.reminders import ReminderSystem
from analytics.stats import HabitStats

from auth import register, login
from database import get_session, init_db
import os

# Initialize the database and create tables if they don't exist
init_db()

def display_auth_menu():
    print("\n" + "="*40)
    print("AUTHENTICATION".center(40))
    print("="*40)
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    print("="*40)

def display_menu():
    print("\n" + "="*40)
    print("HABIT TRACKER".center(40))
    print("="*40)
    print("1. Add New Habit")
    print("2. Mark Habit Complete")
    print("3. View Reminders & Missed Habits")
    print("4. Show Progress Analytics")
    print("5. Logout")
    print("="*40)

def main():
    print("Welcome to Habit Tracker!")
    
    user = None
    while not user:
        display_auth_menu()
        choice = input("Choose an option (1-3): ").strip()
        
        if choice == "1":
            username = input("Choose username: ").strip()
            password = input("Choose password: ").strip()
            register(username, password)
        elif choice == "2":
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            user = login(username, password)
            if user:
                print(f"Welcome, {user.username}!")
        elif choice == "3":
            print("Goodbye!")
            return
        else:
            print("Invalid choice. Please enter 1-3.")

    # User is logged in, now create tracker scoped to this user
    data_path = f"data/habits_{user.username}.json"
    os.makedirs(os.path.dirname(data_path), exist_ok=True)
    tracker = HabitTracker(data_path, user.id)  # ✅ PASS USER ID HERE
    reminders = ReminderSystem(tracker)

    while True:
        display_menu()
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            print("\n" + "-"*40)
            print("ADD NEW HABIT")
            name = input("Habit name (e.g., 'Read'): ").strip()
            frequency = input("Frequency (daily/weekly/monthly): ").lower().strip()
            reminder = input("Reminder time (HH:MM) or leave blank: ").strip()

            # 1. Add to tracker JSON
            tracker.add_habit(name, frequency, reminder if reminder else None)
            
            # 2. Add to the database
            session = get_session()
            existing = session.query(Habit).filter_by(user_id=user.id, name=name).first()
            if not existing:
                db_habit = Habit(name=name, frequency=frequency, user_id=user.id)
                session.add(db_habit)
                session.commit()
                print(f"\n✅ '{name}' added successfully to the database and tracker!")
            else:
                print(f"\n⚠️ Habit '{name}' already exists in the database.")

            input("Press Enter to continue...")

        elif choice == "2":
            print("\n" + "-"*40)
            print("YOUR HABITS:")
            habit_list = list(tracker.habits.values())
            for i, habit in enumerate(habit_list, 1):
                print(f"{i}. {habit.name}")
            try:
                habit_num = int(input("\nEnter habit number to mark complete: ")) - 1
                habit = habit_list[habit_num]
                habit.add_completion()
                tracker.save()
                print(f"\n✅ '{habit.name}' marked complete for today!")
            except (ValueError, IndexError):
                print("\n❌ Invalid selection")
            input("Press Enter to continue...")

        elif choice == "3":
            print("\n" + "-"*40)
            print("REMINDERS & ALERTS")
            due = reminders.check_due_reminders()
            missed = reminders.check_missed_habits()
            if due:
                print("\n🔔 Due Now:")
                for habit in due:
                    print(f"- {habit.name} ({habit.reminder_time})")
            else:
                print("\nNo habits due right now.")
            if missed:
                print("\n⚠️ Missed Habits:")
                for habit in missed:
                    last_done = max(habit.completions) if habit.completions else "Never"
                    print(f"- {habit.name} (last done: {last_done})")
            else:
                print("\nNo missed habits detected.")
            input("\nPress Enter to continue...")

        elif choice == "4":
            print("\n" + "-"*40)
            print("PROGRESS ANALYTICS")

            analytics = HabitStats(user.id)

            # 🐞 DEBUG: Show all habits in the DB for verification
            all_habits = analytics.session.query(Habit).all()
            print(f"\n🐞 Debug: Total habits in DB = {len(all_habits)}")
            for h in all_habits:
                print(f"    - Habit: {h.name} | User ID: {h.user_id}")

            # Fetch only the user's habits
            habit_list = analytics.session.query(Habit).filter_by(user_id=user.id).all()

            if not habit_list:
                print("\n❌ You have no habits in the database.")
            else:
                print("\nSelect a habit to analyze:")
                for i, habit in enumerate(habit_list, 1):
                    print(f"{i}. {habit.name}")

                try:
                    habit_num = int(input("\nEnter habit number to analyze: ")) - 1
                    habit = habit_list[habit_num]
                    print(analytics.summarize_habit(habit))
                except (ValueError, IndexError):
                    print("\n❌ Invalid selection.")

            analytics.close()
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()

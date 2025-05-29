from datetime import datetime, timedelta
from analytics.tracker import HabitTracker
from analytics.reminders import ReminderSystem
from analytics.stats import HabitStats

from auth import register, login
from database import get_session

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
    tracker = HabitTracker(user)
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
            tracker.add_habit(name, frequency, reminder if reminder else None)
            print(f"\n✅ '{name}' added successfully!")
            input("Press Enter to continue...")

        elif choice == "2":
            print("\n" + "-"*40)
            print("YOUR HABITS:")
            for i, habit in enumerate(tracker.habits, 1):
                print(f"{i}. {habit.name}")
            try:
                habit_num = int(input("\nEnter habit number to mark complete: ")) - 1
                habit = tracker.habits[habit_num]
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
            for i, habit in enumerate(tracker.habits, 1):
                print(f"{i}. {habit.name}")
            try:
                habit_num = int(input("\nEnter habit number to analyze: ")) - 1
                habit = tracker.habits[habit_num]
                analytics = HabitStats(tracker.habits)
                print(analytics.summarize_habit(habit.name))
            except (ValueError, IndexError):
                print("\n❌ Invalid selection")
            input("Press Enter to continue...")

        elif choice == "5":
            print("\nLogging out...")
            break

        else:
            print("\n❌ Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()

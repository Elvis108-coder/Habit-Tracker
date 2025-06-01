from datetime import datetime, timedelta
from analytics.tracker import HabitTracker
from analytics.reminders import ReminderSystem
from analytics.stats import HabitStats

def display_menu():
    print("\n" + "="*40)
    print("HABIT TRACKER".center(40))
    print("="*40)
    print("1. Add New Habit")
    print("2. Mark Habit Complete")
    print("3. View Reminders & Missed Habits")
    print("4. Show Progress Analytics")
    print("5. Exit")
    print("="*40)

def safe_input(prompt):
    try:
        return input(prompt)
    except EOFError:
        print("\nNo input detected, exiting.")
        exit(0)

def main():
    tracker = HabitTracker()
    reminders = ReminderSystem(tracker)
    analytics = HabitStats(tracker.habits)

    while True:
        display_menu()
        choice = safe_input("Choose an option (1-5): ")

        if choice == "1":
            # Add New Habit
            print("\n" + "-"*40)
            print("ADD NEW HABIT")
            name = safe_input("Habit name (e.g., 'Read'): ")
            frequency = safe_input("Frequency (daily/weekly/monthly): ").lower()
            reminder = safe_input("Reminder time (HH:MM) or leave blank: ")
            tracker.add_habit(name, frequency, reminder if reminder else None)
            print(f"\n✅ '{name}' added successfully!")
            safe_input("Press Enter to continue...")

        elif choice == "2":
            # Mark Habit Complete
            print("\n" + "-"*40)
            print("YOUR HABITS:")
            for i, name in enumerate(tracker.habits.keys(), 1):
                print(f"{i}. {name}")
            
            try:
                habit_num = int(safe_input("\nEnter habit number to mark complete: ")) - 1
                habit_name = list(tracker.habits.keys())[habit_num]
                tracker.habits[habit_name].completions.append(datetime.now().isoformat())
                tracker.save()
                print(f"\n✅ '{habit_name}' marked complete for today!")
            except (ValueError, IndexError):
                print("\n❌ Invalid selection")
            safe_input("Press Enter to continue...")

        elif choice == "3":
            # View Reminders
            print("\n" + "-"*40)
            print("REMINDERS & ALERTS")
            due = reminders.check_due_reminders()
            missed = reminders.check_missed_habits()
            
            if due:
                print("\n🔔 Due Now:")
                for habit in due:
                    print(f"- {habit} ({tracker.habits[habit].reminder_time})")
            else:
                print("\nNo habits due right now.")
            
            if missed:
                print("\n⚠️ Missed Habits:")
                for habit in missed:
                    print(f"- {habit} (last done: {max(tracker.habits[habit].completions)})")
            else:
                print("\nNo missed habits detected.")
            
            safe_input("\nPress Enter to continue...")

        elif choice == "4":
            # Show Analytics
            print("\n" + "-"*40)
            print("PROGRESS ANALYTICS")
            for i, name in enumerate(tracker.habits.keys(), 1):
                print(f"{i}. {name}")
            
            try:
                habit_num = int(safe_input("\nEnter habit number to analyze: ")) - 1
                habit_name = list(tracker.habits.keys())[habit_num]
                print(analytics.generate_summary(habit_name))
            except (ValueError, IndexError):
                print("\n❌ Invalid selection")
            safe_input("Press Enter to continue...")

        elif choice == "5":
            print("\nGoodbye! Keep building those habits 💪")
            break

        else:
            print("\n❌ Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()

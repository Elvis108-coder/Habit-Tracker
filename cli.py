from database import session
from models import Habit

class HabitTrackerCLI:
    def __init__(self, user):
        """
        Initialize with the current user
        """
        self.user = user
    
    def display_summary(self):
        """Display a general summary of all habits"""
        habits = session.query(Habit).filter_by(user_id=self.user.id).all()
        if not habits:
            print("\nYou have no habits tracked.")
            return
            
        print("\n=== HABIT SUMMARY ===")
        print(f"Total habits tracked: {len(habits)}")
        
        active = sum(1 for h in habits if h.active)
        print(f"Active habits: {active}")
        print(f"Inactive habits: {len(habits) - active}")
        
        longest_streak = max(h.longest_streak for h in habits) if habits else 0
        print(f"\nLongest streak across all habits: {longest_streak} days")
        
        print("\nCurrent streaks:")
        for habit in habits:
            print(f"- {habit.name}: {habit.current_streak} days")
    
    def display_habit_report(self, habit_id):
        """Display detailed report for a specific habit"""
        habit = session.query(Habit).filter_by(id=habit_id, user_id=self.user.id).first()
        
        if not habit:
            print("Habit not found!")
            return
            
        print(f"\n=== DETAILED REPORT: {habit.name.upper()} ===")
        print(f"Frequency: {habit.frequency}")
        print(f"Created on: {habit.created_at}")
        print(f"Current streak: {habit.current_streak} days")
        print(f"Longest streak: {habit.longest_streak} days")
        print(f"Completion rate: {habit.completion_rate}%")
        print(f"Status: {'Active' if habit.active else 'Inactive'}")
        
        if habit.missed_days:
            print("\nRecently missed days:")
            for day in habit.missed_days[-3:]:
                print(f"- {day}")

def use_env(user):
    cli = HabitTrackerCLI(user)
    
    while True:
        print(f"\n👤 Logged in as: {user.username}")  # Display username instead of object
        print("[1] View Habits")
        print("[2] Delete Habit")
        print("[3] Create Habit")
        print("[4] View Summary Report")
        print("[5] View Detailed Habit Report")
        print("[6] Logout")
        choice = input("Choose an option: ")

        if choice == "1":
            view_habits(user)
        elif choice == "2":
            delete_habit(user)
        elif choice == "3":
            create_habit(user)
        elif choice == "4":
            cli.display_summary()
        elif choice == "5":
            view_habits(user)  # Show list first
            habit_id = input("\nEnter the ID of the habit to view report: ")
            cli.display_habit_report(habit_id)
        elif choice == "6":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")

def view_habits(user):  # Added user parameter
    habits = session.query(Habit).filter_by(user_id=user.id).all()
    if not habits:
        print("\nYou have no habits tracked.")
        return
    print("\n📋 Your Habits:")
    for habit in habits:
        print(f"  [{habit.id}] {habit.name} - {habit.frequency}")

def delete_habit(user):  # Added user parameter
    view_habits(user)
    habit_id = input("\nEnter the ID of the habit to delete: ")
    habit = session.query(Habit).filter_by(id=habit_id, user_id=user.id).first()
    if habit:
        session.delete(habit)
        session.commit()
        print(f"Habit '{habit.name}' deleted.")
    else:
        print("Habit not found.")

def create_habit(user):  # Added user parameter
    name = input("Enter habit name: ")
    frequency = input("Enter frequency (e.g. daily, weekly): ")
    new_habit = Habit(name=name, frequency=frequency, user_id=user.id)
    session.add(new_habit)
    session.commit()
    print(f"Habit '{name}' added.")
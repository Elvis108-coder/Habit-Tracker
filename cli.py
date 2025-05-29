import datetime
import os
from database import get_session
from models import Habit, CheckIn
from analytics.stats import HabitStats  # Assuming stats.py for stats/graph

def user_menu(user):
    while True:
        print("\n==== Habit Tracker Menu ====")
        print("1. Add Habit")
        print("2. View Habits")
        print("3. Delete Habit")
        print("4. Log Check-in")
        print("5. View Check-in History")
        print("6. Show Stats")
        print("7. Show Graph")
        print("0. Exit")
        
        choice = input("Choose an option: ").strip()
        
        if choice == "1":
            name = input("Enter habit name: ").strip()
            if name:
                add_habit(user, name)
            else:
                print("❌ Habit name cannot be empty.")
        
        elif choice == "2":
            view_habits(user)
        
        elif choice == "3":
            delete_habit(user)
        
        elif choice == "4":
            log_check_in(user)
        
        elif choice == "5":
            view_check_in_history(user)
        
        elif choice == "6":
            show_stats(user)
        
        elif choice == "7":
            show_graph(user)
        
        elif choice == "0":
            print("Goodbye! 👋")
            break
        
        else:
            print("❌ Invalid choice, please try again.")

def add_habit(user, name):
    session = get_session()
    try:
        new_habit = Habit(name=name, user_id=user.id)  # Fix: use user.id
        session.add(new_habit)
        session.commit()
        print(f"✅ Habit '{name}' added.")
    except Exception as e:
        session.rollback()
        print(f"❌ Error adding habit: {e}")
    finally:
        session.close()

def view_habits(user):
    session = get_session()
    try:
        habits = session.query(Habit).filter_by(user_id=user.id).all()
        if not habits:
            print("You have no habits.")
        else:
            for habit in habits:
                print(f"[{habit.id}] {habit.name}")
    except Exception as e:
        print(f"❌ Error viewing habits: {e}")
    finally:
        session.close()

def delete_habit(user):
    session = get_session()
    try:
        habits = session.query(Habit).filter_by(user_id=user.id).all()
        if not habits:
            print("You have no habits to delete.")
            return

        for habit in habits:
            print(f"[{habit.id}] {habit.name}")

        habit_id = int(input("Enter habit ID to delete: "))
        habit_to_delete = session.query(Habit).filter_by(id=habit_id, user_id=user.id).first()
        if habit_to_delete:
            session.delete(habit_to_delete)
            session.commit()
            print(f"🗑️  Habit '{habit_to_delete.name}' deleted.")
        else:
            print("❌ Habit not found.")
    except ValueError:
        print("❌ Invalid ID.")
    except Exception as e:
        session.rollback()
        print(f"❌ Error deleting habit: {e}")
    finally:
        session.close()

def log_check_in(user):
    session = get_session()
    try:
        view_habits(user)
        habit_id = int(input("Enter habit ID to check-in: "))
        habit = session.query(Habit).filter_by(id=habit_id, user_id=user.id).first()
        today = datetime.date.today()
        if habit:
            already_checked_in = session.query(CheckIn).filter_by(habit_id=habit.id, check_in_date=today).first()
            if not already_checked_in:
                checkin = CheckIn(habit_id=habit.id, check_in_date=today)
                session.add(checkin)
                session.commit()
                print(f"✅ Checked in '{habit.name}' for {today}")
            else:
                print("⚠️ Already checked in today.")
        else:
            print("❌ Habit not found.")
    except ValueError:
        print("❌ Invalid ID.")
    except Exception as e:
        session.rollback()
        print(f"❌ Error logging check-in: {e}")
    finally:
        session.close()

def view_check_in_history(user):
    session = get_session()
    try:
        view_habits(user)
        habit_id = int(input("Enter habit ID: "))
        habit = session.query(Habit).filter_by(id=habit_id, user_id=user.id).first()
        if habit:
            check_ins = session.query(CheckIn).filter_by(habit_id=habit.id).order_by(CheckIn.check_in_date).all()
            if not check_ins:
                print("No check-ins for this habit.")
            else:
                print(f"Check-in history for '{habit.name}':")
                for ci in check_ins:
                    print(f"📅 {ci.check_in_date}")
        else:
            print("❌ Habit not found.")
    except ValueError:
        print("❌ Invalid ID.")
    except Exception as e:
        print(f"❌ Error viewing check-in history: {e}")
    finally:
        session.close()

def show_stats(user):
    session = get_session()
    try:
        habits = session.query(Habit).filter_by(user_id=user.id).all()
        if not habits:
            print("No habits to show stats for.")
            return

        stats = HabitStats(user)  # Assuming HabitStats in analytics/stats.py
        for habit in habits:
            check_ins = session.query(CheckIn).filter_by(habit_id=habit.id).order_by(CheckIn.check_in_date).all()
            total = len(check_ins)
            streak = stats.get_streak(habit)  # Assume HabitStats has get_streak
            print(f"\n📊 Stats for '{habit.name}':")
            print(f"Total Check-ins: {total}")
            print(f"Current Streak: {streak} day{'s' if streak != 1 else ''}")
    except Exception as e:
        print(f"Error showing stats: {e}")
    finally:
        session.close()

def show_graph(user):
    session = get_session()
    try:
        labels, data = [], []
        habits = session.query(Habit).filter_by(user_id=user.id).all()
        if not habits:
            print("No habits to display.")
            return

        stats = HabitStats(user)
        for habit in habits:
            labels.append(habit.name)
            count = stats.get_weekly_check_in_count(habit.id)  # Assume HabitStats method
            data.append([count])

        with open("graph_data.txt", "w") as f:
            for label, counts in zip(labels, data):
                f.write(f"{label}: {' '.join(map(str, counts))}\n")

        os.system("termgraph graph_data.txt --color green")
    except Exception as e:
        print(f"❌ Error showing graph: {e}")
    finally:
        session.close()
        if os.path.exists("graph_data.txt"):
            os.remove("graph_data.txt")
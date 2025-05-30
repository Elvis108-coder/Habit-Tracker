# cli.py

from models import Habit, CheckIn
from database import get_session
import datetime
import os

def add_habit(session, user, name):
    new_habit = Habit(name=name, frequency="daily", user_id=user.id)
    session.add(new_habit)
    session.commit()
    print(f"✅ Habit '{name}' added.")
    session.close()

def view_habits(session, user):
    habits = session.query(Habit).filter_by(user_id=user.id).all()
    if not habits:
        print("You have no habits.")
        return
    for habit in habits:
        print(f"[{habit.id}] {habit.name}")
    session.close()

def delete_habit(session, user):
    habits = session.query(Habit).filter_by(user_id=user.id).all()
    if not habits:
        print("You have no habits to delete.")
        return
    for habit in habits:
        print(f"[{habit.id}] {habit.name}")
    try:
        habit_id = int(input("Enter habit ID to delete: "))
    except ValueError:
        print("❌ Invalid ID.")
        return
    habit_to_delete = session.query(Habit).filter_by(id=habit_id, user_id=user.id).first()
    if habit_to_delete:
        session.delete(habit_to_delete)
        session.commit()
        print(f"🗑️  Habit '{habit_to_delete.name}' deleted.")
    else:
        print("❌ Habit not found.")
    session.close()

def log_check_in(user):
    session = get_session()
    habits = session.query(Habit).filter_by(user_id=user.id).all()
    if not habits:
        print("No habits found.")
        session.close()
        return
    for habit in habits:
        print(f"[{habit.id}] {habit.name}")
    habit_id = input("Enter habit ID to check-in: ")
    try:
        habit = session.query(Habit).filter_by(id=int(habit_id), user_id=user.id).first()
    except ValueError:
        print("Invalid input.")
        session.close()
        return
    today = datetime.date.today()
    existing_checkin = session.query(CheckIn).filter_by(habit_id=habit.id).filter(CheckIn.timestamp >= datetime.datetime.combine(today, datetime.time.min)).first()
    if habit and not existing_checkin:
        checkin = CheckIn(habit_id=habit.id)
        session.add(checkin)
        session.commit()
        print(f"✅ Checked in '{habit.name}' for {today}")
    else:
        print("Already checked in today or habit not found.")
    session.close()

def view_check_in_history(user):
    session = get_session()
    habits = session.query(Habit).filter_by(user_id=user.id).all()
    if not habits:
        print("No habits found.")
        session.close()
        return
    for habit in habits:
        print(f"[{habit.id}] {habit.name}")
    habit_id = input("Enter habit ID: ")
    habit = session.query(Habit).filter_by(id=int(habit_id), user_id=user.id).first()
    if habit:
        check_ins = session.query(CheckIn).filter_by(habit_id=habit.id).order_by(CheckIn.timestamp).all()
        for ci in check_ins:
            print(f"📅 {ci.timestamp}")
    else:
        print("Habit not found.")
    session.close()

def show_stats(user):
    session = get_session()
    for habit in session.query(Habit).filter_by(user_id=user.id).all():
        check_ins = session.query(CheckIn).filter_by(habit_id=habit.id).order_by(CheckIn.timestamp).all()
        total = len(check_ins)
        streak = 0
        today = datetime.date.today()
        for i in range(total - 1, -1, -1):
            days_diff = (today - check_ins[i].timestamp.date()).days
            if days_diff in [0, 1]:
                streak += 1
                today = check_ins[i].timestamp.date()
            else:
                break
        print(f"\n📊 {habit.name}")
        print(f" - Total Check-ins: {total}")
        print(f" - Streak: {streak}")
    session.close()

def show_graph(user):
    session = get_session()
    labels, data = [], []
    for habit in session.query(Habit).filter_by(user_id=user.id).all():
        labels.append(habit.name)
        count = sum(
            (datetime.date.today() - ci.timestamp.date()).days <= 7
            for ci in habit.check_ins
        )
        data.append([count])
    session.close()
    with open("graph_data.txt", "w") as f:
        for l, d in zip(labels, data):
            f.write(f"{l}: {' '.join(map(str, d))}\n")
    os.system("termgraph graph_data.txt --color green")
    os.remove("graph_data.txt")

# ✅ Main interactive menu for logged-in users
def use_env(user):
    while True:
        print("\n📋 Main Menu")
        print("1. Add Habit")
        print("2. View Habits")
        print("3. Delete Habit")
        print("4. Log Check-In")
        print("5. View Check-In History")
        print("6. Show Stats")
        print("7. Show Graph")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter habit name: ")
            add_habit(get_session(), user, name)
        elif choice == "2":
            view_habits(get_session(), user)
        elif choice == "3":
            delete_habit(get_session(), user)
        elif choice == "4":
            log_check_in(user)
        elif choice == "5":
            view_check_in_history(user)
        elif choice == "6":
            show_stats(user)
        elif choice == "7":
            show_graph(user)
        elif choice == "8":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice.")

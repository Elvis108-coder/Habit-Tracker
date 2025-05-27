from models import Habit, CheckIn
from database import session
import datetime
import os

def add_habit(user):
    name = input("Enter habit name: ")
    habit = Habit(name=name, user_id=user.id)
    session.add(habit)
    session.commit()
    print(f"✅ Habit '{name}' added.")

def view_habits(user):
    habits = session.query(Habit).filter_by(user_id=user.id).all()
    if not habits:
        print("No habits.")
    for habit in habits:
        print(f"[{habit.id}] {habit.name}")

def delete_habit(user):
    view_habits(user)
    habit_id = input("Enter habit ID to delete: ")
    habit = session.query(Habit).filter_by(id=int(habit_id), user_id=user.id).first()
    if habit:
        session.delete(habit)
        session.commit()
        print(f"❌ Deleted habit '{habit.name}'.")
    else:
        print("Habit not found.")
        You said:
def log_check_in(user):
    view_habits(user)
    habit_id = input("Enter habit ID to check-in: ")
    habit = session.query(Habit).filter_by(id=int(habit_id), user_id=user.id).first()
    today = datetime.date.today()
    if habit and not session.query(CheckIn).filter_by(habit_id=habit.id, check_in_date=today).first():
        checkin = CheckIn(habit_id=habit.id, check_in_date=today)
        session.add(checkin)
        session.commit()
        print(f"✅ Checked in '{habit.name}' for {today}")
    else:
        print("Already checked in today or habit not found.")

def view_check_in_history(user):
    view_habits(user)
    habit_id = input("Enter habit ID: ")
    habit = session.query(Habit).filter_by(id=int(habit_id), user_id=user.id).first()
    if habit:
        check_ins = session.query(CheckIn).filter_by(habit_id=habit.id).order_by(CheckIn.check_in_date).all()
        for ci in check_ins:
            print(f"📅 {ci.check_in_date}")
    else:
        print("Habit not found.")


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


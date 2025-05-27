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
    
    def show_stats(user):
        for habit in session.query(Habit).filter_by(user_id=user.id).all():
            check_ins = session.query(CheckIn).filter_by(habit_id=habit.id).order_by(CheckIn.check_in_date).all()
            total = len(check_ins)
            streak = 0
            today = datetime.date.today()
            for i in range(total - 1, -1, -1):
                if (today - check_ins[i].check_in_date).days in [0, 1]:
                    streak += 1
                    today = check_ins[i].check_in_date
                else:
                    break
            print(f"\n📊 {habit.name}")
            print(f" - Total Check-ins: {total}")
            print(f" - Streak: {streak}")

def show_graph(user):
    labels, data = [], []
    for habit in session.query(Habit).filter_by(user_id=user.id).all():
        labels.append(habit.name)
        count = sum((datetime.date.today() - ci.check_in_date).days <= 7 for ci in habit.check_ins)
        data.append([count])
    with open("graph_data.txt", "w") as f:
        for l, d in zip(labels, data):
            f.write(f"{l}: {' '.join(map(str, d))}\n")
    os.system("termgraph graph_data.txt --color green")
    os.remove("graph_data.txt")


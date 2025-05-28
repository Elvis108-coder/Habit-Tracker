from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta
import random
from models import Base, User, Habit, CheckIn  # Assuming your models are in models.py

# Database setup
engine = create_engine('sqlite:///habit_tracker.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def create_sample_data():
    # Clear existing data
    session.query(CheckIn).delete()
    session.query(Habit).delete()
    session.query(User).delete()
    session.commit()

    # Create users
    users = [
        User(username="alice", password="password123"),
        User(username="bob", password="securepwd"),
        User(username="charlie", password="test123")
    ]
    session.add_all(users)
    session.commit()

    # Create habits for each user
    habit_names = [
        "Exercise", "Meditation", "Reading", 
        "Drink Water", "Journaling", "Early Bedtime"
    ]
    
    habits = []
    for user in users:
        for i in range(3):  # 3 habits per user
            habit = Habit(
                name=f"{user.username}'s {habit_names[i]}",
                user_id=user.id
            )
            habits.append(habit)
    session.add_all(habits)
    session.commit()

    # Create check-ins for each habit
    for habit in habits:
        # Create check-ins for the past 30 days (randomly skipping some days)
        for day in range(30):
            if random.random() > 0.3:  # 70% chance of checking in each day
                check_in_date = date.today() - timedelta(days=30-day)
                check_in = CheckIn(
                    habit_id=habit.id,
                    check_in_date=check_in_date
                )
                session.add(check_in)
    session.commit()

if __name__ == "__main__":
    create_sample_data()
    print("Database seeded successfully!")
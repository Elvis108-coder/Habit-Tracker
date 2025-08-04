import os
import json
from datetime import datetime
from typing import Dict
from .habit import Habit  # This is your local Habit class (used for JSON)
from database import get_session
from models import Habit as DBHabit  # Import your ORM model

class HabitTracker:
    def __init__(self, data_file, user_id):
        self.data_file = data_file
        self.user_id = user_id
        ...

        self.habits: Dict[str, Habit] = self._load()

    def _load(self) -> Dict[str, Habit]:
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                return {name: Habit(**habit) for name, habit in data.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def add_habit(self, name: str, frequency: str, reminder_time: str = None):
        """Add habit to in-memory store, save to JSON and DB"""
        habit = Habit(
            name=name,
            frequency=frequency,
            created=datetime.now().isoformat(),
            reminder_time=reminder_time
        )
        self.habits[name] = habit
        self.save()

        # ✅ Save to database
        session = get_session()
        db_habit = DBHabit(
            name=name,
            frequency=frequency,
            user_id=self.user_id
        )
        session.add(db_habit)
        session.commit()
        session.close()

    def save(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump({
                name: {
                    "name": habit.name,
                    "frequency": habit.frequency,
                    "created": habit.created,
                    "completions": habit.completions,
                    "reminder_time": habit.reminder_time
                } for name, habit in self.habits.items()
            }, f, indent=2)

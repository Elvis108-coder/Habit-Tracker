import json
from datetime import datetime
from typing import Dict
from .habit import Habit

class HabitTracker:
    def __init__(self, data_file: str = "habits.json"):
        self.data_file = data_file
        self.habits: Dict[str, Habit] = self._load()

    def _load(self) -> Dict[str, Habit]:
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                return {name: Habit(**habit) for name, habit in data.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def add_habit(self, name: str, frequency: str, reminder_time: str = None):
        """Ensure created timestamp is generated here"""
        self.habits[name] = Habit(
            name=name,
            frequency=frequency,
            created=datetime.now().isoformat(),  # Fix: Store proper ISO timestamp
            reminder_time=reminder_time
        )
        self.save()

    def save(self):
        with open(self.data_file, 'w') as f:
            json.dump({
                name: {
                    "name": habit.name,
                    "frequency": habit.frequency,
                    "created": habit.created,  # ISO string
                    "completions": habit.completions,
                    "reminder_time": habit.reminder_time
                } for name, habit in self.habits.items()
            }, f, indent=2)
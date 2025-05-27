from datetime import datetime, timedelta
from typing import List
from .habit import Habit
from .tracker import HabitTracker

class ReminderSystem:
    def __init__(self, tracker: HabitTracker):
        self.tracker = tracker

    def check_missed_habits(self) -> List[str]:
        missed = []
        for name, habit in self.tracker.habits.items():
            if not habit.completions:
                continue
            last_done = max(habit.completions)
            delta = datetime.now() - datetime.fromisoformat(last_done)
            
            if (habit.frequency == "daily" and delta.days >= 1) or \
               (habit.frequency == "weekly" and delta.days >= 7) or \
               (habit.frequency == "monthly" and delta.days >= 30):
                missed.append(name)
        return missed

    def check_due_reminders(self) -> List[str]:
        current_time = datetime.now().strftime("%H:%M")
        return [
            name for name, habit in self.tracker.habits.items()
            if habit.reminder_time == current_time
        ]
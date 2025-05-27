from datetime import datetime
from typing import Dict
from .habit import Habit

class HabitAnalytics:
    def __init__(self, habits: Dict[str, Habit]):
        self.habits = habits

    def calculate_streak(self, habit_name: str) -> Dict[str, int]:
        completions = sorted(self.habits[habit_name].completions)
        streaks = {"current": 0, "longest": 0}
        prev_date = None

        for date_str in completions:
            current_date = datetime.fromisoformat(date_str).date()
            if prev_date and (current_date - prev_date).days == 1:
                streaks["current"] += 1
            else:
                streaks["current"] = 1
            streaks["longest"] = max(streaks["longest"], streaks["current"])
            prev_date = current_date
        return streaks

    def generate_summary(self, habit_name: str) -> str:
        habit = self.habits[habit_name]
        try:
            created_date = datetime.fromisoformat(habit.created).date()
        except ValueError:
            created_date = datetime.now().date()  # Fallback if invalid format

        total_days = (datetime.now().date() - created_date).days + 1
        completion_rate = (len(habit.completions) / total_days) * 100
        streak = self.calculate_streak(habit_name)

        return f"""
        {habit.name.upper()} (Frequency: {habit.frequency})
        ✅ Completed: {len(habit.completions)}/{total_days} days
        🔥 Current Streak: {streak['current']} days
        🏆 Longest Streak: {streak['longest']} days
        📈 Completion Rate: {completion_rate:.1f}%
        """
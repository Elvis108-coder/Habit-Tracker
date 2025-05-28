from datetime import datetime, timedelta
from typing import Dict
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from .habit import Habit

class HabitStats:
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
            created_date = datetime.now().date()

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

    def generate_periodic_report(self, period: str = "weekly") -> dict:
        report = {}
        today = datetime.now().date()
        
        for name, habit in self.habits.items():
            completions = [datetime.fromisoformat(d).date() for d in habit.completions]
            
            if period == "weekly":
                start_date = today - timedelta(days=today.weekday())
                count = sum(1 for d in completions if d >= start_date)
                target = 7
            else:  # monthly
                start_date = today.replace(day=1)
                count = sum(1 for d in completions if d >= start_date)
                target = 30
            
            report[name] = {"target": target, "completed": count}
        return report

    def plot_completion_trend(self, habit_name: str):
        habit = self.habits[habit_name]
        dates = [datetime.fromisoformat(d).date() for d in habit.completions]
        
        if not dates:
            print("No completion data to plot")
            return

        plt.figure(figsize=(10, 4))
        plt.plot(dates, [1]*len(dates), 'o', markersize=8)
        plt.title(f"Completion Trend: {habit.name}")
        plt.gca().xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
        plt.gcf().autofmt_xdate()
        plt.yticks([])
        plt.grid(axis='x')
        plt.show()
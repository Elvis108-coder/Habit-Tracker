from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Habit:
    name: str
    frequency: str  # "daily", "weekly", "monthly"
    created: str = field(default_factory=lambda: datetime.now().isoformat())
    completions: List[str] = field(default_factory=list)
    reminder_time: Optional[str] = None  # "HH:MM" format only

    def add_completion(self, timestamp: Optional[str] = None):
        """Add a completion record with the current or provided timestamp."""
        timestamp = timestamp or datetime.now().isoformat()
        self.completions.append(timestamp)

    def get_summary(self) -> str:
        """Return a summary string for this habit."""
        return (
            f"Habit: {self.name}\n"
            f"- Frequency: {self.frequency}\n"
            f"- Created: {self.created}\n"
            f"- Total Completions: {len(self.completions)}\n"
            f"- Reminder Time: {self.reminder_time or 'None'}"
        )


class HabitStats:
    def __init__(self, habits: List[Habit]):
        self.habits = habits

    def summarize_habit(self, habit_name: str) -> str:
        """Return a summary for the habit with the given name."""
        habit = next((h for h in self.habits if h.name == habit_name), None)

        if not habit:
            return f"No habit found with the name '{habit_name}'."

        return habit.get_summary()

    def list_all_habits(self) -> str:
        """Return a list of all habit names with their index."""
        return "\n".join([f"{idx}. {habit.name}" for idx, habit in enumerate(self.habits)])

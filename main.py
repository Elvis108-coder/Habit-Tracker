from datetime import datetime, timedelta
from analytics.tracker import HabitTracker
from analytics.reminders import ReminderSystem
from analytics.analytics import HabitAnalytics

def main():
    tracker = HabitTracker()
    reminders = ReminderSystem(tracker)
    analytics = HabitAnalytics(tracker.habits)

    # Add sample habits
    tracker.add_habit("Read", "daily", "20:00")
    tracker.add_habit("Exercise", "weekly")

    # Mark completions with PROPER ISO timestamps
    tracker.habits["Read"].completions.extend([
        (datetime.now() - timedelta(days=1)).isoformat(),
        datetime.now().isoformat()
    ])
    tracker.save()

    # Check system
    print("Missed habits:", reminders.check_missed_habits())
    print("Due reminders:", reminders.check_due_reminders())
    print(analytics.generate_summary("Read"))

if __name__ == "__main__":
    main()
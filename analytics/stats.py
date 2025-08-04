from datetime import date, timedelta
from sqlalchemy import func

from database import get_session
from models import Habit, CheckIn

class HabitStats:
    def __init__(self, user_id):
        self.user_id = user_id
        self.session = get_session()

    def get_total_check_ins(self, habit_id):
        return self.session.query(CheckIn).filter_by(habit_id=habit_id).count()

    def get_streak(self, habit):
        # Fetch check-ins for this habit, most recent first
        check_ins = (
            self.session.query(CheckIn)
            .filter_by(habit_id=habit.id)
            .order_by(CheckIn.timestamp.desc())
            .all()
        )

        if not check_ins:
            return 0

        streak = 0
        today = date.today()
        expected_day = today

        # Build a set of dates for quick lookup
        checkin_dates = {ci.timestamp.date() for ci in check_ins}

        while expected_day in checkin_dates:
            streak += 1
            expected_day = expected_day - timedelta(days=1)

        return streak

    def get_weekly_check_in_count(self, habit_id):
        today = date.today()
        week_ago = today - timedelta(days=7)
        return (
            self.session.query(CheckIn)
            .filter(
                CheckIn.habit_id == habit_id,
                func.date(CheckIn.timestamp) >= week_ago
            )
            .count()
        )

    def summarize_habit(self, habit):
        """Returns a summary of a habit's statistics."""
        total_check_ins = self.get_total_check_ins(habit.id)
        current_streak = self.get_streak(habit)
        weekly_count = self.get_weekly_check_in_count(habit.id)

        return (
            f"\n📊 Habit: {habit.name}\n"
            f"🟢 Frequency: {habit.frequency}\n"
            f"✅ Total Check-ins: {total_check_ins}\n"
            f"🔥 Current Streak: {current_streak} days\n"
            f"📅 Check-ins this Week: {weekly_count}\n"
        )

    def close(self):
        self.session.close()

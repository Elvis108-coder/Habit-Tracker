import datetime
from database import get_session
from models import Habit, CheckIn

class HabitStats:
    def __init__(self, user_id):
        self.user_id = user_id
        self.session = get_session()

    def get_total_check_ins(self, habit_id):
        return self.session.query(CheckIn).filter_by(habit_id=habit_id).count()

    def get_streak(self, habit):
        check_ins = self.session.query(CheckIn).filter_by(
            habit_id=habit.id
        ).order_by(CheckIn.check_in_date.desc()).all()

        if not check_ins:
            return 0

        streak = 0
        today = datetime.date.today()

        for i, check_in in enumerate(check_ins):
            expected_date = today - datetime.timedelta(days=i)
            if check_in.check_in_date == expected_date:
                streak += 1
            else:
                break

        return streak

    def get_weekly_check_in_count(self, habit_id):
        today = datetime.date.today()
        week_ago = today - datetime.timedelta(days=7)
        return self.session.query(CheckIn).filter(
            CheckIn.habit_id == habit_id,
            CheckIn.check_in_date >= week_ago
        ).count()

    def close(self):
        self.session.close()

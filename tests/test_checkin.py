import unittest
from test_db_setup import setup_test_db
from models import User, Habit, CheckIn
from datetime import datetime


class TestCheckIn(unittest.TestCase):
    def setUp(self):
        self.session = setup_test_db()
        self.user = User(username="checkintest", password="hashed")
        self.session.add(self.user)
        self.session.commit()

        self.habit = Habit(name="Journal", frequency="daily", user_id=self.user.id)
        self.session.add(self.habit)
        self.session.commit()

    def test_add_checkin(self):
        checkin = CheckIn(habit_id=self.habit.id)
        self.session.add(checkin)
        self.session.commit()

        habit = self.session.query(Habit).filter_by(name="Journal").first()
        self.assertEqual(len(habit.check_ins), 1)
        self.assertIsInstance(habit.check_ins[0].timestamp, datetime)


if __name__ == "__main__":
    unittest.main()
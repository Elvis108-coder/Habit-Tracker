import unittest
from database import session
from models import User, Habit, CheckIn
from datetime import datetime


class TestModels(unittest.TestCase):
    def setUp(self):
        session.query(CheckIn).delete()
        session.query(Habit).delete()
        session.query(User).delete()
        session.commit()

    def test_user_habit_relationship(self):
        user = User(username="modeluser", password="hashed")
        session.add(user)
        session.commit()

        habit = Habit(name="Exercise", frequency="daily", user_id=user.id)
        session.add(habit)
        session.commit()

        fetched_user = session.query(User).filter_by(username="modeluser").first()
        self.assertEqual(len(fetched_user.habits), 1)
        self.assertEqual(fetched_user.habits[0].name, "Exercise")

    def test_habit_checkin_relationship(self):
        user = User(username="checkuser", password="hashed")
        session.add(user)
        session.commit()

        habit = Habit(name="Read", frequency="daily", user_id=user.id)
        session.add(habit)
        session.commit()

        checkin = CheckIn(habit_id=habit.id)
        session.add(checkin)
        session.commit()

        fetched_habit = session.query(Habit).filter_by(name="Read").first()
        self.assertEqual(len(fetched_habit.check_ins), 1)
        self.assertIsInstance(fetched_habit.check_ins[0].timestamp, datetime)


if __name__ == "__main__":
    unittest.main()
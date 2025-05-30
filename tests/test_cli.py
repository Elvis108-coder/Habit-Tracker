import unittest
from unittest.mock import patch
from cli import create_habit, delete_habit, view_habits
from models import Habit, User
from test_db_setup import setup_test_db

class TestCLI(unittest.TestCase):
    def setUp(self):
        self.session = setup_test_db()
        self.user = User(username="cliuser", password="hashed")
        self.session.add(self.user)
        self.session.commit()

    @patch("builtins.input", side_effect=["Drink Water", "daily"])
    def test_create_habit(self, mock_input):
        create_habit()
        habit = self.session.query(Habit).filter_by(name="Drink Water").first()
        self.assertIsNotNone(habit)
        self.assertEqual(habit.frequency, "daily")

    @patch("builtins.input", side_effect=["1"])
    def test_delete_habit(self, mock_input):
        habit = Habit(name="Stretch", frequency="daily", user_id=self.user.id)
        self.session.add(habit)
        self.session.commit()

        # Replace view_habits session temporarily for test isolation
        delete_habit()
        deleted = self.session.query(Habit).filter_by(name="Stretch").first()
        self.assertIsNone(deleted)

    def test_view_habits_empty(self):
        with patch("builtins.print") as mock_print:
            view_habits()
            mock_print.assert_any_call("\nYou have no habits tracked.")


if __name__ == "__main__":
    unittest.main()
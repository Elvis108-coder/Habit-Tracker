import unittest
from auth import register, login
from database import session
from models import User


class TestAuth(unittest.TestCase):
    def setUp(self):
        # Clear existing users before each test
        session.query(User).delete()
        session.commit()

    def test_register_success(self):
        user = register("testuser", "password123")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "testuser")

    def test_register_duplicate_username(self):
        register("duplicateuser", "pass1")
        user = register("duplicateuser", "pass2")
        self.assertIsNone(user)

    def test_login_success(self):
        register("loginuser", "mypassword")
        user = login("loginuser", "mypassword")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "loginuser")

    def test_login_invalid_password(self):
        register("secureuser", "correctpass")
        user = login("secureuser", "wrongpass")
        self.assertIsNone(user)

    def test_login_nonexistent_user(self):
        user = login("ghostuser", "any")
        self.assertIsNone(user)


if __name__ == "__main__":
    unittest.main()
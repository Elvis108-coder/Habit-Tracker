#Habit Tracker CLI App

A simple yet powerful CLI application for tracking user habits and goals using **Python** and **SQLAlchemy ORM** with a **SQLite** database.

---

## Features

- Create and manage **Users**
- Add and track **Goals/Habits**
- View user profiles and goals
- Update user details and goal progress
- Delete users and their goals
- Error handling for integrity and input issues
- Confirmation prompts before update/delete actions

---

##  Tech Stack

- **Python 3.10+**
- **SQLAlchemy**
- **SQLite** (via `sqlitebrowser.org` for GUI inspection)
- **Command-Line Interface**

---

##  Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/habit-tracker.git
cd habit-tracker

Install Dependencies
pip install sqlalchemy

Install SQLite Browser (GUI to view DB)

sudo apt update
sudo apt install sqlitebrowser
sqlitebrowser &

Running the App
python main.py

You'll be presented with a menu of options:
Options:
1. Add User
2. Add Goal
3. Query Users
4. Query Goals
5. Update User
6. Update Goal
7. Delete User
8. Delete Goal
9. Exit


Project Structure
habit-tracker/
│
├── main.py          # Main CLI logic and menu loop
├── models.py        # (Optional) SQLAlchemy ORM models
├── utils.py         # (Optional) Helper functions (get_user, confirm_action, etc.)
└── README.md        # This file


Core Functions
Users
add_user() – Create a new user

update_user() – Edit user details (name, username, email)

delete_user() – Delete a user and all related goals

Goals
add_goal() – Add a new goal for a user

query_goals() – View all goals for a user

update_goal() – Modify a goal's details

delete_goal() – Delete a specific goal

Error Handling
Handles duplicate usernames/emails using IntegrityError

Validates date format (expects YYYY-MM-DD)

Confirms actions like update or delete with yes/no prompts

Author
Allan Ochieng Otieno – https://github.com/Ruler8/Phase_3_PRJ
Elvis Rotich
Ian Kipsang
Warioba Ajona



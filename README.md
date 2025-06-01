# Habit-Tracker
Habit Tracker CLI
A terminal-based Habit Tracking Application built using Python, SQLAlchemy, and SQLite. This app allows users to create accounts, log in securely, and manage their personal habits and check-ins through a command-line interface.

# Project Overview
Habit formation is a key aspect of personal development, and tracking habits can lead to higher consistency and motivation. This CLI-based Habit Tracker is designed to simplify the process of tracking daily or weekly habits. Users can register, log in securely, add habits, check in on their progress, and delete habits — all from the terminal.

# Features
User Management
User Registration with secure password hashing using bcrypt

User Login with validation and session management

Habit Tracking
Add new habits (daily, weekly, etc.)

View all existing habits

Delete habits

Check-In System
Log daily/weekly check-ins for individual habits

View check-in history

# CLI Interface
Simple and intuitive text-based UI using command-line prompts

Secure Authentication
Passwords are stored securely using bcrypt hashing

Duplicate usernames are not allowed

Unit Testing
Automated unit tests using Python’s built-in unittest module

Tests cover authentication, habit creation, and relationship models

# Tech Stack
Tool	Purpose
Python 3.13+	Main programming language
SQLite	Lightweight relational database for storing user and habit data
SQLAlchemy	ORM (Object Relational Mapping) to interact with SQLite
bcrypt	Hashing passwords for secure authentication
unittest	Python's built-in testing framework for writing and running tests
# How to Run the Project
1. Clone the Repository

git clone https://github.com/your-username/habit-tracker.git
cd habit-tracker
2. Install Dependencies
It’s recommended to use Pipenv for managing dependencies.


pipenv install
Alternatively, using pip:


pip install -r requirements.txt
3. Run the Application

pipenv run python app.py
4. Running Unit Tests

python -m unittest discover tests
Testing & Error Handling
# This project includes unit tests for:

User registration and login (tests/test_auth.py)

ORM relationships between User, Habit, and CheckIn models (tests/test_models.py)

Example coverage:

Duplicate usernames

Invalid login credentials

Valid and invalid user authentication

Proper creation of related models (e.g., user.habits, habit.check_ins)

Error handling is implemented in key user-input areas, such as:

Invalid ID input when deleting habits

Empty username/password on login

Missing relationships during habit creation

# Project Structure
habit-tracker/
├── app.py             # Main entry point of the CLI app
├── cli.py             # Command-line interface logic
├── auth.py            # User registration and login logic
├── models.py          # SQLAlchemy ORM model definitions
├── database.py        # Session and engine setup for SQLAlchemy
├── tests/             # Unit test files
│   ├── __init__.py
│   ├── test_auth.py
│   └── test_models.py
├── README.md
└── requirements.txt   # Project dependencies
# Relationships
Defined in models.py using SQLAlchemy:

User → Habit (One-to-Many): A user can have many habits.

Habit → CheckIn (One-to-Many): A habit can have many check-ins.

These relationships enable:

Accessing a user’s habits via user.habits

Accessing a habit’s check-ins via habit.check_ins

Automatic backreferences (e.g., habit.user, checkin.habit)

# Demo Video
Watch the Demo Here:
[Insert Google Drive or YouTube Link]

# Future Improvements
Add reminders via email or desktop notification

Add timestamps to check-ins

Data visualization (e.g., check-in streaks)

Export/import user data

Monthly reporting
# Authors
<Allan>
<Elvis>
<Warioba>




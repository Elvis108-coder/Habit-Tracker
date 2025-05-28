from models import User
from database import get_session
from cli import add_habit, view_habits, delete_habit, log_check_in, view_check_in_history, show_stats, show_graph  # Adjust import if needed

def test_features():
    session = get_session()
    # Create a test user
    user = session.query(User).first()
    if not user:
        user = User(name="Test User", email="test@example.com")
        session.add(user)
        session.commit()
    
    print("=== Testing Add Habit ===")
    add_habit(user)
    
    print("\n=== Testing View Habits ===")
    view_habits(user)
    
    print("\n=== Testing Log Check-In ===")
    log_check_in(user)
    
    print("\n=== Testing Check-In History ===")
    view_check_in_history(user)
    
    print("\n=== Testing Stats ===")
    show_stats(user)
    
    print("\n=== Testing Graph ===")
    show_graph(user)
    
    print("\n=== Testing Delete Habit ===")
    delete_habit(user)
    
    session.close()

if __name__ == "__main__":
    test_features()
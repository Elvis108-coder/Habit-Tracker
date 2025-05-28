def main_menu():
    print("\n🌱 Welcome to Habit Tracker CLI 🌱")
    print("[1] Register")
    print("[2] Login")
    print("[3] Exit")
    return input("Choose an option: ")

if __name__ == "__main__":
    while True:
        choice = main_menu()
        if choice == "1":
            print("You chose to register.")
        elif choice == "2":
            print("You chose to login.")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

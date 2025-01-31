from datetime import datetime

def add_note():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_note = input("Please enter your note here: ")
    with open("MyNote.txt", "a") as file:
        file.write(f"{timestamp}: {user_note}\n")
    print("Note added successfully!")

def view_notes():
    try:
        with open("MyNote.txt", "r") as file:
            notes = file.read()
            if notes:
                print("Your notes:")
                print(notes)
            else:
                print("No notes found.")
    except FileNotFoundError:
        print("No notes found. Add some notes first!")


def get_user_choice():
    while True:
        print("\nHello, here is your PyDairy! \nWhat would you like to do? \n1. Add Note \n2. View Notes \n3. Exit")
        choice = input("Please choose your option (1/2/3): ").strip().lower()

        if choice in ['1', 'add', 'add note']:
            return '1'
        elif choice in ['2', 'view', 'view notes']:
            return '2'
        elif choice in ['3', 'exit', 'quit']:
            return '3'
        else:
            print("Invalid option. Please try again.")


def main():
    while True:
        choice = get_user_choice()

        if choice == '1':
            add_note()
        elif choice == '2':
            view_notes()
        elif choice == '3':
            print("Thank you for using PyDairy!")
            break


if __name__ == "__main__":
    main()



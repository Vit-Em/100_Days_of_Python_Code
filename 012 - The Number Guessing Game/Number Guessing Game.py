import random

LOGO = """
 _____                     _____ _          _____           _             
|   | |_ _ _____ ___ ___  |_   _| |_ ___   |   | |_ _ _____ |_|___ ___ ___ 
| | | | | |     | -_|  _|   | | |   | -_|  | | | | | |     | | -_|  _|_ -|
|_|___|___|_|_|_|___|_|     |_| |_|_|___|  |_|___|___|_|_|_|_|___|_| |___|
"""

def clear_screen():
    print("\n" * 100)

def get_difficulty():
    while True:
        level = input("Choose a difficulty. Type 'easy' or 'hard': ").lower()
        if level in ['easy', 'hard']:
            return 10 if level == 'easy' else 5
        print("Invalid input. Please type 'easy' or 'hard'.")

def play_game():
    print(LOGO)
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.\n")

    secret_number = random.randint(1, 100)
    attempts = get_difficulty()

    print(f"You have {attempts} attempts remaining to guess the number.\n")

    while attempts > 0:
        print(f"You have {attempts} attempts remaining to guess the number.")
        guess = input("Make a guess: ")
        
        if not guess.isdigit() or int(guess) < 1 or int(guess) > 100:
            print("Please enter a valid number between 1 and 100.")
            continue

        guess = int(guess)
        
        if guess == secret_number:
            print(f"You got it! The answer was {secret_number}.")
            return True
        
        print("Too high!" if guess > secret_number else "Too low!")
        attempts -= 1

    print(f"\nYou've run out of guesses. The number was {secret_number}.")
    return False

def main():
    while True:
        clear_screen()
        if play_game():
            print("\nCongratulations! You won!")
        else:
            print("\nBetter luck next time!")
        
        if input("\nDo you want to play again? (y/n): ").lower() != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()

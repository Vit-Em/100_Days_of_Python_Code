import random

ROCK = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

PAPER = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

SCISSORS = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

GAME_IMAGES = [ROCK, PAPER, SCISSORS]
CHOICES = ["Rock", "Paper", "Scissors"]

def get_user_choice():
    while True:
        try:
            choice = int(input("What do you choose? 0 for Rock, 1 for Paper, 2 for Scissors\n"))
            if 0 <= choice <= 2:
                return choice
            else:
                print("Please enter a number between 0 and 2.")
        except ValueError:
            print("Please enter a valid number.")

def determine_winner(user, computer):
    if user == computer:
        return "It's a draw!"
    elif (user == 0 and computer == 2) or (user == 1 and computer == 0) or (user == 2 and computer == 1):
        return "You win!"
    else:
        return "You lose!"

def play_game():
    user_choice = get_user_choice()
    computer_choice = random.randint(0, 2)

    print(f"\nYou chose {CHOICES[user_choice]}:")
    print(GAME_IMAGES[user_choice])

    print(f"\nComputer chose {CHOICES[computer_choice]}:")
    print(GAME_IMAGES[computer_choice])

    result = determine_winner(user_choice, computer_choice)
    print(f"\n{result}")

if __name__ == "__main__":
    play_game()

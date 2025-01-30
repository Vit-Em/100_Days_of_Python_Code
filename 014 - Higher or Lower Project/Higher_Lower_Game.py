from random import randint
from art import logo, vs
from game_data import data

lives = 6
score = 0
print(logo)                             #Print game logo


def get_random_account():
    return randint(0, len(data) - 1)


def format_data(account):
    name = data[account]["name"]
    description = data[account]["description"]
    country = data[account]["country"]
    return f"{name}, a {description}, from {country}"


def check_answer(guess, a_followers, b_followers):
    if a_followers > b_followers:
        return guess == "A"
    else:
        return guess == "B"


def high_or_low():
    global lives, score
    choice_a = get_random_account()
    choice_b = get_random_account()

    while lives > 0:
        while choice_a == choice_b:
            choice_b = get_random_account()

        print(f"You have {lives} attempts.\nCompare A: {format_data(choice_a)}.")
        print(vs)
        print(f"\nAgainst B: {format_data(choice_b)}.")

        guess = input("Who has more followers? Type 'A' or 'B': ").upper()
        a_follower_count = data[choice_a]["follower_count"]
        b_follower_count = data[choice_b]["follower_count"]
        if guess == "A" or guess == "B":
            is_correct = check_answer(guess, a_follower_count, b_follower_count)

            if is_correct:
                score += 1
                print(f"You're right! Current score: {score}.")
            else:
                lives -= 1
                print(f"Sorry, that's wrong. You have {lives} lives left. Current score: {score}.")

        elif choice_a == choice_b:
            print("They have the same number of followers. We will start a new set now.")
        else:
            print(f"You have input a wrong symbol {guess}. Please use only letters A or B in your answers!")
        print(f"Game over. Final score: {score}")
                            # Making account at position B become the next account at position A.
        choice_a = choice_b

high_or_low()

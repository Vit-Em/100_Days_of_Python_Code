print("Welcome to Python Pizza Deliveries!")

def get_valid_input(prompt, valid_options):
    while True:
        user_input = input(prompt).upper()
        if user_input in valid_options:
            return user_input
        print(f"Invalid input. Please choose from {', '.join(valid_options)}.")

size = get_valid_input("What size pizza do you want? S, M or L: ", ["S", "M", "L"])
pepperoni = get_valid_input("Do you want pepperoni on your pizza? Y or N: ", ["Y", "N"])
extra_cheese = get_valid_input("Do you want extra cheese? Y or N: ", ["Y", "N"])

size_prices = {"S": 15, "M": 20, "L": 25}
bill = size_prices[size]

if pepperoni == "Y":
    bill += 2 if size == "S" else 3

if extra_cheese == "Y":
    bill += 1

print(f"Your final bill is: ${bill}.")

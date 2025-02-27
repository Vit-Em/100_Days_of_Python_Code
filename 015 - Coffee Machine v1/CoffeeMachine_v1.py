#TODO 1. Make the dictionaries for menu, resources and coins
MENU = {
    "espresso": {
        "ingredients": {"water": 50, "coffee": 18},
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {"water": 200, "milk": 150, "coffee": 24},
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {"water": 250, "milk": 100, "coffee": 24},
        "cost": 3.0,
    },
}

resources = {"water": 300, "milk": 200, "coffee": 100, "money": 0.0}
coins = {"quarter": 0.25, "dime": 0.10, "nickle": 0.05, "pennie": 0.01}


# TODO 2 Helper functions
"""Print report"""
def print_report():
    """Print the current resources report."""
    print(f"Water: {resources['water']}ml")
    print(f"Milk: {resources['milk']}ml")
    print(f"Coffee: {resources['coffee']}g")
    print(f"Money: ${resources['money']:.2f}")

"""Check resources"""
def check_resources(drink):
    """Check if resources are sufficient for the selected drink."""
    for ingredient, amount in MENU[drink]["ingredients"].items():
        if resources[ingredient] < amount:
            print(f"Sorry, there is not enough {ingredient}.")
            return False
    return True

"""Process coins"""
def process_coins():
    """Process coins input from the user and calculate the total."""
    print("Please insert coins.")
    total = 0
    for coin, value in coins.items():
        total += int(input(f"How many {coin}s? ")) * value
    return round(total, 2)

"""Check transaction"""
def check_transaction(payment, drink_cost):
    """Check if payment is sufficient and handle change."""
    if payment < drink_cost:
        print("Sorry, that's not enough money. Money refunded.")
        return False
    elif payment > drink_cost:
        change = round(payment - drink_cost, 2)
        print(f"Here is ${change} in change.")
    return True

"""Make coffee"""
def make_coffee(drink):
    """Deduct the ingredients from the resources and serve the drink."""
    for ingredient, amount in MENU[drink]["ingredients"].items():
        resources[ingredient] -= amount
    resources["money"] += MENU[drink]["cost"]
    print(f"Here is your {drink}. Enjoy!")

# TODO 3: Main coffee machine function
def coffee_machine():
    """Main loop for the coffee machine."""
    machine_on = True

    while machine_on:
        choice = input("What would you like? (espresso/latte/cappuccino): ").lower()

        if choice == "off":
            machine_on = False
            print("Turning off the coffee machine. Goodbye!")
        elif choice == "report":
            print_report()
        elif choice in MENU:
            if check_resources(choice):
                payment = process_coins()
                if check_transaction(payment, MENU[choice]["cost"]):
                    make_coffee(choice)
        else:
            print("Invalid choice. Please choose espresso, latte, cappuccino, or type 'off' to turn off.")

# TODO 4: Run the coffee machine
coffee_machine()

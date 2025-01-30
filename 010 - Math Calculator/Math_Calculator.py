import art
import math

def add(n1, n2):
    return n1 + n2

def subtract(n1, n2):
    return n1 - n2

def multiply(n1, n2):
    return n1 * n2

def divide(n1, n2):
    return n1 / n2 if n2 != 0 else "Error: Division by zero"

def power(n1, n2):
    return n1 ** n2

def square_root(n1, _):
    return math.sqrt(n1) if n1 >= 0 else "Error: Cannot calculate square root of a negative number"

operations = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
    "^": power,
    "√": square_root
}

def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_operation():
    while True:
        for symbol in operations:
            print(symbol, end=" ")
        operation_symbol = input("\nPick an operation: ")
        if operation_symbol in operations:
            return operation_symbol
        print("Invalid operation. Please try again.")

def calculator():
    print(art.logo)
    num1 = get_number("What is the first number?: ")

    while True:
        operation_symbol = get_operation()
        num2 = get_number("What is the next number?: ") if operation_symbol != "√" else 0

        calculation = operations[operation_symbol]
        answer = calculation(num1, num2)
        
        if isinstance(answer, str):
            print(answer)
        else:
            print(f"{num1} {operation_symbol} {num2 if operation_symbol != '√' else ''} = {answer:.4f}")

        choice = input(f"Type 'y' to continue calculating with {answer:.4f}, 'n' for a new calculation, or 'q' to quit: ").lower()

        if choice == 'y':
            num1 = answer
        elif choice == 'n':
            calculator()
            return
        elif choice == 'q':
            print("Thank you for using the calculator. Goodbye!")
            return
        else:
            print("Invalid choice. Starting a new calculation.")
            calculator()
            return

if __name__ == "__main__":
    calculator()

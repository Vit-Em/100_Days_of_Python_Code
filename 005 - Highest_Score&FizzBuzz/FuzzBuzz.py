def fizzbuzz(number):
    if number % 3 == 0 and number % 5 == 0:
        return "FizzBuzz"
    elif number % 3 == 0:
        return "Fizz"
    elif number % 5 == 0:
        return "Buzz"
    else:
        return str(number)

def play_fizzbuzz(start, end):
    return [fizzbuzz(num) for num in range(start, end + 1)]

def interactive_fizzbuzz():
    print("Welcome to the FizzBuzz game!")
    while True:
        try:
            number = int(input("Enter a number (or 0 to quit): "))
            if number == 0:
                print("Thanks for playing!")
                break
            print(f"FizzBuzz says: {fizzbuzz(number)}")
        except ValueError:
            print("Please enter a valid number.")

def main():
    # Standard FizzBuzz von 1 bis 100
    results = play_fizzbuzz(1, 100)
    print("Standard FizzBuzz (1-100):")
    print(", ".join(results))

    # Statistik
    fizz_count = results.count("Fizz")
    buzz_count = results.count("Buzz")
    fizzbuzz_count = results.count("FizzBuzz")

    print(f"\nStatistik:")
    print(f"Fizz: {fizz_count}")
    print(f"Buzz: {buzz_count}")
    print(f"FizzBuzz: {fizzbuzz_count}")

    # Interaktiver Modus
    print("\nLet's play FizzBuzz interactively!")
    interactive_fizzbuzz()

if __name__ == "__main__":
    main()

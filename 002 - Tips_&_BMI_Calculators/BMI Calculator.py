# Getting user inputs
print("Welcome to the BMI Calculator! \n")
name = input("Enter your Name: ")
weight = float(input("Please Share your weight (in kg): "))
height = float(input("Please Share your height (in meters): "))

def bmi_calculator(weight, height): # This code calculate the Body Mass Index (BMI) and user category
    bmi = weight / (height ** 2)  # BMI Calculation
    if bmi < 18.5:
        user_has = "Underweight️"
    elif 18.5 <= bmi < 24.9:
        user_has = "Normal Weight"
    elif 25 <= bmi < 29.9:
        user_has = "Overweight"
    else:
        user_has = "Obese"
    return bmi, user_has

bmi, user_has = bmi_calculator(height, weight)  # Recall of BMI and user category
print(f'\n{name}, you are {user_has}, because your BMI is: {round(bmi, 2)}\n')


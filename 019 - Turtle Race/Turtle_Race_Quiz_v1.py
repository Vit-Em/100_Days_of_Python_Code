from turtle import Turtle, Screen
import random

is_race_on = False
colors = ["red", "orange", "yellow", "green", "blue", "purple"]
y_positions = [-70, -40, -10, 20, 50, 80 ]
all_turtles = []

screen = Screen()
screen.setup(width=500, height=400)
user_bet = screen.textinput(title="male your bet", prompt="Witch turtler will you win the race? Enter a color: ")

for turtle_index in range(0, 6):
    new_turtle = Turtle(shape="turtle")
    new_turtle.color(colors[turtle_index])
    new_turtle.penup()
    new_turtle.goto(x=-230, y=y_positions[turtle_index])
    all_turtles.append(new_turtle)


if user_bet:
    is_race_on = True

while is_race_on:


    for turtle in all_turtles:
        if turtle.xcor() > 230:
            is_race_on = False
            winig_color = turtle.pencolor()
            if winig_color == user_bet:
                print(f"You've won. The {winig_color} turtle is winner!")
            else:
                print(f"You've lost. The {winig_color} turtle is winner!")

        rand_distance = random.randint(0,10)
        turtle.forward(rand_distance)



screen.exitonclick()

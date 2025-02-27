from turtle import Turtle, Screen
import random
import time


class TurtleRace:
    def __init__(self):
        self.screen = Screen()
        self.screen.setup(width=800, height=600)
        self.screen.title("Turtle Race Quiz")
        self.colors = ["red", "orange", "yellow", "green", "blue", "purple"]
        self.y_positions = [-100, -60, -20, 20, 60, 100]
        self.all_turtles = []
        self.winner = None
        self.create_turtles()
        self.create_finish_line()
        self.create_start_line()
        self.scoreboard = self.create_scoreboard()
        self.start_button = self.create_start_button()
        self.stamina_bars = self.create_stamina_bars()

    def create_turtles(self):
        for turtle_index in range(6):
            new_turtle = Turtle(shape="turtle")
            new_turtle.color(self.colors[turtle_index])
            new_turtle.penup()
            new_turtle.goto(x=-350, y=self.y_positions[turtle_index])
            new_turtle.stamina = 100
            self.all_turtles.append(new_turtle)

    def create_finish_line(self):
        finish_line = Turtle()
        finish_line.hideturtle()
        finish_line.penup()
        finish_line.goto(350, -150)
        finish_line.pendown()
        finish_line.goto(350, 150)

    def create_start_line(self):
        start_line = Turtle()
        start_line.hideturtle()
        start_line.penup()
        start_line.goto(-350, -150)
        start_line.pendown()
        start_line.goto(-350, 150)

    def create_scoreboard(self):
        scoreboard = Turtle()
        scoreboard.hideturtle()
        scoreboard.penup()
        scoreboard.goto(0, 260)
        return scoreboard

    def update_scoreboard(self, message):
        self.scoreboard.clear()
        self.scoreboard.write(message, align="center", font=("Arial", 16, "normal"))

    def create_start_button(self):
        button = Turtle()
        button.hideturtle()
        button.penup()
        button.goto(0, -250)
        button.write("Start Race", align="center", font=("Arial", 20, "normal"))
        return button

    def create_stamina_bars(self):
        stamina_bars = []
        for i, turtle in enumerate(self.all_turtles):
            bar = Turtle()
            bar.hideturtle()
            bar.penup()
            bar.goto(-390, self.y_positions[i] - 10)
            stamina_bars.append(bar)
        return stamina_bars

    def update_stamina_bars(self):
        for i, turtle in enumerate(self.all_turtles):
            self.stamina_bars[i].clear()
            self.stamina_bars[i].write(f"{'|' * int(turtle.stamina / 10)}", font=("Arial", 8, "normal"))

    def move_turtle(self, turtle):
        if turtle.stamina > 0:
            rand_distance = random.randint(0, 10)
            rand_angle = random.randint(-20, 20)
            turtle.right(rand_angle)
            turtle.forward(rand_distance)
            turtle.setheading(0)  # Reset heading to face right
            turtle.stamina -= random.randint(1, 5)
        else:
            turtle.stamina += random.randint(1, 3)

        # Ensure turtle stays within race bounds
        y = turtle.ycor()
        if y < -130:
            turtle.sety(-130)
        elif y > 130:
            turtle.sety(130)

    def race(self):
        while not self.winner:
            for turtle in self.all_turtles:
                self.move_turtle(turtle)
                if turtle.xcor() > 330:
                    self.winner = turtle.pencolor()
                    return self.winner

            self.update_stamina_bars()
            self.screen.update()  # Update the screen to show movements
            time.sleep(0.1)

    def play_round(self):
        user_bet = self.screen.textinput("Make your bet", "Which turtle will win the race? Enter a color: ")
        if user_bet:
            self.start_button.clear()
            winner = self.race()
            if winner == user_bet:
                self.update_scoreboard(f"You've won! The {winner} turtle is the winner!")
            else:
                self.update_scoreboard(f"You've lost. The {winner} turtle is the winner!")
        self.reset_race()

    def reset_race(self):
        for turtle in self.all_turtles:
            turtle.goto(-350, self.y_positions[self.all_turtles.index(turtle)])
            turtle.setheading(0)
            turtle.stamina = 100
        self.winner = None
        self.update_stamina_bars()
        self.create_start_button()

    def play_game(self):
        self.screen.tracer(0)  # Turn off animation
        self.screen.onscreenclick(self.on_click)
        self.screen.mainloop()

    def on_click(self, x, y):
        if -50 < x < 50 and -270 < y < -230:
            self.play_round()


if __name__ == "__main__":
    game = TurtleRace()
    game.play_game()

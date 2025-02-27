# scoreboard.py
from turtle import Turtle
from read_save_rewrite import read_highscore, update_highscore

ALIGNMENT = "center"
FONT = ("Arial", 24, "normal")

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.highscore = read_highscore()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(0, 270)
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.write(f"Score: {self.score}, Highscore: {self.highscore}", align=ALIGNMENT, font=FONT)


    def reset(self):
        if self.score > self.highscore:
            self.highscore = update_highscore(self.score)
        self.score = 0
        self.update_scoreboard()

    def increase_score(self):
        self.score += 1
        self.update_scoreboard()
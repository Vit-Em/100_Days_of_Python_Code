# score.py
from turtle import Turtle

class Score(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.l_score = 0
        self.r_score = 0
        self.update_score()

    def update_score(self):
        """Update the score displayed on the screen."""
        self.clear()
        self.goto(-100, 200)  # Adjust the position slightly downward (from 250 to 200)
        self.write(f"{self.l_score}", align="center", font=("Courier", 40, "normal"))
        self.goto(100, 200)  # Adjust the position of the right score as well
        self.write(f"{self.r_score}", align="center", font=("Courier", 40, "normal"))

    def l_point(self):
        """Erhöhe den Punktestand für den linken Spieler und aktualisiere die Anzeige."""
        self.l_score += 1
        self.update_score()

    def r_point(self):
        """Erhöhe den Punktestand für den rechten Spieler und aktualisiere die Anzeige."""
        self.r_score += 1
        self.update_score()

    def is_game_over(self):
        """Prüfe, ob einer der Spieler das Spiel gewonnen hat."""
        return self.l_score == 10 or self.r_score == 10

    def get_winner(self):
        """Ermittle den Gewinner des Spiels."""
        if self.l_score == 10:
            return "Left Player"
        else:
            return "Right Player"

    def display_winner(self, winner):
        """Zeige die Sieges-Nachricht."""
        self.clear()
        self.goto(0, 0)
        self.write(f"{winner} wins!", align="center", font=("Courier", 30, "normal"))

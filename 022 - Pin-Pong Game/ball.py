# ball.py
from turtle import Turtle

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.speed_factor = 1.0  # Sicherstellen, dass speed_factor existiert
        self.x_move = 10
        self.y_move = 10
        self.reset_position()  # Jetzt korrekt, da speed_factor definiert ist

    def move(self):
        """Bewege den Ball basierend auf x_move und y_move."""
        self.goto(self.xcor() + self.x_move, self.ycor() + self.y_move)

        # Prüfe, ob der Ball die obere oder untere Kante erreicht
        if self.ycor() > 290 or self.ycor() < -290:  # 290 = Bildschirmhöhe in Turtle-Logik
            self.bounce_y()

    def bounce_x(self):
        """Umkehr der Richtung entlang der X-Achse."""
        self.x_move *= -1
        self.increase_speed()

    def bounce_y(self):
        """Umkehr der Richtung entlang der Y-Achse."""
        self.y_move *= -1

    def increase_speed(self):
        """Erhöhe die Geschwindigkeit des Balls, um das Spiel herausfordernder zu machen."""
        self.speed_factor *= 1.05  # Erhöhe schrittweise die Geschwindigkeit
        self.x_move = 10 * self.speed_factor if self.x_move > 0 else -10 * self.speed_factor
        self.y_move = 10 * self.speed_factor if self.y_move > 0 else -10 * self.speed_factor

    def reset_position(self):
        """Setze den Ball in die Mitte zurück und setze ihn wieder auf die Startgeschwindigkeit."""
        self.goto(0, 0)
        self.speed_factor = 1.0  # Geschwindigkeit zurücksetzen
        self.x_move = 10 * self.speed_factor
        self.y_move = 10 * self.speed_factor

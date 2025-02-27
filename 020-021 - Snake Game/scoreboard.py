from turtle import Turtle

ALIGNMENT = "center"
FONT = ("Courier", 24, "normal")


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.high_score = self.read_highscore()  # Highscore aus Datei laden
        self.hideturtle()
        self.color("white")
        self.penup()
        self.goto(0, 260)  # Position etwas weiter nach unten angepasst
        self.update_scoreboard()
        self.game_over_text = None  # Objekt für "GAME OVER" Text

    def update_scoreboard(self):
        """Aktualisiert die Punktzahl-Anzeige auf dem Bildschirm."""
        self.clear()
        self.write(f"Score: {self.score}  High Score: {self.high_score}", align=ALIGNMENT, font=FONT)

    def increase_score(self):
        """Erhöht die Punktzahl und aktualisiert die Anzeige."""
        self.score += 1
        self.update_scoreboard()

    def reset(self):
        """Setzt das Scoreboard für ein neues Spiel zurück und speichert den High Score."""
        if self.score > self.high_score:
            self.high_score = self.score
            self.write_highscore()  # Neuen High Score speichern
        self.score = 0
        self.update_scoreboard()

    def game_over(self):
        """Zeigt 'GAME OVER' Text auf dem Bildschirm an."""
        if not self.game_over_text:  # Nur erstellen, wenn noch nicht vorhanden
            self.game_over_text = Turtle()
            self.game_over_text.color("white")
            self.game_over_text.hideturtle()
            self.game_over_text.penup()
            self.game_over_text.write("GAME OVER", align=ALIGNMENT, font=FONT)

    def clear_game_over(self):
        """Entfernt den 'GAME OVER' Text."""
        if self.game_over_text:
            self.game_over_text.clear()
            self.game_over_text = None

    def read_highscore(self):
        """Liest den Highscore aus der Datei."""
        try:
            with open("highscore.txt", "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    def write_highscore(self):
        """Schreibt den aktuellen High Score in die Datei."""
        with open("highscore.txt", "w") as file:
            file.write(str(self.high_score))

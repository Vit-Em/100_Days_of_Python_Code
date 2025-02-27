# SnakeGame_main_v2.py

from turtle import Screen
from snake import Snake
import time
from food import Food
from scoreboard import Scoreboard

game_is_on = True


def restart_game():
    """Reset snake, scoreboard und starte ein neues Spiel."""
    global game_is_on
    snake.reset()
    scoreboard.reset()
    setup_controls()  # Steuerung zurücksetzen
    game_is_on = True  # Ermöglicht Neustart


def setup_controls():
    """Setzt Tastatursteuerung für das Snake-Spiel."""
    screen.listen()
    screen.onkey(snake.up, "Up")
    screen.onkey(snake.down, "Down")
    screen.onkey(snake.left, "Left")
    screen.onkey(snake.right, "Right")


def show_restart_dialog():
    """Zeigt den Dialog an: Möchtest du erneut spielen? (Y/N)"""
    global game_is_on
    answer = screen.textinput("Spiel beendet", "Spiel erneut starten? (Y/N)")

    # Überprüfung, ob der Benutzer "Abbrechen" wählt
    if answer is None:  # Benutzer klickt auf "Cancel"/"Abbrechen"
        game_is_on = False
        screen.bye()  # Schließt das Fenster
    elif answer.lower() == "y":  # Neustart des Spiels
        restart_game()
    else:  # Spiel beenden
        game_is_on = False
        screen.bye()

if __name__ == "__main__":
    # Spielbildschirm einrichten
    screen = Screen()
    screen.setup(width=600, height=600)
    screen.bgcolor("black")
    screen.title("My Snake Game")
    screen.tracer(0)

    snake = Snake()
    food = Food()
    scoreboard = Scoreboard()

    setup_controls()

    # Hauptspiel-Schleife
    while game_is_on:
        screen.update()
        time.sleep(0.1)
        snake.move()

        # Kollision mit Essen
        if snake.head.distance(food) < 15:
            food.refresh()
            snake.extend()
            scoreboard.increase_score()

        # Kollision mit dem Schwanz
        for segment in snake.segments[1:]:  # Erster Teil (Kopf) ignorieren
            if snake.head.distance(segment) < 10:
                show_restart_dialog()

        # Kollision mit der Wand
        if abs(snake.head.xcor()) > 280 or abs(snake.head.ycor()) > 280:
            show_restart_dialog()

        if not game_is_on:
            break

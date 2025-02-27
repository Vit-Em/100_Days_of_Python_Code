# read_save_rewrite.py
import os
from datetime import datetime


timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def save_highscore(score):
    # Erstellt oder speichert den neuen Highscore
    try:
        with open("HighScore.txt", "a") as file:
            file.write(f"{timestamp}; {score}\n")
    except OSError as e:
        print(f"Fehler beim Speichern der Highscore-Datei: {e}")


def read_highscore():
    # Liest den höchsten Score aus der Datei oder erstellt eine neue Datei
    try:
        with open("HighScore.txt", "r") as file:
            lines = file.readlines()
            if not lines:
                return 0
            last_score = lines[-1].strip().split(";")
            return int(last_score[1].strip()) if len(last_score) > 1 else 0
    except (FileNotFoundError, ValueError):
        save_highscore(0)  # Neue Datei oder fehlerhafte Datei ersetzen
        return 0


def update_highscore(new_score):
    current_highscore = read_highscore()
    if new_score > current_highscore:
        save_highscore(new_score)
        return new_score
    return current_highscore

# modules/tests_logic.py
import random as rd


def weighted_choice(data):
    """Wählt ein Element aus der Datenliste basierend auf der Gewichtung ('Weight')."""
    if not data:
        print("Keine Daten verfügbar - bitte mindestens ein Wörterbuch auswählen")
        return None
    
    # Weights are now pre-processed and validated during the loading stage.
    weights = [entry["Weight"] for entry in data]
    return rd.choices(data, weights=weights, k=1)[0]

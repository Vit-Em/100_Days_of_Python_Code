# modules/card_logic.py
import random as rd


def weighted_choice(data):
    """Wählt ein Element aus der Datenliste basierend auf der Gewichtung ('Weight')."""
    try:
        # Extrahiere die Gewichte
        weights = [entry.get("Weight", 1.0) for entry in data]

        # Sicherstellen, dass alle Gewichte numerisch sind
        weights = [float(w) if isinstance(w, (int, float)) else 1.0 for w in weights]

        # Auswahl basierend auf den Gewichten treffen
        return rd.choices(data, weights=weights, k=1)[0]

    except Exception as e:
        print(f"Fehler bei der gewichteten Auswahl: {e}")
        # Rückfall auf zufällige Auswahl ohne Gewichte
        return rd.choice(data)

# modules/data_handler.py as data_handler.py
import pandas as pd
from . import translation_api


class WordPair:
    def __init__(self, weight=None, word_1=None, part_1=None, word_2=None, part_2=None):
        self.weight = weight
        self.word_1 = word_1
        self.part_1 = part_1
        self.word_2 = word_2
        self.part_2 = part_2

    def to_dict(self):
        return {
            "Weight": self.weight,
            "Word_1": self.word_1,
            "Part_1": self.part_1,
            "Word_2": self.word_2,
            "Part_2": self.part_2,
        }


def load_data():
    """Lädt die Daten aus der neuen CSV-Tabelle 'Words_deu-rus_v1.csv'."""
    try:
        # CSV-Datei einlesen
        file_path = "data/Words_deu-rus_v1.csv"
        data = pd.read_csv(file_path)

        # Sicherstellen, dass die Gewicht-Spalte vorhanden ist und ggf. leer ist
        if "Weight" not in data.columns:
            data["Weight"] = None  # Initialisieren mit leeren Werten

        # Konvertieren in eine Liste von Dictionaries
        return data.to_dict(orient="records")

    except FileNotFoundError:
        print(f"Die Datei {file_path} wurde nicht gefunden.")
        return []


def fetch_api_word_pairs(
    word: str, source_language: str, target_language: str
):
    """Holt Wortpaare aus der API."""
    word_pairs = []
    translation = translation_api.translate_word(word, source_language, target_language)
    if translation:
        word_pair = WordPair(
            weight="",
            word_1=word,
            part_1="",
            word_2=translation[0],  # Nimmt die erste Übersetzung
            part_2="",
        )
        word_pairs.append(word_pair.to_dict())
    return word_pairs


def load_api_data(self):
    """Führt das Laden von API-Daten im Hintergrund aus."""
    import threading

    threading.Thread(target=self._load_api_data_threaded, daemon=True).start()


def _load_api_data_threaded(self):
    """Lädt API-Daten und aktualisiert die Daten."""
    try:
        if self.fetch_api_word_pairs_func:
            # Beispielwörter für die API-Abfragen
            words = ["Apfel", "Haus", "Buch", "Tisch", "Stuhl"]
            api_data = []

            # API-Daten abrufen
            for word in words:
                word_pairs = self.fetch_api_word_pairs_func(
                    word, self.source_language, self.target_language
                )
                if word_pairs:
                    api_data.extend(word_pairs)

            # API-Daten der Haupt-Datenliste hinzufügen
            self.window.after(0, self.update_data, api_data)
    except Exception as e:
        print(f"Fehler beim Laden der API-Daten: {e}")

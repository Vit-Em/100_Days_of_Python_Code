# translation_api.py
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator  # Importiere Google Translator
import time as tm
import random as rd


def get_random_words_from_wiktionary(language_code: str, count: int):
    """Holt zufällige Wörter von der Wiktionary-Hauptseite oder Spezial:Zufällige_Seite.
    Holt auch die Wortarten, falls verfügbar."""
    base_url = f"https://{language_code}.wiktionary.org/wiki/"
    random_words = []

    # Use Spezial:Zufällige_Seite to fetch random entries
    random_page_url = f"{base_url}Spezial:Zufällige_Seite"

    print(
        f"Starte das Scraping von {count} zufälligen Wörtern vom Wiktionary ({language_code})..."
    )

    for i in range(count):
        try:
            response = requests.get(random_page_url)
            response.raise_for_status()

            # BeautifulSoup für HTML-Parsing
            soup = BeautifulSoup(response.text, "html.parser")

            # Das Wort aus dem Seitentitel extrahieren
            word = soup.find("h1", {"id": "firstHeading"}).text.strip()

            # Suche spezifisch nach Wortart (z. B. Noun, Verb ...)
            # Eine Tabelle mit Wortart suchen (bei Bedarf Debugging aktivieren)
            word_type = "Unknown"
            for table in soup.find_all("table", {"class": "wikitable"}):
                first_row = table.find("tr")
                if first_row and (
                    "Substantiv" in first_row.text or "Verb" in first_row.text
                ):
                    word_type = first_row.text.strip()

            print(f"Wort {i + 1}: {word} ({word_type})")
            random_words.append({"word": word, "type": word_type})

        except Exception as e:
            print(f"Fehler beim Scrapen von zufälligen Wörtern: {e}")
            continue

        # Warte, um den Server nicht zu überlasten
        tm.sleep(1 + rd.uniform(0, 1))

    return random_words


def translate_words_with_google(word_list, source_language: str, target_language: str):
    """Übersetzt eine Liste von Wörtern mithilfe von GoogleTranslator (deep_translator)."""
    translated_words = []

    print(f"Starte die Übersetzung ins {target_language}...")

    for entry in word_list:
        word = entry["word"]
        word_type = entry["type"]
        try:
            # Übersetze das Wort mit deep_translator.GoogleTranslator
            translated_word = GoogleTranslator(
                source=source_language, target=target_language
            ).translate(word)
            print(f"Übersetzt '{word}' ({word_type}) zu '{translated_word}'")
            translated_words.append(
                {
                    "Word_1": word,
                    "Part_1": word_type,
                    "Word_2": translated_word,
                    "Part_2": word_type,  # Wortart bleibt gleich
                }
            )

        except Exception as e:
            print(
                f"Fehler bei der Übersetzung von '{word}' und/oder seinen Art {word_type}: {e}"
            )
            continue

        # Warte einige Zeit, um keine Überlastung zu erzeugen
        tm.sleep(0.5)

    return translated_words


def save_word_pairs(word_pairs, filename="word_pairs.json"):
    """Speichert die Wortpaare als JSON-Datei."""
    import json

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(word_pairs, f, indent=4, ensure_ascii=False)

    print(f"Wortpaare wurden in '{filename}' gespeichert.")


def main():
    # Spracheinstellungen
    source_language = "de"  # Quellsprache
    target_language = "ru"  # Zielsprache
    word_count = 20  # Anzahl der Wörter, die gesammelt werden sollen

    # 1. Zufällige Wörter und ihre Wortarten scrapen
    random_words = get_random_words_from_wiktionary(source_language, word_count)

    # 2. Übersetzungen der Wörter durchführen
    translated_pairs = translate_words_with_google(
        random_words, source_language, target_language
    )

    # 3. Ergebnisse speichern
    save_word_pairs(translated_pairs)

    print("\nFertig! Zufällige Wörter wurden verarbeitet und gespeichert.")


if __name__ == "__main__":
    main()

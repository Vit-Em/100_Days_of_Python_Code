# Flash_Cards_main_v5.py
from modules import gui, data_handler as dh


def main():
    """Daten laden"""
    data = dh.load_data()

    """ GUI erstellen und starten, Funktion zum Abrufen von API-Daten übergeben"""
    app = gui.FlashcardApp(data, dh.fetch_api_word_pairs)

    app.run()


if __name__ == "__main__":
    main()

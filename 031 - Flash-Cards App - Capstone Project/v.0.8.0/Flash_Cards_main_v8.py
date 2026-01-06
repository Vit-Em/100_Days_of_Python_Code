# Flash_Cards_main_v8.py
from modules import gui


def main():
    """GUI erstellen und starten."""
    app = gui.FlashcardApp()
    app.run()


if __name__ == "__main__":
    main()
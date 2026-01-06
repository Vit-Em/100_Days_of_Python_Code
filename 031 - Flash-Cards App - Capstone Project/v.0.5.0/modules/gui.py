# modules/gui_v3.py as gui.py
import time, os, webbrowser, threading, pandas as pd, tkinter as tk
from . import card_logic, statistics

BACKGROUND_COLOR = "#B1DDC6"
FRONTSIDE_COLOR = "#FFFFFF"
BACKSIDE_COLOR = "#91c2af"
FRONTSIDE_TITLE = "Word_1"
FRONTSIDE_PROP = "Part_1"
BACKSIDE_TITLE = "Word_2"
BACKSIDE_PROP = "Part_2"


class FlashcardApp:
    def __init__(
        self,
        data,
        fetch_api_word_pairs_func=None,
        source_language="de",
        target_language="ru",
    ):
        self.data = data
        self.fetch_api_word_pairs_func = fetch_api_word_pairs_func
        self.source_language = source_language
        self.target_language = target_language
        self.card_side = "front"
        self.window = tk.Tk()
        self.window.title("Flashcards")
        self.window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

        # Add dictionary selection checkboxes
        self.dictionary_frame = tk.Frame(self.window, bg=BACKGROUND_COLOR)
        self.dictionary_frame.grid(row=0, column=0, columnspan=5, pady=10)

        self.dictionary_label = tk.Label(
            self.dictionary_frame,
            text="Флэш-карточки Русский и",
            font=("Arial", 12),
            bg=BACKGROUND_COLOR,
        )
        self.dictionary_label.pack(side=tk.LEFT, padx=10)

        self.deutsch_var = tk.BooleanVar(value=True)  # Default checked
        self.deutsch_check = tk.Checkbutton(
            self.dictionary_frame,
            text="Deutsch, 5k Wörter",
            variable=self.deutsch_var,
            font=("Arial", 12),
            bg=BACKGROUND_COLOR,
            activebackground=BACKGROUND_COLOR,
            command=self.update_dictionaries,
        )
        self.deutsch_check.pack(side=tk.LEFT, padx=10)

        self.oxford_var = tk.BooleanVar()
        self.oxford_check = tk.Checkbutton(
            self.dictionary_frame,
            text="Oxford English 5k words",
            variable=self.oxford_var,
            font=("Arial", 12),
            bg=BACKGROUND_COLOR,
            activebackground=BACKGROUND_COLOR,
            command=self.update_dictionaries,
        )
        self.oxford_check.pack(side=tk.LEFT, padx=10)

        self.american_var = tk.BooleanVar()
        self.american_check = tk.Checkbutton(
            self.dictionary_frame,
            text="American English 150k words",
            variable=self.american_var,
            font=("Arial", 12),
            bg=BACKGROUND_COLOR,
            activebackground=BACKGROUND_COLOR,
            command=self.update_dictionaries,
        )
        self.american_check.pack(side=tk.LEFT, padx=10)

        # Rest of the GUI setup
        self.canvas = tk.Canvas(
            width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0
        )
        self.card_front_img = tk.PhotoImage(file="images/card_front.png")
        self.card_back_img = tk.PhotoImage(file="images/card_back.png")
        self.canvas.create_image(400, 263, image=self.card_front_img)
        self.canvas.grid(row=1, column=0, columnspan=5)

        # Help label
        self.help_label = tk.Label(
            self.window,
            text="Hilfe / Help / Справка",
            font=("Arial", 12),
            fg="#246484",
            cursor="hand2",
        )
        self.help_label.grid(row=1, column=2, sticky="n")
        self.help_label.bind("<Button-1>", self.open_help)
        self.help_label.bind("<Enter>", self.on_enter)
        self.help_label.bind("<Leave>", self.on_leave)

        self.current_card = card_logic.weighted_choice(self.data)
        self.click_times = []
        self.start_time = 0
        self.display_card()
        self.unknown_count = 0
        self.unknown_label = tk.Label(
            self.window,
            text=f"{self.unknown_count}",
            font=("Arial", 24),
            bg=BACKGROUND_COLOR,
        )
        self.unknown_label.grid(row=3, column=0)
        self.cross_image = tk.PhotoImage(file="images/wrong.png")
        self.unknown_button = tk.Button(
            image=self.cross_image, highlightthickness=0, command=self.mark_unknown
        )
        self.unknown_button.grid(row=3, column=1, padx=20)
        self.timer_label = tk.Label(
            self.window, text="00.0", font=("Arial", 24), bg=BACKGROUND_COLOR
        )
        self.timer_label.grid(row=3, column=2)
        self.check_image = tk.PhotoImage(file="images/right.png")
        self.known_button = tk.Button(
            image=self.check_image, highlightthickness=0, command=self.mark_known
        )
        self.known_button.grid(row=3, column=3, padx=20)
        self.known_count = 0
        self.known_label = tk.Label(
            self.window,
            text=f"{self.known_count}",
            font=("Arial", 24),
            bg=BACKGROUND_COLOR,
        )
        self.known_label.grid(row=3, column=4)
        self.start_timer()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Starte den Thread zum Laden von API-Daten
        if self.fetch_api_word_pairs_func:
            self.load_api_data()

    def update_dictionaries(self):
        """
        Updates the selected dictionaries based on checkbox states.
        """
        selected_dictionaries = []
        if self.deutsch_var.get():
            selected_dictionaries.append("data/Words_deu-rus_v1.csv")
        if self.oxford_var.get():
            selected_dictionaries.append("data/5k_Oxford_eng_words.csv")
        if self.american_var.get():
            selected_dictionaries.append("data/150k_ANC_eng_words_couted.csv")

        # Load the selected dictionaries
        self.data = self.load_selected_dictionaries(selected_dictionaries)

        # Update the help label text based on the selected dictionaries
        if self.deutsch_var.get():
            self.help_label.config(text="Hilfe / Справка")
        else:
            self.help_label.config(text="Help / Справка")

        self.next_card()

    def load_selected_dictionaries(self, file_paths):
        """
        Loads data from the selected dictionaries and adds a 'source' field.
        """
        data = []
        for file_path in file_paths:
            try:
                df = pd.read_csv(file_path)
                if "Weight" not in df.columns:
                    df["Weight"] = 1.0

                # Add a 'source' field to indicate the dictionary
                if "deu-rus" in file_path:
                    df["source"] = "deutsch"
                elif "Oxford" in file_path or "ANC" in file_path:
                    df["source"] = "english"

                data.extend(df.to_dict(orient="records"))
            except FileNotFoundError:
                print(f"Die Datei {file_path} wurde nicht gefunden.")
        return data

    def load_data(self):
        """Lädt die Daten und validiert das Feld 'Weight'."""
        try:
            file_path = "data/Words_deu-rus_v1.csv"
            data = pd.read_csv(file_path)

            # Sicherstellen, dass die Gewicht-Spalte immer vorhanden ist
            if "Weight" not in data.columns:
                data["Weight"] = None  # Initialisierung mit leeren Gewichten

            # Validierung der Gewichtsspalte: Alle leer/nicht-numerischen Werte auf Standardgewicht 1.0 setzen
            data["Weight"] = data["Weight"].apply(
                lambda x: float(x) if pd.notna(x) and str(x).isdigit() else 1.0
            )

            # Konvertieren in eine Liste von Dictionaries
            return data.to_dict(orient="records")

        except FileNotFoundError:
            print(f"Die Datei {file_path} wurde nicht gefunden.")
            return []

    def load_api_data(self):
        """Startet das Laden von API-Daten im Hintergrund."""
        threading.Thread(target=self._load_api_data_threaded, daemon=True).start()

    def _load_api_data_threaded(self):
        """Lädt Daten von der API."""
        try:
            words = ["Apfel", "Haus"]
            api_data = []
            if self.fetch_api_word_pairs_func:
                for word in words:
                    data = self.fetch_api_word_pairs_func(
                        word, self.source_language, self.target_language
                    )
                    if data:
                        api_data.extend(data)

            # Aktualisierung der GUI-Daten im Haupt-Thread
            self.window.after(0, self.update_data, api_data)
        except Exception as e:
            print(f"Fehler API-Abruf: {e}")

    def update_data(self, api_data):
        """Fügt die neuen Daten hinzu."""
        for entry in api_data:
            if "Weight" not in entry:
                entry["Weight"] = 1.0
        self.data.extend(api_data)
        print("Daten hinzugefügt.")
        self.next_card()

    def open_help(self, event=None):
        """Öffnet die Hilfedatei im Standardbrowser."""
        try:
            # Absoluten Pfad zur Hilfedatei ermitteln (relativ zum Hauptverzeichnis)
            base_dir = os.path.dirname(
                os.path.dirname(__file__)
            )  # Gehe zwei Ebenen hoch
            help_file_path = os.path.join(base_dir, "help", "FlashcardsHilfe.html")

            # Prüfen, ob die Datei existiert
            if not os.path.exists(help_file_path):
                raise FileNotFoundError(
                    f"Die Hilfedatei '{help_file_path}' wurde nicht gefunden."
                )

            # Datei im Standardbrowser öffnen
            webbrowser.open(f"file://{os.path.abspath(help_file_path)}")

        except FileNotFoundError as e:
            from tkinter import messagebox

            messagebox.showerror("Fehler", str(e))
        except Exception as e:
            from tkinter import messagebox

            messagebox.showerror(
                "Fehler", f"Ein unerwarteter Fehler ist aufgetreten:\n{e}"
            )

    def on_enter(self, event):
        self.help_label.config(fg="red")  # oder eine andere Farbe

    def on_leave(self, event):
        self.help_label.config(fg="#246484")  # Originalfarbe

    def display_card(self):
        if self.card_side == "front":
            self.canvas.delete("all")
            self.canvas.create_image(400, 263, image=self.card_front_img)

            # Set the front flashcard title based on the source
            source = self.current_card.get("source", "deutsch")  # Default to "Deutsch"
            title = "Deutsch" if source == "deutsch" else "English"
            self.canvas.create_text(400, 120, text=title, font=("Arial", 24))

            # Zugriff auf das neue Feld 'Part_1' (zuvor 'Wortart de')
            front_property = self.current_card.get(FRONTSIDE_PROP, "Unbekannt")
            self.canvas.create_text(400, 150, text=front_property, font=("Arial", 18))

            self.canvas.create_text(
                400,
                263,
                text=self.current_card[FRONTSIDE_TITLE],
                font=("Arial", 60, "bold"),
            )
            self.help_label.config(bg=FRONTSIDE_COLOR)
            self.start_time = time.perf_counter()
        else:
            self.canvas.delete("all")
            self.canvas.create_image(400, 263, image=self.card_back_img)
            self.canvas.create_text(400, 120, text="Русский", font=("Arial", 24))

            # Zugriff auf das neue Feld 'Part_2' (zuvor 'Часть речи')
            back_property = self.current_card.get(BACKSIDE_PROP, "Неизвестно")
            self.canvas.create_text(400, 150, text=back_property, font=("Arial", 18))

            self.canvas.create_text(
                400,
                230,
                text=self.current_card[BACKSIDE_TITLE],
                font=("Arial", 60, "bold"),
            )
            self.help_label.config(bg=BACKSIDE_COLOR)

    def next_card(self):
        try:
            self.current_card = card_logic.weighted_choice(self.data)
            self.card_side = "front"
            self.display_card()
            self.start_timer()
        except Exception as e:
            print(f"Fehler beim Lesen der nächsten Karte: {e}")

    def mark_unknown(self):
        if self.card_side == "front":
            self.card_side = "back"
            self.display_card()
        else:
            self.unknown_count += 1
            self.unknown_label.config(text=f"{self.unknown_count}")
            self.next_card()

    def mark_known(self):
        click_time = time.perf_counter()
        reaction_time = click_time - self.start_time
        self.click_times.append(reaction_time)
        self.known_count += 1
        self.known_label.config(text=f"{self.known_count}")
        self.next_card()

    def start_timer(self):
        self.timer_value = 0.1
        self.update_timer()

    def update_timer(self):
        if self.timer_value > 0:
            self.timer_label.config(text=f"{self.timer_value:.1f}")
            self.timer_value += 0.1
            self.window.after(100, self.update_timer)
        else:
            self.timer_label.config(text="00.0")

    def on_closing(self):
        statistics.save_statistics(
            self.click_times, self.known_count, self.unknown_count
        )
        self.window.destroy()

    def run(self):
        try:
            self.window.mainloop()
        except Exception as e:
            print(f"Unerwarteter Fehler: {e}")

# modules/tests_gui.py
"""

Main Flashcard Application GUI.
Uses modular components following DRY and SOLID principles.
"""

import os
import webbrowser
import threading
import tkinter as tk
from . import card_logic, statistics
from .flashcard_config import UIConfig, DictionaryConfig, DisplayConfig, APIConfig, ProgressiveLoadingConfig, resource_path
from .flashcard_text_renderer import TextRenderer
from .flashcard_dictionary_manager import DictionaryManager
from .flashcard_checkbox_factory import CheckboxFactory
from .flashcard_card_display import CardDisplay
from .flashcard_timer_manager import TimerManager
from .tracing import tracer





class FlashcardApp:
    """Main flashcard application class using modular components."""

    def __init__(self, data=None, fetch_api_word_pairs_func=None, source_language=None, target_language=None):
        # Initialize configurations
        self.ui_config = UIConfig()
        self.dict_config = DictionaryConfig()
        self.display_config = DisplayConfig()
        self.api_config = APIConfig()
        self.loading_config = ProgressiveLoadingConfig()

        # Initialize components
        self.text_renderer = TextRenderer()
        self.dictionary_manager = DictionaryManager(
            config=self.dict_config,
            loading_config=self.loading_config
        )
        self.checkbox_factory = CheckboxFactory()
        self.timer_manager = TimerManager()

        # Application state
        self.data = data or []
        self.fetch_api_word_pairs_func = fetch_api_word_pairs_func
        self.source_language = source_language or self.api_config.DEFAULT_SOURCE_LANGUAGE
        self.target_language = target_language or self.api_config.DEFAULT_TARGET_LANGUAGE
        self.card_side = "front"
        self.unknown_count = 0
        self.known_count = 0
        self.click_times = []
        self.current_card = None

        # Initialize GUI
        self._setup_window()
        self._setup_components()
        self._setup_ui()

        # Explicitly call update_dictionaries to load the default data
        self.update_dictionaries()

    def _setup_window(self):
        """Initialize the main window."""
        self.window = tk.Tk()
        self.window.title(self.ui_config.WINDOW_TITLE)
        self.window.config(
            padx=self.ui_config.WINDOW_PADX,
            pady=self.ui_config.WINDOW_PADY,
            bg=self.ui_config.BACKGROUND_COLOR
        )

        # Set program icon
        try:
            icon_path = resource_path(os.path.join("images", self.dict_config.PROGRAM_ICON))
            self.window.iconphoto(False, tk.PhotoImage(file=icon_path))
        except tk.TclError:
            print(f"Warning: Could not load program icon {icon_path}")

        # Forbid window reshaping
        self.window.resizable(False, False)

        # Set close handler
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _setup_components(self):
        """Initialize UI components."""
        # Dictionary selection frame
        self.dictionary_frame = tk.Frame(self.window, bg=self.ui_config.BACKGROUND_COLOR)
        self.dictionary_frame.grid(
            row=self.display_config.DICTIONARY_ROW,
            column=0,
            columnspan=5,
            pady=10
        )

        # Canvas for flashcard display
        self.canvas = tk.Canvas(
            width=self.ui_config.CANVAS_WIDTH,
            height=self.ui_config.CANVAS_HEIGHT,
            bg=self.ui_config.BACKGROUND_COLOR,
            highlightthickness=0
        )
        self.canvas.grid(row=self.display_config.CANVAS_ROW, column=0, columnspan=5)

        # Initialize card display component
        self.card_display = CardDisplay(self.canvas, self.text_renderer)

        # Help label
        self.help_label = tk.Label(
            self.window,
            text=self.display_config.HELP_LABELS["german"],
            font=(self.ui_config.FONT_FAMILY, 12),
            fg=self.ui_config.HELP_LINK_COLOR,
            cursor="hand2",
        )
        self.help_label.grid(row=self.display_config.CANVAS_ROW, column=self.display_config.HELP_COLUMN, sticky="n")
        self.help_label.bind("<Button-1>", self.open_help)
        self.help_label.bind("<Enter>", self.on_enter)
        self.help_label.bind("<Leave>", self.on_leave)

        # Statistics labels and buttons
        self._setup_statistics_ui()

    def _setup_statistics_ui(self):
        """Setup statistics display and control buttons."""
        # Unknown count
        self.unknown_label = tk.Label(
            self.window,
            text=f"{self.unknown_count}",
            font=(self.ui_config.FONT_FAMILY, 24),
            bg=self.ui_config.BACKGROUND_COLOR,
        )
        self.unknown_label.grid(row=self.display_config.STATS_ROW, column=0)

        # Unknown button
        self.cross_image = tk.PhotoImage(file=resource_path(os.path.join("images", "wrong.png")))
        self.unknown_button = tk.Button(
            image=self.cross_image,
            highlightthickness=0,
            command=self.mark_unknown
        )
        self.unknown_button.grid(row=self.display_config.STATS_ROW, column=1, padx=self.ui_config.BUTTON_PADX)

        # Timer
        self.timer_label = tk.Label(
            self.window,
            text=self.ui_config.TIMER_DEFAULT_DISPLAY,
            font=(self.ui_config.FONT_FAMILY, 24),
            bg=self.ui_config.BACKGROUND_COLOR
        )
        self.timer_label.grid(row=self.display_config.STATS_ROW, column=2)

        # Setup timer manager
        self.timer_manager.set_timer_label(self.timer_label)
        self.timer_manager.set_window(self.window)

        # Known button
        self.check_image = tk.PhotoImage(file=resource_path(os.path.join("images", "right.png")))
        self.known_button = tk.Button(
            image=self.check_image,
            highlightthickness=0,
            command=self.mark_known
        )
        self.known_button.grid(row=self.display_config.STATS_ROW, column=3, padx=self.ui_config.BUTTON_PADX)

        # Known count
        self.known_label = tk.Label(
            self.window,
            text=f"{self.known_count}",
            font=(self.ui_config.FONT_FAMILY, 24),
            bg=self.ui_config.BACKGROUND_COLOR,
        )
        self.known_label.grid(row=self.display_config.STATS_ROW, column=4)

    def _setup_ui(self):
        """Setup dictionary selection checkboxes."""
        # Create individual checkbox variables (like original)
        # FIX: Set deutsch_var to False to only load custom by default
        self.deutsch_var = tk.BooleanVar(value=self.dict_config.DICTIONARIES["deutsch"]["default_checked"])
        self.oxford_var = tk.BooleanVar(value=self.dict_config.DICTIONARIES["oxford"]["default_checked"])
        self.american_var = tk.BooleanVar(value=self.dict_config.DICTIONARIES["american"]["default_checked"])
        self.custom_var = tk.BooleanVar(value=self.dict_config.DICTIONARIES["custom"]["default_checked"])

        # Load icons
        self.deu_rus_icon = tk.PhotoImage(file=resource_path(os.path.join("images", self.dict_config.DICTIONARIES["deutsch"]["icon"])))
        self.eng_rus_icon = tk.PhotoImage(file=resource_path(os.path.join("images", self.dict_config.DICTIONARIES["oxford"]["icon"])))
        self.usa_rus_icon = tk.PhotoImage(file=resource_path(os.path.join("images", self.dict_config.DICTIONARIES["american"]["icon"])))
        self.law_icon = tk.PhotoImage(file=resource_path(os.path.join("images", self.dict_config.DICTIONARIES["custom"]["icon"])))

        # Create checkboxes directly (like original)
        self.deutsch_check = tk.Checkbutton(
            self.dictionary_frame,
            text=self.dict_config.DICTIONARIES["deutsch"]["text"],
            image=self.deu_rus_icon,
            compound=tk.LEFT,
            variable=self.deutsch_var,
            font=(self.ui_config.FONT_FAMILY, 12),
            bg=self.ui_config.BACKGROUND_COLOR,
            activebackground=self.ui_config.BACKGROUND_COLOR,
            command=self.update_dictionaries,
        )
        self.deutsch_check.pack(side=tk.LEFT, padx=10)

        self.oxford_check = tk.Checkbutton(
            self.dictionary_frame,
            text=self.dict_config.DICTIONARIES["oxford"]["text"],
            image=self.eng_rus_icon,
            compound=tk.LEFT,
            variable=self.oxford_var,
            font=(self.ui_config.FONT_FAMILY, 12),
            bg=self.ui_config.BACKGROUND_COLOR,
            activebackground=self.ui_config.BACKGROUND_COLOR,
            command=self.update_dictionaries,
        )
        self.oxford_check.pack(side=tk.LEFT, padx=10)

        self.american_check = tk.Checkbutton(
            self.dictionary_frame,
            text=self.dict_config.DICTIONARIES["american"]["text"],
            image=self.usa_rus_icon,
            compound=tk.LEFT,
            variable=self.american_var,
            font=(self.ui_config.FONT_FAMILY, 12),
            bg=self.ui_config.BACKGROUND_COLOR,
            activebackground=self.ui_config.BACKGROUND_COLOR,
            command=self.update_dictionaries,
        )
        self.american_check.pack(side=tk.LEFT, padx=10)

        self.custom_check = tk.Checkbutton(
            self.dictionary_frame,
            text=self.dict_config.DICTIONARIES["custom"]["text"],
            image=self.law_icon,
            compound=tk.LEFT,
            variable=self.custom_var,
            font=(self.ui_config.FONT_FAMILY, 12),
            bg=self.ui_config.BACKGROUND_COLOR,
            activebackground=self.ui_config.BACKGROUND_COLOR,
            command=self.update_dictionaries,
        )
        self.custom_check.pack(side=tk.LEFT, padx=10)

    def update_dictionaries(self):
        """Update selected dictionaries based on checkbox states."""
        # Get selected dictionary types
        selected_types = []
        if self.deutsch_var.get():
            selected_types.append("deutsch")
        if self.oxford_var.get():
            selected_types.append("oxford")
        if self.american_var.get():
            selected_types.append("american")
        if self.custom_var.get():
            selected_types.append("custom")

        # Load dictionaries using the dictionary manager
        try:
            self.data = self.dictionary_manager.load_selected_dictionaries(selected_types)
            tracer.ic({"gui_loaded_entries": len(self.data), "selected_types": selected_types})
            print(f"GUI: Loaded {len(self.data)} entries for: {selected_types}")

            # Show entry distribution
            if self.data:
                # Count entries per dictionary type
                type_counts = {}
                for entry in self.data:
                    source = entry.get('source', 'unknown')
                    type_counts[source] = type_counts.get(source, 0) + 1
                tracer.ic({"type_counts": type_counts})
                print(f"Loaded {len(self.data)} entries: {type_counts}")
        except Exception as e:
            tracer.ic({"gui_load_error": str(e)})
            print(f"Error loading dictionaries: {e}")
            return

        # Update help label based on selection
        self._update_help_label()

        # Move to next card only if we have data
        if self.data:
            self.next_card()
        else:
            self._show_no_data_message()

    def _update_help_label(self):
        """Update help label text based on selected dictionaries."""
        # The logic here is a bit simple, but assumes German (Deutsch) or Custom (which
        # could be German-based) are the main ones that trigger the German help text.
        if self.deutsch_var.get() or self.custom_var.get():
            help_text = self.display_config.HELP_LABELS["german"]
        else:
            help_text = self.display_config.HELP_LABELS["english"]

        self.help_label.config(text=help_text)

    def _show_no_data_message(self):
        """Show message when no dictionaries are selected."""
        self.canvas.delete("all")
        self.canvas.create_text(
            self.ui_config.CARD_CENTER_X,
            self.ui_config.CARD_CENTER_Y,
            text=self.ui_config.NO_DATA_MESSAGE,
            font=(self.ui_config.FONT_FAMILY, 24),
            fill="red"
        )

    def _standardize_card_keys(self, card):
        """Standardize dictionary-specific column names to generic display keys."""
        if not card:
            return card

        # FIX: Map custom CSV keys (Word_1, Part_1, etc.) to generic keys
        # that the CardDisplay component is likely expecting (e.g., 'Front_Word').

        # Front of card (Main Word / Part of Speech)
        card['Front_Word'] = card.get('Word_1', card.get('Word', ''))
        card['Front_Part'] = card.get('Part_1', card.get('Part_of_Speech', ''))

        # Back of card (Translation / Definition)
        card['Back_Word'] = card.get('Word_2', card.get('Meaning', ''))
        card['Back_Part'] = card.get('Part_2', card.get('Category', ''))

        return card

    def display_card(self):
        """Display the current card based on the current side."""
        if not self.current_card:
            self._show_no_data_message()
            return
        if self.card_side == "front":
            self.card_display.show_front(self.current_card)
            self.help_label.config(bg=self.ui_config.FRONTSIDE_COLOR)
        else:
            self.card_display.show_back(self.current_card)
            self.help_label.config(bg=self.ui_config.BACKSIDE_COLOR)

    def next_card(self):
        """Move to the next card."""
        try:
            self.current_card = card_logic.weighted_choice(self.data)

            if self.current_card:
                # FIX: Standardize the keys before display
                self.current_card = self._standardize_card_keys(self.current_card)

                # The tracer line confirms Word_1 is being accessed successfully
                tracer.ic({
                    "next_card": {
                        "word_1_csv_key": self.current_card.get('Word_1'),
                        "front_word_standard": self.current_card.get('Front_Word'),
                        "source": self.current_card.get('source')
                    }
                })

                self.card_side = "front"
                self.display_card()
                self.timer_manager.start_timer()  # Start the timer for the new card
            else:
                self._show_no_data_message()
        except Exception as e:
            tracer.ic({"next_card_error": str(e)})
            raise

    def mark_unknown(self):
        """Mark current card as unknown and show back side."""
        if not self.current_card:
            self._show_no_data_message()
            return

        # Stop timer and record reaction time
        reaction_time = self.timer_manager.stop_timer()
        self.click_times.append(reaction_time)

        # Update statistics
        self.unknown_count += 1
        self.unknown_label.config(text=f"{self.unknown_count}")

        self.card_side = "back"
        self.display_card()

    def mark_known(self):
        """Mark current card as known and go to next."""
        if not self.current_card:
            self._show_no_data_message()
            return

        # Stop timer and record reaction time
        reaction_time = self.timer_manager.stop_timer()
        self.click_times.append(reaction_time)

        # Update statistics
        self.known_count += 1
        self.known_label.config(text=f"{self.known_count}")

        self.next_card()

    def open_help(self, event=None):
        """Open help file in default browser."""
        try:
            # Changed to use external_path for help files
            from .flashcard_config import external_path
            help_file_path = external_path(os.path.join("help", self.dict_config.HELP_FILE))

            if not os.path.exists(help_file_path):
                raise FileNotFoundError(f"Help file not found: {help_file_path}")

            webbrowser.open(f"file://{os.path.abspath(help_file_path)}")

        except FileNotFoundError as e:
            tk.messagebox.showerror("Error", str(e))
        except Exception as e:
            tk.messagebox.showerror("Error", f"Unexpected error: {e}")

    def on_enter(self, event):
        """Handle mouse enter on help label."""
        self.help_label.config(fg=self.ui_config.HELP_HOVER_COLOR)

    def on_leave(self, event):
        """Handle mouse leave on help label."""
        self.help_label.config(fg=self.ui_config.HELP_LINK_COLOR)

    def _load_api_data(self):
        """Start loading API data in background thread."""
        threading.Thread(target=self._load_api_data_threaded, daemon=self.api_config.DAEMON_THREAD).start()

    def _load_api_data_threaded(self):
        """Load API data in background thread."""
        try:
            api_data = []
            if self.fetch_api_word_pairs_func:
                for word in self.api_config.API_WORDS:
                    data = self.fetch_api_word_pairs_func(
                        word, self.source_language, self.target_language
                    )
                    if data:
                        api_data.extend(data)

            # Update GUI data in main thread
            self.window.after(0, self._update_data, api_data)
        except Exception as e:
            print(f"API loading error: {e}")

    def _update_data(self, api_data):
        """Add new API data to application data."""
        for entry in api_data:
            if self.dict_config.WEIGHT_COLUMN not in entry:
                entry[self.dict_config.WEIGHT_COLUMN] = self.dict_config.DEFAULT_WEIGHT
        self.data.extend(api_data)
        print("API data added.")
        # Don't call next_card() automatically - let user control the flow

    def on_closing(self):
        """Handle application closing."""
        # Save statistics before closing
        try:
            statistics.save_statistics(self.click_times, self.known_count, self.unknown_count)
        except Exception as e:
            print(f"Error saving statistics: {e}")
        
        # Stop progressive loading
        try:
            self.dictionary_manager.stop_progressive_loading()
            self.dictionary_manager.cleanup()
        except Exception as e:
            print(f"Error cleaning up progressive loading: {e}")
        
        # Close the window
        self.window.destroy()

    def run(self):
        """Start the application main loop."""
        try:
            self.window.mainloop()
        except Exception as e:
            print(f"Unexpected error: {e}")
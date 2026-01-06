# modules/tests_config.py
"""
Configuration constants for the Flashcard Application.
Centralizes all magic numbers, colors, dimensions, and file paths.
This module uses a single-instance pattern - all classes are accessed directly without instantiation.


USAGE INSTRUCTIONS
All config classes use the singleton pattern - access attributes directly:
✅ CORRECT:
from modules.flashcard_config import UIConfig
width = UIConfig.CANVAS_WIDTH
frame = UIConfig.TEXT_FRAME_FRONT
This ensures all modules share the EXACT SAME configuration values.
"""
import os
import sys

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def external_path(relative_path):
    """Get path for external folders (data, help) next to EXE."""
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# UI Configuration
class UIConfig:
    """UI configuration settings - use class attributes directly (singleton pattern)."""

    # Window and Canvas Dimensions
    CANVAS_WIDTH = 800
    CANVAS_HEIGHT = 526
    CARD_CENTER_X = 400
    CARD_CENTER_Y = 263

    # Text Rendering
    MAX_TEXT_WIDTH = 600
    BASE_FONT_SIZE = 40  # Increased base for more granular scaling
    TITLE_FONT_SIZE = 20
    PROPERTY_FONT_SIZE = 16
    LINE_HEIGHT_OFFSET = 6  # Optimized for card alignment

    # Card Layout Positions
    TITLE_Y = 35
    SUBTITLE_Y = 65

    # Bounding box for text rendering (x_center, y_center, width, height)
    # IMPORTANT: This is the SINGLE SOURCE OF TRUTH for text frame dimensions
    # Used by both preprocessing and rendering to ensure consistency
    TEXT_FRAME_BACK = TEXT_FRAME_FRONT = (400, 270, 700, 400)

    # Colors
    BACKGROUND_COLOR = "#B1DDC6"
    FRONTSIDE_COLOR = "#FFFFFF"
    BACKSIDE_COLOR = "#91c2af"
    HELP_LINK_COLOR = "#246484"
    HELP_HOVER_COLOR = "red"

    # Fonts
    FONT_FAMILY = "Arial"
    FONT_WEIGHT_BOLD = "bold"

    # Padding and Spacing
    WINDOW_PADX = 50
    WINDOW_PADY = 50
    CHECKBOX_PADX = 10
    BUTTON_PADX = 20

    # Timer Configuration
    TIMER_START_VALUE = 0.1
    TIMER_INCREMENT = 0.1
    TIMER_UPDATE_INTERVAL = 100  # milliseconds
    TIMER_DISPLAY_FORMAT = "{:.1f}"
    TIMER_DEFAULT_DISPLAY = "00.0"
    WINDOW_TITLE = "Flashcards"
    NO_DATA_MESSAGE = "Bitte mindestens ein Wörterbuch auswählen!"


# Dictionary Configuration
class DictionaryConfig:
    """Dictionary configuration settings - use class attributes directly (singleton pattern)."""

    # Base Paths
    DATA_DIR = "data/"  # Base directory for dictionary files

    # Shared translation label
    TRANSLATION = "Русский"

    DICTIONARIES = {
        "deutsch": {
            "file": os.path.join(DATA_DIR, "Words_deu-rus_v1.csv"),
            "icon": "GER-RUS_icon.png",
            "text": "5k Wörter",
            "source": "deutsch",
            "default_checked": True,
            "delimiter": "\t",
            "front_title": "Deutsch",
            "back_title": TRANSLATION
        },
        "oxford": {
            "file": os.path.join(DATA_DIR, "5k_Oxford_eng_words.csv"),
            "icon": "ENG-RUS_icon.png",
            "text": "5k words",
            "source": "english",
            "default_checked": True,
            "delimiter": "\t",
            "front_title": "English",
            "back_title": TRANSLATION
        },
        "american": {
            "file": os.path.join(DATA_DIR, "150k_ANC_eng_words_couted.csv"),
            "icon": "USA-RUS_icon.png",
            "text": "150k words",
            "source": "english",
            "default_checked": True,
            "delimiter": "\t",
            "front_title": "English (Am.)",
            "back_title": TRANSLATION
        },
        "custom": {
            "file": os.path.join(DATA_DIR, "custom_dict.csv"),
            "icon": "LAW_icon.png",
            "text": "custom dict",
            "source": "custom",
            "default_checked": True,
            "delimiter": "\t",
            "front_title": "Frage",
            "back_title": "Antwort"
        },
    }

    # File Paths
    ICONS_DIR = "images/"
    HELP_DIR = "help/"
    HELP_FILE = "FlashcardsHilfe.html"
    PROGRAM_ICON = "Program_icon.png"

    # CSV Column Names
    WEIGHT_COLUMN = "Weight"
    WORD_1_COLUMN = "Word_1"
    PART_1_COLUMN = "Part_1"
    WORD_2_COLUMN = "Word_2"
    PART_2_COLUMN = "Part_2"
    SOURCE_COLUMN = "source"

    # Default Values
    DEFAULT_WEIGHT = 1.0
    DEFAULT_PART_1 = "Unbekannt"
    DEFAULT_PART_2 = "Неизвестно"


# Text Rendering Configuration
class TextRenderConfig:
    """Text rendering configuration - use class attributes directly (singleton pattern)."""

    # Newline and space symbols
    # IMPORTANT: These symbols are used in CSV data and must be consistent
    NEW_LINE_SYMBOL = ";"  # Represents a semicolon in the CSV data
    NON_BREAKABLE_SPACE_SYMBOL = "&nbsp;"  # Represents a non-breakable space

    # Font Size Multipliers (stabilized for better learning experience)
    FONT_SIZE_MULTIPLIERS = {
        1: 1.0,      # 32px - full size for single words
        2: 0.9,      # 29px - gentle decrease for two words
        3: 0.8,      # 26px - moderate decrease for three words
        4: 0.7,      # 22px - reasonable size for four words
        5: 0.65,     # 21px - comfortable size for five words
        "default": 0.6  # 19px - stable size for longer phrases
    }

    # Text Wrapping
    MAX_LINES_FRONT = 4
    MAX_LINES_BACK = 8
    MIN_WORDS_FOR_WRAPPING = 4

    # Enhanced wrapping configuration
    MAX_PIXEL_WIDTH = 500  # Reasonable wrapping for readability
    HYPHENATION_ENABLED = True
    FALLBACK_TO_WORD_COUNT = True  # For backward compatibility

    # Language Detection
    # IMPORTANT: Used for proper hyphenation and word splitting
    GERMAN_INDICATORS = ['ä', 'ö', 'ü', 'ß', 'sch', 'tz', 'pf', 'haus', 'deutsch', 'straf', 'recht']
    ENGLISH_INDICATORS = ['th', 'sh', 'ing', 'tion', 'sion', 'programming', 'algorithm']


# Display Configuration
class DisplayConfig:
    """Display configuration - use class attributes directly (singleton pattern)."""

    # Help Labels
    HELP_LABELS = {
        "german": "Hilfe / Справка",
        "english": "Help / Справка"
    }

    # Grid Positions
    DICTIONARY_ROW = 0
    CANVAS_ROW = 1
    STATS_ROW = 3
    HELP_COLUMN = 2


# API Configuration
class APIConfig:
    """API configuration - use class attributes directly (singleton pattern)."""

    # API Data Loading
    API_WORDS = ["Apfel", "Haus"]
    DEFAULT_SOURCE_LANGUAGE = "de"
    DEFAULT_TARGET_LANGUAGE = "ru"
    WORD_COUNT = 20
    WORD_PAIRS_FILENAME = "word_pairs.json"

    # Threading
    DAEMON_THREAD = True


# Progressive Loading Configuration
class ProgressiveLoadingConfig:
    """Progressive loading configuration - use class attributes directly (singleton pattern)."""

    # Batch Loading Settings
    BATCH_SIZE = 1000  # Number of entries to load per batch
    LOADING_INTERVAL = 180  # Seconds between progressive loads
    MAX_LOADED_ENTRIES = 10000  # Maximum entries per dictionary in memory

    # Performance Settings
    ENABLE_PROGRESSIVE_LOADING = True  # Master switch for progressive loading
    BACKGROUND_LOADING = True  # Load in background thread
    CACHE_LOADED_RANGES = True  # Track loaded ranges to avoid duplicates


# Statistics Configuration
class StatisticsConfig:
    """Statistics configuration - use class attributes directly (singleton pattern)."""

    # File Paths
    STATS_FILE = "statistics.csv"

    # Data Fields
    STATS_COLUMNS = [
        "Datum", "Zeit", "Übungsdauer", "Richtig", "Falsch",
        "Durchschnittliche Reaktionszeit"
    ]
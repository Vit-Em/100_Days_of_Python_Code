# modules/__init__.py
# This file initializes the 'modules' package and provides a clear API for accessing its components.

# Importing key classes and functions from each module
from .gui import FlashcardApp
from .statistics import save_statistics
from .data_handler import load_data, fetch_api_word_pairs
from .card_logic import weighted_choice

# Define the public interface of the package for cleaner imports
__all__ = [
    "FlashcardApp",
    "save_statistics",
    "load_data",
    "fetch_api_word_pairs",
    "weighted_choice",
]

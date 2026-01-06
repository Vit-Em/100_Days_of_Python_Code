"""
Card display component for rendering flashcard front and back sides.
Separates card rendering logic from main GUI class.
"""

import tkinter as tk
import os
import sys
from .flashcard_config import UIConfig, DictionaryConfig


def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class CardDisplay:
    """Handles flashcard rendering for front and back sides."""

    def __init__(self, canvas, text_renderer, ui_config=None, dict_config=None):
        self.canvas = canvas
        self.text_renderer = text_renderer
        self.ui_config = ui_config or UIConfig()
        self.dict_config = dict_config or DictionaryConfig()

        self.card_front_img = tk.PhotoImage(file=resource_path(os.path.join("images", "card_front.png")))
        self.card_back_img = tk.PhotoImage(file=resource_path(os.path.join("images", "card_back.png")))

    def _parse_render_constants(self, constants_str):
        """Parses the render constants string into a tuple of integers."""
        try:
            parts = str(constants_str).split(',')
            if len(parts) == 3:
                return tuple(int(p) for p in parts)
        except (ValueError, TypeError):
            pass
        # Return a safe fallback tuple if parsing fails
        return (12, 60, 5) # font_size, chars_per_line, num_lines

    def show_front(self, card_data):
        """
        Display the front side of the flashcard.
        """
        self.canvas.delete("all")
        self.canvas.create_image(self.ui_config.CARD_CENTER_X, self.ui_config.CARD_CENTER_Y, image=self.card_front_img)

        dict_type = card_data.get(self.dict_config.SOURCE_COLUMN, "custom")
        dict_info = self.dict_config.DICTIONARIES.get(dict_type, self.dict_config.DICTIONARIES["custom"])
        title = dict_info.get("front_title", "Question")

        self.canvas.create_text(
            self.ui_config.CARD_CENTER_X, self.ui_config.TITLE_Y, text=title,
            font=(self.ui_config.FONT_FAMILY, self.ui_config.TITLE_FONT_SIZE)
        )

        part_1 = card_data.get("Front_Part", "")
        self.canvas.create_text(
            self.ui_config.CARD_CENTER_X, self.ui_config.SUBTITLE_Y, text=part_1,
            font=(self.ui_config.FONT_FAMILY, self.ui_config.PROPERTY_FONT_SIZE)
        )

        # Use pre-calculated render constants
        main_text = card_data.get("Front_Word", "")
        render_constants_str = card_data.get('Text_constants_front', '12,60,5')
        render_constants = self._parse_render_constants(render_constants_str)

        self.text_renderer.render_precalculated_text(
            self.canvas, main_text, self.ui_config.TEXT_FRAME_FRONT, render_constants
        )

    def show_back(self, card_data):
        """
        Display the back side of the flashcard.
        """
        self.canvas.delete("all")
        self.canvas.create_image(self.ui_config.CARD_CENTER_X, self.ui_config.CARD_CENTER_Y, image=self.card_back_img)

        dict_type = card_data.get(self.dict_config.SOURCE_COLUMN, "custom")
        dict_info = self.dict_config.DICTIONARIES.get(dict_type, self.dict_config.DICTIONARIES["custom"])
        title = dict_info.get("back_title", "Answer")

        self.canvas.create_text(
            self.ui_config.CARD_CENTER_X, self.ui_config.TITLE_Y, text=title,
            font=(self.ui_config.FONT_FAMILY, self.ui_config.TITLE_FONT_SIZE)
        )

        part_2 = card_data.get("Back_Part", "")
        self.canvas.create_text(
            self.ui_config.CARD_CENTER_X, self.ui_config.SUBTITLE_Y, text=part_2,
            font=(self.ui_config.FONT_FAMILY, self.ui_config.PROPERTY_FONT_SIZE)
        )

        # Use pre-calculated render constants
        main_text = card_data.get("Back_Word", "")
        render_constants_str = card_data.get('Text_constants_back', '12,60,5')
        render_constants = self._parse_render_constants(render_constants_str)

        self.text_renderer.render_precalculated_text(
            self.canvas, main_text, self.ui_config.TEXT_FRAME_BACK, render_constants
        )

    def clear(self):
        """Clear the canvas."""
        self.canvas.delete("all")
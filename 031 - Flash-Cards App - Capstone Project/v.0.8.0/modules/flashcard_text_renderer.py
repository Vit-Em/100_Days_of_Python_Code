# /modules/tests_text_renderer.py
"""
Text rendering service for the Flashcard Application.
This version uses the SAME text wrapping algorithm as preprocessing for perfect consistency.
Uses single config instance pattern.
"""

import re
from tkinter import font
from .flashcard_config import UIConfig, TextRenderConfig

# Try to import pyphen for proper German hyphenation
try:
    import pyphen
    PYPHEN_AVAILABLE = True
    HYPHEN_DE = pyphen.Pyphen(lang='de_DE')
    HYPHEN_EN = pyphen.Pyphen(lang='en_US')
except ImportError:
    PYPHEN_AVAILABLE = False
    HYPHEN_DE = None
    HYPHEN_EN = None


class TextRenderer:
    """Renders text using pre-calculated font size and the canonical wrapping algorithm."""

    def __init__(self, ui_config=None):
        # Use single config instance
        self.ui_config = ui_config or UIConfig
        self.text_config = TextRenderConfig

    def _is_german_text(self, text):
        """Detect if text is likely German based on character patterns."""
        if not isinstance(text, str):
            return False
        text_lower = text.lower()

        german_score = sum(1 for indicator in TextRenderConfig.GERMAN_INDICATORS
                           if indicator in text_lower)
        english_score = sum(1 for indicator in TextRenderConfig.ENGLISH_INDICATORS
                            if indicator in text_lower)

        return german_score > english_score

    def _can_break_at_position(self, word, i, vowels):
        """Check if we can break a German word at position i."""
        if i >= len(word) - 2:
            return False

        consonant_vowel = word[i] not in vowels and word[i+1] in vowels
        double_consonant = word[i] == word[i+1] and word[i] not in vowels

        return consonant_vowel or double_consonant

    def _add_hyphenated_part(self, result, current_part, remaining_char, max_width, font_obj):
        """Add a hyphenated part to result if it exceeds max width."""
        if len(current_part) <= 1:
            return current_part

        test_with_hyphen = current_part + "-"
        if font_obj.measure(test_with_hyphen) > max_width:
            result.append(current_part[:-1] + "-")
            return remaining_char
        return current_part

    def _split_word_with_pyphen(self, word, max_width, font_obj, hyphenator):
        """Split a word using pyphen library for proper hyphenation."""
        if not hyphenator:
            return [word]

        pairs = hyphenator.iterate(word)
        result = []
        current_part = ""

        for left, right in pairs:
            test_part = left + "-"
            if font_obj.measure(test_part) <= max_width:
                current_part = left
            else:
                if current_part:
                    result.append(current_part + "-")
                    current_part = ""
                break

        if current_part:
            result.append(current_part + "-")
            remaining = word[len(current_part):]
            if remaining:
                result.extend(self._split_word_with_pyphen(remaining, max_width, font_obj, hyphenator))
        else:
            result.append(word)

        return result if len(result) > 1 else [word]

    def _split_german_word(self, word, max_width, font_obj):
        """Split a German word according to German hyphenation rules."""
        if font_obj.measure(word) <= max_width:
            return [word]

        if PYPHEN_AVAILABLE and HYPHEN_DE:
            return self._split_word_with_pyphen(word, max_width, font_obj, HYPHEN_DE)

        vowels = 'aeiouäöüAEIOUÄÖÜ'
        result = []
        current_part = ""

        for i, char in enumerate(word):
            current_part += char
            if self._can_break_at_position(word, i, vowels):
                current_part = self._add_hyphenated_part(result, current_part, char, max_width, font_obj)

        if current_part:
            result.append(current_part)

        return result if len(result) > 1 else [word]

    def _handle_long_word(self, word, wrap_width, font_obj, is_german):
        """Handle words longer than wrap_width, splitting them according to language rules."""
        if is_german:
            return self._split_german_word(word, wrap_width, font_obj)
        else:
            avg_char_width = font_obj.measure('m') or 1
            chars_per_line = max(1, int(wrap_width / avg_char_width))
            result = []
            for i in range(0, len(word), chars_per_line):
                result.append(word[i:i + chars_per_line])
            return result

    def _handle_word_starting_with_paren(self, word, current_line, wrap_width, font_obj, final_lines):
        """Handle words starting with '(' - must stay with next word."""
        test_line = f"{current_line} {word}".strip() if current_line else word
        if font_obj.measure(test_line.replace("\u00A0", " ")) <= wrap_width:
            return test_line

        if current_line:
            final_lines.append(current_line)
        return word

    def _handle_word_with_closing_paren(self, word, current_line, wrap_width, font_obj, final_lines):
        """Handle words with ')' - cannot be split."""
        measurable_word = word.replace("\u00A0", " ")

        if font_obj.measure(measurable_word) > wrap_width:
            if current_line:
                final_lines.append(current_line)
            final_lines.append(word)
            return ""

        test_line = f"{current_line} {word}".strip() if current_line else word
        if font_obj.measure(test_line.replace("\u00A0", " ")) <= wrap_width:
            return test_line

        if current_line:
            final_lines.append(current_line)
        return word

    def _process_word_with_parentheses(self, word, current_line, wrap_width, font_obj, final_lines):
        """Handle words with parentheses according to rules."""
        if word.startswith('('):
            return self._handle_word_starting_with_paren(word, current_line, wrap_width, font_obj, final_lines)

        if ')' in word:
            return self._handle_word_with_closing_paren(word, current_line, wrap_width, font_obj, final_lines)

        return None

    def _handle_long_word_in_paragraph(self, word, current_line, wrap_width, font_obj, final_lines, is_german):
        """Handle a word that's too long to fit on one line."""
        if current_line:
            final_lines.append(current_line)

        split_parts = self._handle_long_word(word, wrap_width, font_obj, is_german)
        final_lines.extend(split_parts)
        return ""

    def _try_add_word_to_line(self, word, current_line, wrap_width, font_obj, final_lines):
        """Try to add a word to the current line, wrapping if necessary."""
        test_line = f"{current_line} {word}".strip()
        if font_obj.measure(test_line.replace("\u00A0", " ")) <= wrap_width:
            return test_line

        if current_line:
            final_lines.append(current_line)
        return word

    def _process_single_word(self, word, current_line, wrap_width, font_obj, final_lines, is_german):
        """Process a single word with all rules applied."""
        if not word:
            return current_line

        special_result = self._process_word_with_parentheses(word, current_line, wrap_width, font_obj, final_lines)
        if special_result is not None:
            return special_result

        measurable_word = word.replace("\u00A0", " ")
        if font_obj.measure(measurable_word) > wrap_width:
            return self._handle_long_word_in_paragraph(word, current_line, wrap_width, font_obj, final_lines, is_german)

        return self._try_add_word_to_line(word, current_line, wrap_width, font_obj, final_lines)

    def _process_paragraph(self, paragraph, wrap_width, font_obj, final_lines, is_german):
        """Helper to process and wrap a single paragraph with language-aware rules."""
        words = paragraph.split(' ')
        current_line = ""

        for word in words:
            current_line = self._process_single_word(word, current_line, wrap_width, font_obj, final_lines, is_german)

        if current_line:
            final_lines.append(current_line)

    def wrap_text(self, text, wrap_width, font_obj):
        """
        CANONICAL text wrapping function - IDENTICAL to preprocessing.
        Respects:
        1. Semicolon (;) as newline symbol
        2. Left brace '(' must stick to next word
        3. Words with ')' cannot be split
        4. German hyphenation rules for word splitting
        5. Non-breakable spaces
        """
        final_lines = []

        text = text.replace(TextRenderConfig.NON_BREAKABLE_SPACE_SYMBOL, "\u00A0")
        is_german = self._is_german_text(text)

        text = re.sub(r'\s*\(\s*', ' (', text)
        text = re.sub(r'\s*\)', ')', text)

        paragraphs = text.split(TextRenderConfig.NEW_LINE_SYMBOL)

        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if paragraph:
                self._process_paragraph(paragraph, wrap_width, font_obj, final_lines, is_german)

        return [line.replace("\u00A0", " ") for line in final_lines]

    def render_precalculated_text(self, canvas, text, frame_coords, render_constants):
        """
        Renders text using pre-calculated font size and the SAME wrapping algorithm.

        Args:
            canvas: The tkinter canvas to draw on.
            text: The text string to render.
            frame_coords: A tuple (x_center, y_center, width, height) defining the frame.
            render_constants: A tuple (font_size, chars_per_line, num_lines).
        """
        if not text or not isinstance(text, str):
            return

        font_size, _, _ = render_constants

        if render_constants == (12, 60, 5):
            # Fallback for dictionaries without pre-calculated font sizes
            word_count = len(text.split())
            multiplier = self.text_config.FONT_SIZE_MULTIPLIERS.get(word_count, self.text_config.FONT_SIZE_MULTIPLIERS["default"])
            font_size = int(self.ui_config.BASE_FONT_SIZE * multiplier)

        if not isinstance(font_size, (int, float)) or font_size <= 0:
            canvas.create_text(frame_coords[0], frame_coords[1],
                               text="Invalid Render Constants",
                               font=("Arial", 12), fill="red")
            return

        # Create the font object with the pre-calculated size
        font_obj = font.Font(
            family=self.ui_config.FONT_FAMILY,
            size=int(font_size),
            weight=self.ui_config.FONT_WEIGHT_BOLD
        )

        # Use the SAME wrapping algorithm as preprocessing
        frame_x, frame_y, frame_width, _ = frame_coords
        lines = self.wrap_text(text, frame_width, font_obj)

        # Calculate positioning
        line_height = font_size + self.ui_config.LINE_HEIGHT_OFFSET
        total_text_height = len(lines) * line_height
        start_y = frame_y - (total_text_height / 2) + (line_height / 2)

        # Render the final lines
        for i, line in enumerate(lines):
            line_y = start_y + (i * line_height)
            canvas.create_text(frame_x, line_y, text=line, font=font_obj, anchor="center")
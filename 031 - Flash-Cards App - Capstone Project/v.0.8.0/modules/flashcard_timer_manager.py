"""
Timer management service for the Flashcard Application.
Handles timing functionality for reaction time measurement.
"""

import time
from .flashcard_config import UIConfig


class TimerManager:
    """Manages timer functionality for reaction time measurement."""
    
    def __init__(self, ui_config=None):
        self.ui_config = ui_config or UIConfig()
        self.timer_value = 0.0
        self.start_time = 0.0
        self.timer_label = None
        self.window = None
    
    def set_timer_label(self, timer_label):
        """
        Set the timer label widget for display updates.
        
        Args:
            timer_label: Tkinter Label widget for timer display
        """
        self.timer_label = timer_label
    
    def set_window(self, window):
        """
        Set the main window for scheduling updates.
        
        Args:
            window: Tkinter root window
        """
        self.window = window
    
    def start_timer(self):
        """Start the timer for a new card."""
        self.timer_value = self.ui_config.TIMER_START_VALUE
        self.start_time = time.perf_counter()
        self.update_timer()
    
    def update_timer(self):
        """Update the timer display."""
        if self.start_time > 0 and self.timer_label and self.window:
            # Calculate actual elapsed time instead of incrementing
            elapsed = time.perf_counter() - self.start_time
            self.timer_label.config(
                text=self.ui_config.TIMER_DISPLAY_FORMAT.format(elapsed)
            )
            # Update every 100ms for smooth display
            self.window.after(self.ui_config.TIMER_UPDATE_INTERVAL, self.update_timer)
        else:
            if self.timer_label:
                self.timer_label.config(text=self.ui_config.TIMER_DEFAULT_DISPLAY)
    
    def get_reaction_time(self):
        """
        Get the current reaction time.
        
        Returns:
            Reaction time in seconds
        """
        if self.start_time > 0:
            return time.perf_counter() - self.start_time
        return 0.0
    
    def reset_timer(self):
        """Reset the timer to initial state."""
        self.timer_value = 0.0
        self.start_time = 0.0
        if self.timer_label:
            self.timer_label.config(text=self.ui_config.TIMER_DEFAULT_DISPLAY)
    
    def stop_timer(self):
        """Stop the timer and return the final reaction time."""
        reaction_time = self.get_reaction_time()
        self.reset_timer()
        return reaction_time

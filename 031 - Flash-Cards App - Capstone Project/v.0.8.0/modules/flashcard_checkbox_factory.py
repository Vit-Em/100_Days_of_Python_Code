"""
Checkbox factory for creating dictionary selection checkboxes.
Implements DRY principle for checkbox creation.
"""

import tkinter as tk
from .flashcard_config import UIConfig, DictionaryConfig


class CheckboxFactory:
    """Factory for creating standardized dictionary selection checkboxes."""
    
    def __init__(self, ui_config=None, dict_config=None):
        self.ui_config = ui_config or UIConfig()
        self.dict_config = dict_config or DictionaryConfig()
    
    def create_checkbox(self, parent, dict_type, var, command):
        """
        Create a dictionary selection checkbox.
        
        Args:
            parent: Parent widget (Frame)
            dict_type: Dictionary type name
            var: BooleanVar for checkbox state
            command: Callback function for checkbox changes
            
        Returns:
            Configured Checkbutton widget
        """
        dict_info = self.dict_config.DICTIONARIES.get(dict_type)
        if not dict_info:
            raise ValueError(f"Unknown dictionary type: {dict_type}")
        
        # Load icon
        icon_path = self.dict_config.ICONS_DIR + dict_info["icon"]
        try:
            icon = tk.PhotoImage(file=icon_path)
        except tk.TclError:
            print(f"Warning: Could not load icon {icon_path}")
            icon = None
        
        # Create checkbox
        checkbox = tk.Checkbutton(
            parent,
            text=dict_info["text"],
            image=icon,
            compound=tk.LEFT,
            variable=var,
            font=(self.ui_config.FONT_FAMILY, 12),
            bg=self.ui_config.BACKGROUND_COLOR,
            activebackground=self.ui_config.BACKGROUND_COLOR,
            command=command,
        )
        
        # Store icon reference to prevent garbage collection
        checkbox.icon = icon
        
        return checkbox
    
    def create_all_checkboxes(self, parent, checkbox_vars, command):
        """
        Create all dictionary checkboxes.
        
        Args:
            parent: Parent widget (Frame)
            checkbox_vars: Dictionary mapping dict_type to BooleanVar
            command: Callback function for checkbox changes
            
        Returns:
            Dictionary mapping dict_type to Checkbutton widget
        """
        checkboxes = {}
        
        for dict_type in self.dict_config.DICTIONARIES.keys():
            if dict_type in checkbox_vars:
                checkbox = self.create_checkbox(
                    parent, dict_type, checkbox_vars[dict_type], command
                )
                checkboxes[dict_type] = checkbox
        
        return checkboxes
    
    def pack_checkboxes(self, checkboxes, side=tk.LEFT, padx=None):
        """
        Pack all checkboxes with consistent spacing.
        
        Args:
            checkboxes: Dictionary of checkbox widgets
            side: Pack side (default: LEFT)
            padx: Horizontal padding (default from config)
        """
        padx = padx or self.ui_config.CHECKBOX_PADX
        
        for checkbox in checkboxes.values():
            checkbox.pack(side=side, padx=padx)
    
    def get_selected_types(self, checkbox_vars):
        """
        Get list of selected dictionary types.
        
        Args:
            checkbox_vars: Dictionary mapping dict_type to BooleanVar
            
        Returns:
            List of selected dictionary type names
        """
        selected_types = []
        
        for dict_type, var in checkbox_vars.items():
            if var.get():
                selected_types.append(dict_type)
        
        return selected_types
    
    def set_default_selections(self, checkbox_vars):
        """
        Set default checkbox selections based on configuration.
        
        Args:
            checkbox_vars: Dictionary mapping dict_type to BooleanVar
        """
        default_types = self.dict_config.get_default_checked_types()
        
        for dict_type, var in checkbox_vars.items():
            var.set(dict_type in default_types)

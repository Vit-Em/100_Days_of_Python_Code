# modules/tests_dictionary_manager.py
"""
Dictionary management service for the Flashcard Application.
Handles loading, combining, and managing multiple dictionary sources.
Now includes progressive loading for O(1) performance.
"""

import pandas as pd

from .flashcard_config import DictionaryConfig, ProgressiveLoadingConfig, resource_path

from .flashcard_progressive_loader import ProgressiveDictionaryManager

from .tracing import tracer



# Fix for python:S7498 - Use dictionary literal

CSV_KWARGS = {'engine': 'python', 'on_bad_lines': 'skip', 'quotechar': '"'}





class DictionaryManager:

    """Manages dictionary loading, source detection, and data combination."""

    

    def __init__(self, config=None, loading_config=None):

        self.config = config or DictionaryConfig()

        self.loading_config = loading_config or ProgressiveLoadingConfig()

        

        # Initialize progressive loading system

        self.progressive_loader = ProgressiveDictionaryManager(

            dict_config=self.config,

            loading_config=self.loading_config

        )

    

    def load_selected_dictionaries(self, selected_types):

        """

        Load data from selected dictionary types using progressive loading.

        """

        if self.loading_config.ENABLE_PROGRESSIVE_LOADING:

            tracer.ic({"loader": "progressive", "selected": selected_types})

            return self._load_with_progressive_system(selected_types)

        else:

            tracer.ic({"loader": "legacy", "selected": selected_types})

            return self._load_with_legacy_system(selected_types)

    

    def _load_with_progressive_system(self, selected_types):

        """

        Load dictionaries using the progressive loading system.

        """

        self.progressive_loader.update_active_dictionaries(selected_types)

        entries = self.progressive_loader.get_available_entries(selected_types)

        tracer.ic({"progressive_loaded": len(entries)})

        return entries



    def _load_with_legacy_system(self, selected_types):
        """
        Load dictionaries using the legacy full-loading system.
        """
        data = []
        for dict_type in selected_types:
            if dict_type not in self.config.DICTIONARIES:
                continue

            dict_info = self.config.DICTIONARIES[dict_type]
            file_path = resource_path(dict_info["file"])
            
            try:
                df = pd.read_csv(
                    file_path,
                    nrows=1000 if dict_type == "american" else None,
                    sep=dict_info.get("delimiter", "\t"),
                    **CSV_KWARGS
                )
                if dict_type == "american":
                    # Fix for python:S3457 - Use normal string
                    print("Loaded 1,000 entries from American dictionary for performance")

                required_columns = [self.config.WORD_1_COLUMN, self.config.WORD_2_COLUMN]
                if not all(col in df.columns for col in required_columns):
                    # Fix for python:S3457 - Use normal string
                    print("--- PARSING ERROR ---")
                    print(f"File: {file_path}")
                    print(f"Could not find expected columns. The delimiter '{dict_info.get("delimiter", "\t")}' might be incorrect.")
                    print(f"Found columns: {df.columns.tolist()}")
                    # Fix for python:S3457 - Use normal string
                    print("-----------------------")
                    continue

                tracer.ic({"legacy_loaded": {"dict": dict_type, "rows": len(df)}})
                
                if self.config.WEIGHT_COLUMN not in df.columns:
                    df[self.config.WEIGHT_COLUMN] = self.config.DEFAULT_WEIGHT
                
                df[self.config.SOURCE_COLUMN] = dict_info["source"]
                
                data.extend(df.to_dict(orient="records"))
                
            except FileNotFoundError:
                print(f"File not found: {file_path}")
            except pd.errors.ParserError as e:
                # Fix for python:S3457 - Use normal string
                print("--- PANDAS PARSING ERROR ---")
                print(f"File: {file_path}")
                print(f"Pandas could not parse the file. It may be corrupted. Error: {e}")
                # Fix for python:S3457 - Use normal string
                print("----------------------------")
            except Exception as e:
                tracer.ic({"legacy_error": str(e), "file": file_path})
                print(f"An unexpected error occurred while loading {file_path}: {e}")
        
        return data
    
    def get_dictionary_file_paths(self, selected_types):
        """
        Get file paths for selected dictionary types.
        """
        return [
            self.config.DICTIONARIES[dict_type]["file"]
            for dict_type in selected_types
            if dict_type in self.config.DICTIONARIES
        ]
    
    def get_source_type(self, file_path):
        """
        Detect dictionary source type from file path based on configuration.
        This is now the single source of truth.
        """
        for dict_info in self.config.DICTIONARIES.values():
            if dict_info["file"] == file_path:
                return dict_info["source"]
        return "deutsch"  # Default fallback if no match is found in config

    def validate_dictionary_data(self, data):
        """
        Validate and clean dictionary data, setting defaults for missing fields.
        """
        validated_data = []
        
        for entry in data:
            validated_entry = {
                self.config.WORD_1_COLUMN: entry.get(self.config.WORD_1_COLUMN, ""),
                self.config.WORD_2_COLUMN: entry.get(self.config.WORD_2_COLUMN, ""),
                self.config.PART_1_COLUMN: entry.get(self.config.PART_1_COLUMN, self.config.DEFAULT_PART_1),
                self.config.PART_2_COLUMN: entry.get(self.config.PART_2_COLUMN, self.config.DEFAULT_PART_2),
                self.config.SOURCE_COLUMN: entry.get(self.config.SOURCE_COLUMN, "deutsch")
            }

            # Validate weight is numeric
            try:
                weight = float(entry.get(self.config.WEIGHT_COLUMN))
            except (ValueError, TypeError, AttributeError):
                weight = self.config.DEFAULT_WEIGHT
            
            validated_entry[self.config.WEIGHT_COLUMN] = weight
            validated_data.append(validated_entry)
        
        return validated_data
    
    def get_dictionary_info(self, dict_type):
        """
        Get information about a specific dictionary type.
        """
        return self.config.DICTIONARIES.get(dict_type)
    
    def get_all_dictionary_types(self):
        """
        Get all available dictionary types.
        """
        return list(self.config.DICTIONARIES.keys())
    
    def get_default_checked_types(self):
        """
        Get dictionary types that should be checked by default.
        """
        return [
            dict_type
            for dict_type, dict_info in self.config.DICTIONARIES.items()
            if dict_info.get("default_checked", False)
        ]
    
    def get_loading_statistics(self):
        """
        Get progressive loading statistics.
        """
        if self.loading_config.ENABLE_PROGRESSIVE_LOADING:
            return self.progressive_loader.get_loading_statistics()
        return {"progressive_loading": False}
    
    def stop_progressive_loading(self):
        """
        Stop progressive loading operations.
        """
        if self.loading_config.ENABLE_PROGRESSIVE_LOADING:
            self.progressive_loader.stop_progressive_loading()
    
    def cleanup(self):
        """
        Clean up resources and stop all loading operations.
        """
        if self.loading_config.ENABLE_PROGRESSIVE_LOADING:
            self.progressive_loader.cleanup()
"""
Progressive Dictionary Loading System for the Flashcard Application.
Implements O(1) startup time with progressive content discovery.
"""

import pandas as pd
import random
import threading
from typing import List, Dict
from .flashcard_config import DictionaryConfig, ProgressiveLoadingConfig, external_path
from .tracing import tracer

# Fix: Remove the hardcoded 'sep' argument. It will be provided dynamically.
CSV_KWARGS = dict(engine='python', on_bad_lines='skip', quotechar='"', escapechar='\\')

class ProgressiveDictionaryManager:
    """
    Manages progressive loading of dictionary entries for O(1) performance.

    Features:
    - O(1) startup time regardless of dictionary size
    - Progressive content discovery every 60 seconds
    - Active dictionary focus (only loads selected dictionaries)
    - Random batch loading to ensure content variety
    - Constant memory usage
    """

    def __init__(self, dict_config=None, loading_config=None):
        self.dict_config = dict_config or DictionaryConfig()
        self.loading_config = loading_config or ProgressiveLoadingConfig()

        # Core state management
        self.loaded_entries = {}      # dict_type -> list of entries
        self.loaded_ranges = {}       # dict_type -> set of loaded ranges (start, end)
        self.total_entries = {}       # dict_type -> total count
        self.active_dictionaries = set()  # Currently selected dict types

        # Progressive loading state
        self.loading_timer = None
        self.loading_thread = None
        self.is_loading = False
        self.loading_lock = threading.Lock()

        # Performance tracking
        self.loading_stats = {
            'total_batches_loaded': 0,
            'total_entries_loaded': 0,
            'loading_times': []
        }

    def update_active_dictionaries(self, selected_types: List[str]) -> None:
        """
        Update which dictionaries are currently active and load initial batches.
        """
        with self.loading_lock:
            newly_activated = set(selected_types) - self.active_dictionaries
            deactivated = self.active_dictionaries - set(selected_types)
            self.active_dictionaries = set(selected_types)
            tracer.ic({"update_active": {"new": list(newly_activated), "off": list(deactivated)}})

            for dict_type in newly_activated:
                if dict_type not in self.loaded_entries:
                    self._load_initial_batch(dict_type)
                    print(f"Dynamically activated {dict_type} dictionary")
                else:
                    print(f"Dynamically reactivated {dict_type} dictionary")

            for dict_type in deactivated:
                print(f"Dynamically deactivated {dict_type} dictionary")

            if self.loading_config.BACKGROUND_LOADING:
                self._schedule_progressive_loading()

    def get_available_entries(self, selected_types: List[str]) -> List[Dict]:
        """
        Get all currently loaded entries for the selected dictionary types.
        """
        with self.loading_lock:
            combined_entries = []
            for dict_type in selected_types:
                if dict_type in self.loaded_entries:
                    combined_entries.extend(self.loaded_entries[dict_type])
            return combined_entries

    def _load_initial_batch(self, dict_type: str) -> None:
        """
        Load the initial batch of entries for a dictionary.
        """
        try:
            if dict_type not in self.dict_config.DICTIONARIES:
                print(f"Warning: Unknown dictionary type: {dict_type}")
                return

            dict_info = self.dict_config.DICTIONARIES[dict_type]
            file_path = dict_info["file"]
            tracer.ic({"init_batch": {"dict": dict_type, "file": file_path}})

            total_count = self._get_total_entry_count(dict_type, file_path)
            self.total_entries[dict_type] = total_count
            tracer.ic({"total_count": {"dict": dict_type, "total": total_count}})

            if total_count == 0:
                print(f"Warning: Empty dictionary file: {file_path}")
                return

            if total_count <= self.loading_config.BATCH_SIZE:
                entries = self._load_full_dictionary(dict_type, file_path)
                self.loaded_entries[dict_type] = entries
                self.loaded_ranges[dict_type] = {(0, total_count)}
                print(f"Loaded entire {dict_type} dictionary ({len(entries)} entries)")
            else:
                entries = self._load_random_batch(dict_type, file_path, total_count)
                self.loaded_entries[dict_type] = entries
                print(f"Loaded initial batch for {dict_type} ({len(entries)} entries)")

            self.loading_stats['total_batches_loaded'] += 1
            self.loading_stats['total_entries_loaded'] += len(entries)

        except Exception as e:
            tracer.ic({"init_batch_error": str(e)})
            print(f"Error loading initial batch for {dict_type}: {e}")
            self.loaded_entries[dict_type] = []
            self.loaded_ranges[dict_type] = set()

    def _load_random_batch(self, dict_type: str, file_path: str, total_count: int) -> List[Dict]:
        """
        Load a random batch of entries from a dictionary file.
        """
        max_start = max(0, total_count - self.loading_config.BATCH_SIZE)
        start_position = random.randint(0, max_start)
        end_position = min(start_position + self.loading_config.BATCH_SIZE, total_count)
        tracer.ic({"random_batch": {"dict": dict_type, "start": start_position, "end": end_position}})

        try:
            # Fix: Get the delimiter for the current dictionary
            dict_info = self.dict_config.DICTIONARIES[dict_type]
            delimiter = dict_info.get("delimiter", ",")

            df = pd.read_csv(external_path(file_path), skiprows=range(1, start_position + 1),
                           nrows=end_position - start_position, sep=delimiter, **CSV_KWARGS)

            entries = self._process_dataframe(df, dict_info)

            if dict_type not in self.loaded_ranges:
                self.loaded_ranges[dict_type] = set()
            self.loaded_ranges[dict_type].add((start_position, end_position))

            return entries

        except Exception as e:
            tracer.ic({"random_batch_error": str(e)})
            print(f"Error loading random batch from {file_path}: {e}")
            return []

    def _process_dataframe(self, df: pd.DataFrame, dict_info: Dict) -> List[Dict]:
        """
        Apply common processing steps to a loaded dictionary DataFrame.
        """
        if self.dict_config.WEIGHT_COLUMN not in df.columns:
            df[self.dict_config.WEIGHT_COLUMN] = self.dict_config.DEFAULT_WEIGHT

        df[self.dict_config.SOURCE_COLUMN] = dict_info["source"]
        df = self._apply_dynamic_weights(df)

        return df.to_dict(orient="records")

    def _apply_dynamic_weights(self, df) -> pd.DataFrame:
        """
        Apply dynamic weights based on content complexity and length.
        """
        def calculate_dynamic_weight(row):
            base_weight = 100
            definition = str(row.get('Word_2', ''))
            char_count = len(definition)
            word_count = len(definition.split())

            paragraph_indicators = [';', '1)', '2)', '3)', '4)', '5)', '§', 'GG§', 'StGB']
            has_paragraphs = any(indicator in definition for indicator in paragraph_indicators)

            legal_terms = ['StGB', 'GG§', 'Recht', 'Gesetz', 'Verfassung', 'Staat', 'Demokratie']
            has_legal_terms = any(term in definition for term in legal_terms)

            weight = base_weight

            if char_count > 200: weight += 50
            if char_count > 400: weight += 100
            if char_count > 600: weight += 150
            if has_paragraphs: weight += 100
            if has_legal_terms: weight += 50
            if word_count > 20: weight += 25
            if word_count > 40: weight += 50

            return int(weight)

        df[self.dict_config.WEIGHT_COLUMN] = df.apply(calculate_dynamic_weight, axis=1)

        weight_stats = df[self.dict_config.WEIGHT_COLUMN].describe()
        if weight_stats['max'] > 200:
            print(f"Dynamic weights applied - Min: {weight_stats['min']:.0f}, Max: {weight_stats['max']:.0f}, Mean: {weight_stats['mean']:.0f}")

        return df

    def _load_full_dictionary(self, dict_type: str, file_path: str) -> List[Dict]:
        """
        Load the entire dictionary file.
        """
        try:
            dict_info = self.dict_config.DICTIONARIES[dict_type]
            delimiter = dict_info.get("delimiter", ",")

            df = pd.read_csv(external_path(file_path), sep=delimiter, **CSV_KWARGS)
            tracer.ic({"full_load": {"dict": dict_type, "rows": len(df)}})

            return self._process_dataframe(df, dict_info)

        except Exception as e:
            tracer.ic({"full_load_error": str(e)})
            print(f"Error loading full dictionary from {file_path}: {e}")
            return []

    def _get_total_entry_count(self, dict_type: str, file_path: str) -> int:
        """
        Get the total number of entries in a dictionary file by efficiently counting lines.
        """
        full_path = external_path(file_path)
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                # We subtract 1 to account for the header row
                count = sum(1 for _ in f) - 1
            tracer.ic({"count_rows": {"file": full_path, "rows": count}})
            return max(0, count)
        except FileNotFoundError:
            tracer.ic({"count_error": "File not found", "file": full_path})
            print(f"Error: Dictionary file not found at {full_path}")
            return 0
        except Exception as e:
            tracer.ic({"count_error": str(e), "file": full_path})
            print(f"Error counting entries in {full_path}: {e}")
            return 0
    
    def _schedule_progressive_loading(self) -> None:
        """
        Schedule periodic progressive loading of new batches.
        """
        if not self.loading_config.ENABLE_PROGRESSIVE_LOADING:
            return
        
        if self.loading_timer:
            self.loading_timer.cancel()
        
        self.loading_timer = threading.Timer(
            self.loading_config.LOADING_INTERVAL,
            self._progressive_load_next_batches
        )
        self.loading_timer.daemon = True
        self.loading_timer.start()
    
    def _progressive_load_next_batches(self) -> None:
        """
        Load next batches for all active dictionaries.
        """
        if self.is_loading:
            return
        
        with self.loading_lock:
            self.is_loading = True
        
        try:
            for dict_type in self.active_dictionaries:
                if dict_type in self.total_entries:
                    self._load_next_batch(dict_type)
            
            self._schedule_progressive_loading()
            
        finally:
            with self.loading_lock:
                self.is_loading = False
    
    def _load_next_batch(self, dict_type: str) -> None:
        """
        Load the next batch for a specific dictionary.
        """
        try:
            if dict_type not in self.dict_config.DICTIONARIES:
                return
            
            dict_info = self.dict_config.DICTIONARIES[dict_type]
            file_path = dict_info["file"]
            total_count = self.total_entries.get(dict_type, 0)
            
            if total_count <= self.loading_config.BATCH_SIZE:
                return
            
            current_loaded = len(self.loaded_entries.get(dict_type, []))
            if current_loaded >= self.loading_config.MAX_LOADED_ENTRIES:
                return
            
            new_entries = self._load_random_batch(dict_type, file_path, total_count)
            
            if new_entries:
                if dict_type not in self.loaded_entries:
                    self.loaded_entries[dict_type] = []
                self.loaded_entries[dict_type].extend(new_entries)
                
                self.loading_stats['total_batches_loaded'] += 1
                self.loading_stats['total_entries_loaded'] += len(new_entries)
                
                print(f"Progressive load: Added {len(new_entries)} entries to {dict_type} "
                      f"(total: {len(self.loaded_entries[dict_type])})")
            
        except Exception as e:
            print(f"Error in progressive loading for {dict_type}: {e}")
    
    def get_loading_statistics(self) -> Dict:
        """
        Get current loading statistics.
        """
        with self.loading_lock:
            stats = self.loading_stats.copy()
            stats['active_dictionaries'] = list(self.active_dictionaries)
            stats['loaded_entries_per_dict'] = {
                dict_type: len(entries) 
                for dict_type, entries in self.loaded_entries.items()
            }
            stats['total_entries_per_dict'] = self.total_entries.copy()
            return stats
    
    def stop_progressive_loading(self) -> None:
        """
        Stop the progressive loading timer.
        """
        if self.loading_timer:
            self.loading_timer.cancel()
            self.loading_timer = None
    
    def cleanup(self) -> None:
        """
        Clean up resources and stop all loading operations.
        """
        self.stop_progressive_loading()
        with self.loading_lock:
            self.loaded_entries.clear()
            self.loaded_ranges.clear()
            self.total_entries.clear()
            self.active_dictionaries.clear()
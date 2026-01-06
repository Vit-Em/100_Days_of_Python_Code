# Flash Cards v8 - Multi-Purpose Learning Tool

## Description

**Flash Cards v8** is a **multi-purpose learning program** with **4 different dictionaries** for flexible and comprehensive language learning experiences. The application supports learning German, English, and custom vocabulary with Russian translations.

### 🎯 Multi-Purpose Design
The program can be used for various learning purposes:
- **General Language Education** (German, English)
- **Specialized Learning** (Law, Medicine, Technology, etc.)
- **Exam Preparation** (B1, B2, C1 levels)
- **Professional Development** (Business English, Technical terminology)

### 📚 4 Dictionaries Available:
- **🇩🇪 5k German Words** (German-Russian) - B1 level
- **🇬🇧 5k Oxford English Words** (English-Russian) - B1-C1 level
- **🇺🇸 150k American English Words** (English-Russian) - Comprehensive
- **⚖️ Custom Dictionary** (German Law Terms) - Specialized legal vocabulary

### ✨ Flexible Combinations
All 4 dictionaries can be selected **independently** and used in **any combinations** to create personalized learning programs.

### 🚀 Performance & Intelligence Features
- **O(1) Progressive Loading**: Fast startup with intelligent batch loading
- **Dynamic Dictionary Activation**: Real-time dictionary switching without restart
- **Intelligent Text Wrapping**: German hyphenation with pixel-based width calculation
- **Dynamic Content Weighting**: Complex definitions appear more frequently
- **Stabilized Font Sizing**: Consistent, readable text rendering
- **Clean Dependencies**: Only 9 essential packages for optimal performance

The application saves practice statistics and offers a modern, modular architecture with improved performance and user-friendliness.

## Project Structure

```
Flashcards/
├── Flash_Cards_main_v8.py                      # Main module: program entry point
├── modules/                                    # Folder for individual modules
│   ├── gui.py                                  # GUI module: Tkinter window, Canvas, Buttons, etc.
│   ├── flashcard_config.py                     # Configuration: All constants and settings
│   ├── flashcard_text_renderer.py              # Text rendering: Dynamic font sizes and text wrapping
│   ├── flashcard_dictionary_manager.py         # Dictionary manager: Loading and managing dictionaries
│   ├── flashcard_progressive_loader.py         # Progressive loading system for O(1) performance
│   ├── flashcard_card_display.py               # Card display: Rendering flashcard front and back
│   ├── flashcard_timer_manager.py              # Timer manager: Reaction time measurement
│   ├── flashcard_checkbox_factory.py           # Checkbox factory: DRY checkbox creation
│   ├── statistics.py                           # Statistics module: Save, load, calculate statistics
│   ├── data_handler.py                         # Data module: Load and save vocabulary data (CSV)
│   ├── card_logic.py                           # Module for card logic: Selection, display, flipping
│   ├── translation_api.py                      # API module: Translation API integration
│   ├── preprocess_dictionaries.py              # Utility to pre-process dictionaries for performance
│   ├── tracing.py                              # Central tracing utility
│   └── __init__.py                             # Makes 'modules' an importable package
├── data/                                       # Folder for data
│   ├── Words_deu-rus_v1.csv                   # 5k German words (German-Russian)
│   ├── 5k_Oxford_eng_words.csv                # 5k Oxford English words (English-Russian)
│   ├── 150k_ANC_eng_words_couted.csv          # 150k American English words (English-Russian)
│   ├── custom_dict.csv                         # Custom dictionary (Custom Dictionary)
│   └── achievements.csv                        # Learning statistics for self-control and motivation
├── images/                                     # Folder for images
│   ├── card_front.png                          # Front side of flashcard
│   ├── card_back.png                           # Back side of flashcard
│   ├── right.png                               # "I know" button
│   ├── wrong.png                               # "I don't know" button
│   ├── GER-RUS_icon.png                        # Icon for German words
│   ├── ENG-RUS_icon.png                        # Icon for Oxford English words
│   ├── USA-RUS_icon.png                        # Icon for American English words
│   ├── LAW_icon.png                            # Icon for Custom Dictionary
│   └── Program_icon.png                        # Program icon
├── help/                                       # Folder for help files
│   ├── FlashcardsHilfe.html                    # Help file in HTML format
│   ├── FlashcardsHilfe.odt                     # Help file in OpenDocument Text format
│   ├── FlashcardsHilfe.pdf                     # Help file in PDF format
│   └── FlashcardsHilfe.xml                     # Help file in XML format
├── _archive.keep/                              # Archive for no longer used files
├── requirements.txt                            # Python dependencies
├── TODO.md                                     # Development plan and progress
└── README.md                                   # Project description
```

### Modules (Refactored Architecture)
*   **Flash_Cards_main_v8.py**: Starts the application and connects the modules
*   **modules/gui.py**: Main GUI module with modular design
*   **modules/flashcard_config.py**: Central configuration of all constants and settings
*   **modules/flashcard_text_renderer.py**: Dynamic text rendering with automatic font size adjustment
*   **modules/flashcard_dictionary_manager.py**: Dictionary management and loading
*   **modules/flashcard_card_display.py**: Card rendering for front and back
*   **modules/flashcard_timer_manager.py**: Timer management for reaction time measurement
*   **modules/flashcard_checkbox_factory.py**: DRY checkbox creation
*   **modules/statistics.py**: Save and manage learning statistics
*   **modules/data_handler.py**: Load and save CSV data
*   **modules/card_logic.py**: Card logic for weighted selection
*   **modules/translation_api.py**: API integration for translations

### Data
*   **data/Words_deu-rus_v1.csv**: 5,000 German vocabulary (German-Russian)
*   **data/5k_Oxford_eng_words.csv**: 5,000 British English vocabulary (English-Russian)
*   **data/150k_ANC_eng_words_couted.csv**: 150,000 American English vocabulary (English-Russian)
*   **data/custom_dict.csv**: Custom dictionary (e.g., legal terminology). This file now supports complex, multi-line content and uses a tab (`\t`) delimiter. It must be processed with the `preprocess_dictionaries.py` script after any changes.
*   **data/achievements.csv**: Learning statistics and progress data

### Images
*   **images/card_front.png**: Front side of flashcard
*   **images/card_back.png**: Back side of flashcard
*   **images/right.png**: "I know" button
*   **images/wrong.png**: "I don't know" button
*   **images/GER-RUS_icon.png**: Icon for German words
*   **images/ENG-RUS_icon.png**: Icon for Oxford English words
*   **images/USA-RUS_icon.png**: Icon for American English words
*   **images/LAW_icon.png**: Icon for Custom Dictionary
*   **images/Program_icon.png**: Program icon

### Help Files
*   **help/FlashcardsHilfe.html**: Help file in HTML format
*   **help/FlashcardsHilfe.odt**: Help file in OpenDocument Text format
*   **help/FlashcardsHilfe.pdf**: Help file in PDF format
*   **help/FlashcardsHilfe.xml**: Help file in XML format

## Installation

1. **Install Python 3.12+** (recommended)
2. **Create virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # or
   .venv\Scripts\activate     # Windows
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   **Clean Dependencies**: Only 9 essential packages for optimal performance:
   - `pandas>=2.3.0` - Data manipulation
   - `numpy<2.0.0` - Numerical operations
   - `pyphen>=0.10.0` - German hyphenation
   - `bottleneck>=1.6.0` - Pandas optimization
   - `tkinter` - GUI framework (built-in)
   - `threading` - Background loading (built-in)
   - `random` - Weighted selection (built-in)
   - `csv` - Data handling (built-in)
   - `json` - Configuration (built-in)

## Usage

1. **Pre-process Custom Dictionary (if modified)**:
   If you have made changes to `data/custom_dict.csv`, you must run the pre-processing script to ensure optimal performance. This script analyzes the text and calculates the best way to display it.
   ```bash
   python modules/preprocess_dictionaries.py
   ```

2. **Start application**:
   ```bash
   python Flash_Cards_main_v8.py
   ```

3. **Select dictionaries**: Use checkboxes to combine different dictionaries:
   - 🇩🇪 **5k Wörter** (German Words)
   - 🇬🇧 **5k words** (Oxford English Words)
   - 🇺🇸 **150k words** (American English Words)
   - ⚖️ **custom dict** (Custom Dictionary)

4. **Learn**: Use "I know" and "I don't know" buttons to mark your progress

5. **Statistics**: Learning statistics are automatically saved

## Performance Improvements

### 🚀 O(1) Progressive Loading
- **Fast Startup**: Loads only 1,000 entries initially (vs. 150,000+ full load)
- **Background Loading**: Continuous learning without interruption
- **Memory Efficient**: Only active dictionaries consume memory
- **Dynamic Activation**: Switch dictionaries without restart

### 🧠 Intelligent Content Weighting
- **Complex Definitions**: Constitutional law concepts appear 4-6x more frequently
- **Content Analysis**: Automatic detection of important legal terminology
- **Balanced Learning**: Important concepts get more exposure
- **Dynamic Application**: Weights calculated in real-time

### 📝 Advanced Text Rendering
- **German Hyphenation**: Proper word breaking using Pyphen library
- **Pixel-Based Wrapping**: Consistent line lengths regardless of word length
- **Stabilized Fonts**: Consistent, readable text rendering
- **Multiline Alignment**: Proper vertical spacing for complex definitions

## New Features in v8

### ✅ Advanced Custom Dictionary Support
- **Complex Text Handling**: Full support for multi-line paragraphs, lists, and complex structures within the `custom_dict.csv`. This allows for detailed and rich content, such as legal texts or technical definitions.
- **New CSV Format**: The `custom_dict.csv` now uses a tab (`\t`) delimiter to reliably handle complex text containing commas and semicolons.

### ✅ Pre-processing for Performance
- **`preprocess_dictionaries.py` Utility**: A new tool that analyzes the `custom_dict.csv` and pre-calculates the optimal font size and layout for each card.
- **Runtime Performance Boost**: By pre-calculating rendering parameters, the main application avoids expensive on-the-fly calculations, resulting in a smoother and faster user experience.

### ✅ Progressive Loading System
- **`flashcard_progressive_loader.py`**: A new module that implements a sophisticated progressive loading system.
- **O(1) Startup Time**: The application starts instantly, regardless of the size of the dictionaries.
- **Dynamic Content Discovery**: The loader periodically discovers and loads new content in the background, ensuring a varied and seamless learning experience.
- **Memory Efficiency**: Only active dictionaries consume memory, and the loader manages memory usage by loading batches of entries.

### ✅ Enhanced Tracing
- **`tracing.py`**: A central tracing utility for debugging and monitoring the application's behavior.
- **Conditional Tracing**: Tracing can be enabled or disabled via an environment variable, providing detailed insights into the application's internal state without cluttering the output in production.


## New Features in v6

### ✅ Modular Architecture
- **DRY & SOLID principles** implemented
- **Functional file names** instead of generic names
- **Central configuration** of all constants
- **Modular components** for better maintainability

### ✅ Extended Dictionary Support
- **4 dictionaries** to choose from (German, Oxford, American, Custom)
- **Independent checkbox selection** - all combinations possible
- **Custom Dictionary** for special areas (e.g., legal terminology)
- **Dynamic dictionary activation** - real-time switching without restart

### ✅ Performance & Intelligence
- **O(1) Progressive Loading**: Fast startup with intelligent batch loading
- **Dynamic Content Weighting**: Complex definitions appear 4-6x more frequently
- **Background Loading**: Continuous learning without interruption
- **Memory Optimization**: Only loads active dictionaries

### ✅ Advanced Text Rendering
- **Intelligent text wrapping** with German hyphenation using Pyphen
- **Pixel-based width calculation** for consistent line lengths
- **Stabilized font sizes** for consistent learning experience
- **Multiline alignment** with proper vertical spacing

### ✅ Dynamic Content Weighting System
- **Intelligent Weighting**: Complex definitions get 4-6x higher weights
- **Content Analysis**: Length, structure, and legal terminology detection
- **Balanced Learning**: Important concepts appear more frequently
- **Automatic Application**: Weights calculated and applied dynamically

### ✅ Technical Improvements
- **Timer management** for reaction time measurement
- **Error handling** and stability
- **Clean dependencies** (only 9 essential packages including Pyphen)
- **Virtual environment** for isolated installation
- **Progressive loading system** with background threading

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

# Flashcard-Anwendung v8 - Multi-Purpose Lernwerkzeug

## Beschreibung

**Flash Cards v8** ist ein **multi-purpose Lernprogramm** mit **4 verschiedenen Wörterbüchern** für flexible und umfassende Sprachlern-Erfahrungen. Die Anwendung unterstützt das Erlernen von deutschen, englischen und benutzerdefinierten Vokabeln mit russischen Übersetzungen.

### 🎯 Multi-Purpose Design
Das Programm kann für verschiedene Lernzwecke eingesetzt werden:
- **Allgemeine Sprachausbildung** (Deutsch, Englisch)
- **Fachspezifisches Lernen** (Recht, Medizin, Technik, etc.)
- **Prüfungsvorbereitung** (B1, B2, C1 Niveau)
- **Berufliche Weiterbildung** (Business English, Fachterminologie)

### 📚 4 Wörterbücher zur Auswahl:
- **🇩🇪 5k Deutsche Wörter** (Deutsch-Russisch) - B1 Niveau
- **🇬🇧 5k Oxford Englische Wörter** (Englisch-Russisch) - B1-C1 Niveau
- **🇺🇸 150k Amerikanische Englische Wörter** (Englisch-Russisch) - Umfassend
- **⚖️ Benutzerdefiniertes Wörterbuch** (Custom Dictionary) - Flexibel anpassbar

### ✨ Flexible Kombinationen
Alle 4 Wörterbücher können **unabhängig voneinander** ausgewählt und in **beliebigen Kombinationen** verwendet werden, um personalisierte Lernprogramme zu erstellen.

Die Anwendung speichert Übungsstatistiken und bietet eine moderne, modulare Architektur mit verbesserter Performance und Benutzerfreundlichkeit.

## Projektstruktur

```
Flashcards/
├── Flash_Cards_main_v8.py                      # Hauptmodul: Startpunkt des Programms
├── modules/                                    # Ordner für die einzelnen Module
│   ├── gui.py                                  # GUI-Modul: Tkinter-Fenster, Canvas, Buttons, etc.
│   ├── flashcard_config.py                     # Konfiguration: Alle Konstanten und Einstellungen
│   ├── flashcard_text_renderer.py              # Text-Rendering: Dynamische Schriftgrößen und Textumbruch
│   ├── flashcard_dictionary_manager.py         # Wörterbuch-Manager: Laden und Verwalten der Wörterbücher
│   ├── flashcard_progressive_loader.py         # Progressives Ladesystem für O(1) Performance
│   ├── flashcard_card_display.py               # Karten-Anzeige: Rendering der Flashcard-Front- und Rückseite
│   ├── flashcard_timer_manager.py              # Timer-Manager: Reaktionszeit-Messung
│   ├── flashcard_checkbox_factory.py           # Checkbox-Factory: DRY Checkbox-Erstellung
│   ├── statistics.py                           # Statistik-Modul: Speichern, Laden, Berechnen von Statistiken
│   ├── data_handler.py                         # Daten-Modul: Laden und Speichern der Vokabeldaten (CSV)
│   ├── card_logic.py                           # Modul für die Kartenlogik: Auswahl, Anzeigen, Umdrehen
│   ├── translation_api.py                      # API-Modul: Übersetzungs-API Integration
│   ├── preprocess_dictionaries.py              # Dienstprogramm zur Vorverarbeitung von Wörterbüchern zur Leistungssteigerung
│   ├── tracing.py                              # Zentrales Tracing-Dienstprogramm
│   └── __init__.py                             # Macht 'modules' zu einem importierbaren Paket
├── data/                                       # Ordner für die Daten
│   ├── Words_deu-rus_v1.csv                   # 5k Deutsche Wörter (Deutsch-Russisch)
│   ├── 5k_Oxford_eng_words.csv                # 5k Oxford Englische Wörter (Englisch-Russisch)
│   ├── 150k_ANC_eng_words_couted.csv          # 150k Amerikanische Englische Wörter (Englisch-Russisch)
│   ├── custom_dict.csv                         # Benutzerdefiniertes Wörterbuch (Custom Dictionary)
│   └── achievements.csv                        # Lernstatistik für Selbstkontrolle und Motivation
├── images/                                     # Ordner für die Bilder
│   ├── card_front.png                          # Vorderseite von Flashkarte
│   ├── card_back.png                           # Rückseite von Flashkarte
│   ├── right.png                               # "Ich weiß"-Knopf
│   ├── wrong.png                               # "Ich weiß nicht"-Knopf
│   ├── GER-RUS_icon.png                        # Icon für Deutsche Wörter
│   ├── ENG-RUS_icon.png                        # Icon für Oxford Englische Wörter
│   ├── USA-RUS_icon.png                        # Icon für Amerikanische Englische Wörter
│   ├── LAW_icon.png                            # Icon für Custom Dictionary
│   └── Program_icon.png                        # Programm-Icon
├── help/                                       # Ordner für die Hilfedateien
│   ├── FlashcardsHilfe.html                    # Hilfedatei im HTML Format
│   ├── FlashcardsHilfe.odt                     # Hilfedatei im OpenDocument Text Format
│   ├── FlashcardsHilfe.pdf                     # Hilfedatei im PDF Format
│   └── FlashcardsHilfe.xml                     # Hilfedatei im XML Format
├── _archive.keep/                              # Archiv für nicht mehr verwendete Dateien
├── requirements.txt                            # Python-Abhängigkeiten
├── TODO.md                                     # Entwicklungsplan und Fortschritt
└── README.md                                   # Projektbeschreibung
```

### Module (Refactored Architecture)
*   **Flash_Cards_main_v8.py**: Startet die Anwendung und verbindet die Module
*   **modules/gui.py**: Haupt-GUI-Modul mit modularem Design
*   **modules/flashcard_config.py**: Zentrale Konfiguration aller Konstanten und Einstellungen
*   **modules/flashcard_text_renderer.py**: Dynamisches Text-Rendering mit automatischer Schriftgrößenanpassung
*   **modules/flashcard_dictionary_manager.py**: Wörterbuch-Management und -Laden
*   **modules/flashcard_card_display.py**: Karten-Rendering für Front- und Rückseite
*   **modules/flashcard_timer_manager.py**: Timer-Management für Reaktionszeit-Messung
*   **modules/flashcard_checkbox_factory.py**: DRY Checkbox-Erstellung
*   **modules/statistics.py**: Lernstatistiken speichern und verwalten
*   **modules/data_handler.py**: CSV-Daten laden und speichern
*   **modules/card_logic.py**: Kartenlogik für gewichtete Auswahl
*   **modules/translation_api.py**: API-Integration für Übersetzungen

### Daten
*   **data/Words_deu-rus_v1.csv**: 5.000 deutsche Vokabeln (Deutsch-Russisch)
*   **data/5k_Oxford_eng_words.csv**: 5.000 britische englische Vokabeln (Englisch-Russisch)
*   **data/150k_ANC_eng_words_couted.csv**: 150.000 amerikanische englische Vokabeln (Englisch-Russisch)
*   **data/custom_dict.csv**: Benutzerdefiniertes Wörterbuch (z.B. Rechtsterminologie). Diese Datei unterstützt jetzt komplexe, mehrzeilige Inhalte und verwendet einen Tabulator (`\t`) als Trennzeichen. Sie muss nach jeder Änderung mit dem Skript `preprocess_dictionaries.py` verarbeitet werden.
*   **data/achievements.csv**: Lernstatistiken und Fortschrittsdaten

### Bilder
*   **images/card_front.png**: Vorderseite der Flashcard
*   **images/card_back.png**: Rückseite der Flashcard
*   **images/right.png**: "Ich weiß"-Button
*   **images/wrong.png**: "Ich weiß nicht"-Button
*   **images/GER-RUS_icon.png**: Icon für deutsche Wörter
*   **images/ENG-RUS_icon.png**: Icon für Oxford englische Wörter
*   **images/USA-RUS_icon.png**: Icon für amerikanische englische Wörter
*   **images/LAW_icon.png**: Icon für Custom Dictionary
*   **images/Program_icon.png**: Programm-Icon

### Hilfedateien
*   **help/FlashcardsHilfe.html**: Hilfedatei im HTML Format
*   **help/FlashcardsHilfe.odt**: Hilfedatei im OpenDocument Text Format
*   **help/FlashcardsHilfe.pdf**: Hilfedatei im PDF Format
*   **help/FlashcardsHilfe.xml**: Hilfedatei im XML Format

## Installation

1. **Python 3.12+ installieren** (empfohlen)
2. **Virtuelle Umgebung erstellen**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # oder
   .venv\Scripts\activate     # Windows
   ```
3. **Abhängigkeiten installieren**:
   ```bash
   pip install -r requirements.txt
   ```

## Verwendung

1. **Benutzerdefiniertes Wörterbuch vorverarbeiten (falls geändert)**:
   Wenn Sie Änderungen an `data/custom_dict.csv` vorgenommen haben, müssen Sie das Vorverarbeitungsskript ausführen, um eine optimale Leistung zu gewährleisten. Dieses Skript analysiert den Text und berechnet die beste Art, ihn anzuzeigen.
   ```bash
   python modules/preprocess_dictionaries.py
   ```

2. **Anwendung starten**:
   ```bash
   python Flash_Cards_main_v8.py
   
   or in one command line
   
   cd /home/oem/Dokumente/_Python/100_Days/031 && source .venv/bin/activate && python3 Flash_Cards_main_v8.py
   
   ```

3. **Wörterbücher auswählen**: Verwende die Checkboxen um verschiedene Wörterbücher zu kombinieren:
   - 🇩🇪 **5k Wörter** (Deutsche Wörter)
   - 🇬🇧 **5k words** (Oxford Englische Wörter)
   - 🇺🇸 **150k words** (Amerikanische Englische Wörter)
   - ⚖️ **custom dict** (Benutzerdefiniertes Wörterbuch)

4. **Lernen**: Verwende die "Ich weiß" und "Ich weiß nicht" Buttons um deinen Fortschritt zu markieren

5. **Statistiken**: Die Lernstatistiken werden automatisch gespeichert

## Neue Features in v8

### ✅ Erweiterte Unterstützung für benutzerdefinierte Wörterbücher
- **Verarbeitung komplexer Texte**: Volle Unterstützung für mehrzeilige Absätze, Listen und komplexe Strukturen innerhalb der `custom_dict.csv`. Dies ermöglicht detaillierte und reichhaltige Inhalte, wie z.B. juristische Texte oder technische Definitionen.
- **Neues CSV-Format**: Die `custom_dict.csv` verwendet nun ein Tabulator-Trennzeichen (`\t`), um komplexe Texte, die Kommas und Semikolons enthalten, zuverlässig zu verarbeiten.

### ✅ Vorverarbeitung zur Leistungssteigerung
- **`preprocess_dictionaries.py`-Dienstprogramm**: Ein neues Werkzeug, das die `custom_dict.csv` analysiert und die optimale Schriftgröße und das Layout für jede Karte vorab berechnet.
- **Laufzeit-Leistungssteigerung**: Durch die Vorabberechnung der Rendering-Parameter vermeidet die Hauptanwendung teure On-the-fly-Berechnungen, was zu einer flüssigeren und schnelleren Benutzererfahrung führt.

### ✅ Progressives Ladesystem
- **`flashcard_progressive_loader.py`**: Ein neues Modul, das ein ausgeklügeltes progressives Ladesystem implementiert.
- **O(1) Startzeit**: Die Anwendung startet sofort, unabhängig von der Größe der Wörterbücher.
- **Dynamische Inhaltsentdeckung**: Der Lader entdeckt und lädt regelmäßig neue Inhalte im Hintergrund, was eine abwechslungsreiche und nahtlose Lernerfahrung gewährleistet.
- **Speichereffizienz**: Nur aktive Wörterbücher verbrauchen Speicher, und der Lader verwaltet die Speichernutzung durch das Laden von Eintragsstapeln.

### ✅ Verbessertes Tracing
- **`tracing.py`**: Ein zentrales Tracing-Dienstprogramm zur Fehlersuche und Überwachung des Anwendungsverhaltens.
- **Bedingtes Tracing**: Das Tracing kann über eine Umgebungsvariable aktiviert oder deaktiviert werden und liefert detaillierte Einblicke in den internen Zustand der Anwendung, ohne die Ausgabe in der Produktion zu überladen.


## Neue Features in v6

### ✅ Modulare Architektur
- **DRY & SOLID Prinzipien** implementiert
- **Funktionale Dateinamen** statt generischer Namen
- **Zentrale Konfiguration** aller Konstanten
- **Modulare Komponenten** für bessere Wartbarkeit

### ✅ Erweiterte Wörterbuch-Unterstützung
- **4 Wörterbücher** zur Auswahl (Deutsch, Oxford, Amerikanisch, Custom)
- **Unabhängige Checkbox-Auswahl** - alle Kombinationen möglich
- **Custom Dictionary** für spezielle Bereiche (z.B. Rechtsterminologie)
- **Performance-Optimierung** (American Dictionary auf 1.000 Einträge begrenzt)

### ✅ Verbesserte Benutzeroberfläche
- **Icon-basierte Checkboxen** für bessere Erkennbarkeit
- **Stabilisierte Schriftgrößen** für konsistente Lernerfahrung
- **Intelligenter Textumbruch** mit deutscher Silbentrennung für lange Phrasen
- **Programm-Icon** im Fenster

### ✅ Technische Verbesserungen
- **Timer-Management** für Reaktionszeit-Messung
- **Fehlerbehandlung** und Stabilität
- **Saubere Dependencies** (nur 9 essentielle Pakete inklusive Pyphen)
- **Virtuelle Umgebung** für isolierte Installation
- **Erweiterte Textdarstellung** mit pixel-basiertem Umbruch und deutscher Silbentrennung

## Lizenz

Dieses Projekt ist unter der [MIT Lizenz](https://opensource.org/licenses/MIT) lizenziert.

---

# Приложение для карточек v8 - Многоцелевой инструмент обучения

## Описание

**Flash Cards v8** - это **многоцелевая обучающая программа** с **4 различными словарями** для гибкого и всестороннего языкового обучения. Приложение поддерживает изучение немецких, английских и пользовательских словарей с русскими переводами.

### 🎯 Многоцелевой дизайн
Программа может использоваться для различных целей обучения:
- **Общее языковое образование** (Немецкий, Английский)
- **Специализированное обучение** (Право, Медицина, Техника, и т.д.)
- **Подготовка к экзаменам** (B1, B2, C1 уровень)
- **Профессиональное развитие** (Деловой английский, Специальная терминология)

### 📚 4 словаря на выбор:
- **🇩🇪 5k Немецких слов** (Немецко-Русский) - B1 уровень
- **🇬🇧 5k Оксфордских английских слов** (Англо-Русский) - B1-C1 уровень
- **🇺🇸 150k Американских английских слов** (Англо-Русский) - Всеобъемлющий
- **⚖️ Пользовательский словарь** (Custom Dictionary) - Гибко настраиваемый

### ✨ Гибкие комбинации
Все 4 словаря могут быть выбраны **независимо друг от друга** и использованы в **любых комбинациях** для создания персонализированных программ обучения.

Приложение сохраняет статистику обучения и предлагает современную модульную архитектуру с улучшенной производительностью и удобством использования.

## Структура проекта

```
Flashcards/
├── Flash_Cards_main_v8.py                      # Главный модуль: точка запуска программы
├── modules/                                    # Папка для отдельных модулей
│   ├── gui.py                                  # GUI-модуль: Tkinter-окно, Canvas, кнопки и т.д.
│   ├── flashcard_config.py                     # Конфигурация: Все константы и настройки
│   ├── flashcard_text_renderer.py              # Рендеринг текста: Динамические размеры шрифтов и перенос текста
│   ├── flashcard_dictionary_manager.py         # Менеджер словарей: Загрузка и управление словарями
│   ├── flashcard_progressive_loader.py         # Система прогрессивной загрузки для производительности O(1)
│   ├── flashcard_card_display.py               # Отображение карт: Рендеринг лицевой и обратной стороны карточек
│   ├── flashcard_timer_manager.py              # Менеджер таймера: Измерение времени реакции
│   ├── flashcard_checkbox_factory.py           # Фабрика чекбоксов: DRY создание чекбоксов
│   ├── statistics.py                           # Модуль статистики: Сохранение, загрузка, вычисление статистики
│   ├── data_handler.py                         # Модуль данных: Загрузка и сохранение данных словаря (CSV)
│   ├── card_logic.py                           # Модуль для логики карточек: Выбор, отображение, переворачивание
│   ├── translation_api.py                      # API-модуль: Интеграция API переводов
│   ├── preprocess_dictionaries.py              # Утилита для предварительной обработки словарей для повышения производительности
│   ├── tracing.py                              # Центральная утилита трассировки
│   └── __init__.py                             # Делает 'modules' импортируемым пакетом
├── data/                                       # Папка для данных
│   ├── Words_deu-rus_v1.csv                   # 5k Немецких слов (Немецко-Русский)
│   ├── 5k_Oxford_eng_words.csv                # 5k Оксфордских английских слов (Англо-Русский)
│   ├── 150k_ANC_eng_words_couted.csv          # 150k Американских английских слов (Англо-Русский)
│   ├── custom_dict.csv                         # Пользовательский словарь (Custom Dictionary)
│   └── achievements.csv                        # Статистика обучения для самоконтроля и мотивации
├── images/                                     # Папка для изображений
│   ├── card_front.png                          # Лицевая сторона карточки
│   ├── card_back.png                           # Обратная сторона карточки
│   ├── right.png                               # Кнопка "Я знаю"
│   ├── wrong.png                               # Кнопка "Я не знаю"
│   ├── GER-RUS_icon.png                        # Иконка для немецких слов
│   ├── ENG-RUS_icon.png                        # Иконка для оксфордских английских слов
│   ├── USA-RUS_icon.png                        # Иконка для американских английских слов
│   ├── LAW_icon.png                            # Иконка для Custom Dictionary
│   └── Program_icon.png                        # Иконка программы
├── help/                                       # Папка для файлов справки
│   ├── FlashcardsHilfe.html                    # Файл справки в формате HTML
│   ├── FlashcardsHilfe.odt                     # Файл справки в формате OpenDocument Text
│   ├── FlashcardsHilfe.pdf                     # Файл справки в формате PDF
│   └── FlashcardsHilfe.xml                     # Файл справки в формате XML
├── _archive.keep/                              # Архив для больше не используемых файлов
├── requirements.txt                            # Python зависимости
├── TODO.md                                     # План разработки и прогресс
└── README.md                                   # Описание проекта
```

### Модули (Рефакторенная архитектура)
*   **Flash_Cards_main_v8.py**: Запускает приложение и связывает модули
*   **modules/gui.py**: Главный GUI-модуль с модульным дизайном
*   **modules/flashcard_config.py**: Центральная конфигурация всех констант и настроек
*   **modules/flashcard_text_renderer.py**: Динамический рендеринг текста с автоматической настройкой размера шрифта
*   **modules/flashcard_dictionary_manager.py**: Управление словарями и загрузка
*   **modules/flashcard_card_display.py**: Рендеринг карт для лицевой и обратной стороны
*   **modules/flashcard_timer_manager.py**: Управление таймером для измерения времени реакции
*   **modules/flashcard_checkbox_factory.py**: DRY создание чекбоксов
*   **modules/statistics.py**: Сохранение и управление статистикой обучения
*   **modules/data_handler.py**: Загрузка и сохранение CSV данных
*   **modules/card_logic.py**: Логика карт для взвешенного выбора
*   **modules/translation_api.py**: API интеграция для переводов

### Данные
*   **data/Words_deu-rus_v1.csv**: 5,000 немецких слов (Немецко-Русский)
*   **data/5k_Oxford_eng_words.csv**: 5,000 британских английских слов (Англо-Русский)
*   **data/150k_ANC_eng_words_couted.csv**: 150,000 американских английских слов (Англо-Русский)
*   **data/custom_dict.csv**: Пользовательский словарь (например, правовая терминология). Этот файл теперь поддерживает сложный, многострочный контент и использует табуляцию (`\t`) в качестве разделителя. Он должен быть обработан с помощью скрипта `preprocess_dictionaries.py` после любых изменений.
*   **data/achievements.csv**: Статистика обучения и данные о прогрессе

### Изображения
*   **images/card_front.png**: Лицевая сторона карточки
*   **images/card_back.png**: Обратная сторона карточки
*   **images/right.png**: Кнопка "Я знаю"
*   **images/wrong.png**: Кнопка "Я не знаю"
*   **images/GER-RUS_icon.png**: Иконка для немецких слов
*   **images/ENG-RUS_icon.png**: Иконка для оксфордских английских слов
*   **images/USA-RUS_icon.png**: Иконка для американских английских слов
*   **images/LAW_icon.png**: Иконка для Custom Dictionary
*   **images/Program_icon.png**: Иконка программы

### Файлы справки
*   **help/FlashcardsHilfe.html**: Файл справки в формате HTML
*   **help/FlashcardsHilfe.odt**: Файл справки в формате OpenDocument Text
*   **help/FlashcardsHilfe.pdf**: Файл справки в формате PDF
*   **help/FlashcardsHilfe.xml**: Файл справки в формате XML

## Установка

1. **Установить Python 3.12+** (рекомендуется)
2. **Создать виртуальное окружение**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # или
   .venv\Scripts\activate     # Windows
   ```
3. **Установить зависимости**:
   ```bash
   pip install -r requirements.txt
   ```

## Использование

1. **Предварительная обработка пользовательского словаря (если он был изменен)**:
   Если вы внесли изменения в `data/custom_dict.csv`, вы должны запустить скрипт предварительной обработки для обеспечения оптимальной производительности. Этот скрипт анализирует текст и вычисляет наилучший способ его отображения.
   ```bash
   python modules/preprocess_dictionaries.py
   ```

2. **Запустить приложение**:
   ```bash
   python Flash_Cards_main_v8.py
   ```

3. **Выбрать словари**: Используйте чекбоксы для комбинирования различных словарей:
   - 🇩🇪 **5k Wörter** (Немецкие слова)
   - 🇬🇧 **5k words** (Оксфордские английские слова)
   - 🇺🇸 **150k words** (Американские английские слова)
   - ⚖️ **custom dict** (Пользовательский словарь)

4. **Обучение**: Используйте кнопки "Я знаю" и "Я не знаю" для отметки вашего прогресса

5. **Статистика**: Статистика обучения сохраняется автоматически

## Новые функции в v8

### ✅ Расширенная поддержка пользовательских словарей
- **Обработка сложных текстов**: Полная поддержка многострочных абзацев, списков и сложных структур в `custom_dict.csv`. Это позволяет использовать подробный и насыщенный контент, такой как юридические тексты или технические определения.
- **Новый формат CSV**: `custom_dict.csv` теперь использует табуляцию (`\t`) в качестве разделителя для надежной обработки сложных текстов, содержащих запятые и точки с запятой.

### ✅ Предварительная обработка для повышения производительности
- **Утилита `preprocess_dictionaries.py`**: Новый инструмент, который анализирует `custom_dict.csv` и предварительно рассчитывает оптимальный размер шрифта и макет для каждой карточки.
- **Повышение производительности во время выполнения**: Благодаря предварительному расчету параметров рендеринга основное приложение избегает дорогостоящих вычислений «на лету», что приводит к более плавной и быстрой работе пользователя.

### ✅ Система прогрессивной загрузки
- **`flashcard_progressive_loader.py`**: Новый модуль, реализующий сложную систему прогрессивной загрузки.
- **Время запуска O(1)**: Приложение запускается мгновенно, независимо от размера словарей.
- **Динамическое обнаружение контента**: Загрузчик периодически обнаруживает и загружает новый контент в фоновом режиме, обеспечивая разнообразный и беспроблемный процесс обучения.
- **Эффективность памяти**: Память потребляют только активные словари, а загрузчик управляет использованием памяти, загружая пакеты записей.

### ✅ Улучшенная трассировка
- **`tracing.py`**: центральная утилита трассировки для отладки и мониторинга поведения приложения.
- **Условная трассировка**: трассировку можно включить или отключить с помощью переменной среды, что дает подробное представление о внутреннем состоянии приложения, не загромождая вывод в рабочей среде.


## Новые функции в v6

### ✅ Модульная архитектура
- **DRY & SOLID принципы** реализованы
- **Функциональные имена файлов** вместо общих имен
- **Центральная конфигурация** всех констант
- **Модульные компоненты** для лучшей поддерживаемости

### ✅ Расширенная поддержка словарей
- **4 словаря** на выбор (Немецкий, Оксфорд, Американский, Custom)
- **Независимый выбор чекбоксов** - все комбинации возможны
- **Custom Dictionary** для специальных областей (например, правовая терминология)
- **Оптимизация производительности** (Американский словарь ограничен 1,000 записями)

### ✅ Улучшенный пользовательский интерфейс
- **Чекбоксы на основе иконок** для лучшего распознавания
- **Стабилизированные размеры шрифтов** для последовательного обучения
- **Интеллектуальный перенос текста** с немецкой расстановкой переносов для длинных фраз
- **Иконка программы** в окне

### ✅ Технические улучшения
- **Управление таймером** для измерения времени реакции
- **Обработка ошибок** и стабильность
- **Чистые зависимости** (только 9 основных пакетов включая Pyphen)
- **Виртуальное окружение** для изолированной установки
- **Расширенный рендеринг текста** с пиксельным переносом и немецкой расстановкой переносов

## Лицензия

Этот проект лицензирован в соответствии с [лицензией MIT](https://opensource.org/licenses/MIT).
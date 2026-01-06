# Flashcard-Anwendung (Deutsch - Russisch)

## Beschreibung

Dieses Programm ist ein interaktives Flashcard-Anwendung, 
das beim Erlernen von deutschen Vokabeln mit russischen 
Übersetzungen hilft. Es verwendet eine gewichtete Auswahl 
von ca. 5000 deutschen, 5000 britisch englischen und/oder 
150k amerikanisch englischen Vokabeln, um das Lernen zu 
optimieren, und speichert die Übungsstatistiken über 
Ihren Lernfortschritte in eine Textdatei als eine Tabelle.
Die 5 Version beinhaltet eine Vorgabe für dynamische 
Aktualisierung von Lern-Wörtebüche aber zurzeit verwendet 
nur die lokale Wort-Daten (s. Daten).

## Projektstruktur

Flashcards/
├── Flash_Cards_main.py							# Hauptmodul: Startpunkt des Programms
├── modules/									# Ordner für die einzelnen Module
│ ├── gui.py									# GUI-Modul: Tkinter-Fenster, Canvas, Buttons, etc.
│ ├── statistics.py								# Statistik-Modul: Speichern, Laden, Berechnen von Statistiken
│ ├── data_handler.py							# Daten-Modul: Laden und Speichern der Vokabeldaten (CSV)
│ ├── card_logic.py								# Modul für die Kartenlogik: Auswahl, Anzeigen, Umdrehen
│ └── init.py									# Macht 'modules' zu einem importierbaren Paket
├── data/										# Ordner für die Daten
│ ├── 5k_German_frequent_words(deu-rus).csv		# Datenbank mit DEU/RUS-Lerninhalt, strukturiert als eine Spreadsheet-ASCII-Datei 
│ ├── 5k_Oxford_eng_words.csv					# Datenbank mit ENG/RUS-Lerninhalt, strukturiert als eine Spreadsheet-ASCII-Datei
│ ├── 150k_ANC_eng_words_couted.csv				# Datenbank mit ENG/RUS-Lerninhalt, strukturiert als eine Spreadsheet-ASCII-Datei
│ └── achievements.csv							# Lernstatistik für Selbstkontrolle und Motivation
├── images/										# Ordner für die Bilder
│ ├── card_front.png							# Vorderseite von Flashkarte
│ ├── card_back.png								# Rückseite von Flashkarte
│ ├── right.png									# "Ich_weiß"/"I_know"-Knopf: Befehl die nächste Flashkarte zeigen
│ └── wrong.png									# "Ich_weiß_nicht"/"Idon't_know"-Knopf: Befehl die Rückseite von Flashkarte zeigen und mit nächstem Klick die Forderseite nächster Flashkarte zeigen
├── help/										# Ordner für die Hilfedateien
│ ├── FlashcardsHilfe.odt						# Hilfedatei im OpenDocument Text Format
│ └── FlashcardsHilfe.xml						# Hilfedatei im XML Format
└── README.md									# Kurze Beschreibung des Projekts


### Module
*   Flash_Cards_main.py: Startet die Anwendung und verbindet die Module.
*   modules/gui.py: Verwaltet die grafische Benutzeroberfläche (GUI) der Anwendung.
*   modules/statistics.py: Speichert und verwaltet die Lernstatistiken.
*   modules/data_handler.py: Lädt die Vokabeldaten aus der CSV-Datei.
*   modules/card_logic.py: Steuert die Logik für die Auswahl der Vokabelkarten.

### Daten
*   data/Words_deu-rus_v1.csv: Enthält die 5000 von DEU-Vokabelnpaaren und Übersetzungen auf Russisch.
*   data/5k_Oxford_eng_words.csv: Enthält die 5000 von britischen ENG-Vokabelnpaaren (von B1 bis C1 level) und Übersetzungen auf Russisch.
*	data/150k_ANC_eng_words_couted.csv: Enthält die 150000 von amerikanischen ENG-Vokabelnpaaren und Übersetzungen auf Russisch.
*	data/achievements.csv: Speichert die Lernstatistiken.

### Bilder
*   images/card_front.png: Bild für die Vorderseite der Flashcard.
*   images/card_back.png: Bild für die Rückseite der Flashcard.
*   images/right.png: Bild für die "richtig"-Taste.
*   images/wrong.png: Bild für die "falsch"-Taste.

### Hilfedateien
*   help/FlashcardsHilfe.odt: Hilfedatei im OpenDocument Text Format.
*   help/FlashcardsHilfe.xml: Hilfedatei im XML Format.

## Installation

1.  Stelle sicher, dass Python 3.x installiert ist.
2.  Installiere die benötigten Pakete:

pip install pandas tkinter

## Verwendung

1.  Starte die Anwendung in der Console mit: 

python Flash_Cards_main.py

2.  Verwende die "richtig"- und "falsch"-Tasten, um deinen Fortschritt zu markieren.
3.  Die Statistiken werden automatisch gespeichert, wenn die Anwendung geschlossen wird.

## Lizenz

Dieses Projekt ist unter der [MIT Lizenz](https://opensource.org/licenses/MIT) lizenziert.



# Приложение для карточек (Немецкий - Русский)

## Описание

Это интерактивное приложение для карточек, которое помогает в изучении немецких слов с русскими переводами. Оно использует взвешенный выбор из примерно 5000 слов для оптимизации обучения и сохраняет статистику ваших успехов.

## Структура проекта

├── Flash_Cards_main.py						# Главный модуль: точка запуска программы
├── modules/								# Папка для отдельных модулей
│ ├── gui.py								# GUI-модуль: Tkinter-окно, Canvas, кнопки и т.д.
│ ├── statistics.py							# Модуль статистики: сохранение, загрузка, вычисление статистики
│ ├── data_handler.py						# Модуль данных: загрузка и сохранение данных словаря (CSV)
│ ├── card_logic.py							# Модуль для логики карточек: выбор, отображение, переворачивание
│ └── init.py								# Делает 'modules' импортируемым пакетом
├── data/									# Папка для данных
│ ├── 5k_German_frequent_words(deu-rus).csv # База данных с учебным контентом, структурированная как Spreadsheet-ASCII-файл
│ └── achievements.csv
├── images/									# Папка для изображений
│ ├── card_front.png
│ ├── card_back.png
│ ├── right.png
│ └── wrong.png
├── help/									# Папка для файлов справки
│ ├── FlashcardsHilfe.odt					# Файл справки в формате OpenDocument Text
│ └── FlashcardsHilfe.xml					# Файл справки в формате XML
└── README.md								# Краткое описание проекта


### Модули
*   Flash_Cards_main.py: Запускает приложение и связывает модули.
*   modules/gui.py: Управляет графическим интерфейсом пользователя (GUI) приложения.
*   modules/statistics.py: Сохраняет и управляет статистикой обучения.
*   modules/data_handler.py: Загружает данные словаря из CSV-файла.
*   modules/card_logic.py: Управляет логикой выбора карточек со словами.

### Данные
*   data/5k_German_frequent_words(deu-rus).csv: Содержит словарь и переводы.
*   data/achievements.csv: Сохраняет статистику обучения.

### Изображения
*   images/card_front.png: Изображение для лицевой стороны карточки.
*   images/card_back.png: Изображение для обратной стороны карточки.
*   images/right.png: Изображение для кнопки "правильно".
*   images/wrong.png: Изображение для кнопки "неправильно".

### Файлы справки
*   help/FlashcardsHilfe.odt: Файл справки в формате OpenDocument Text.
*   help/FlashcardsHilfe.xml: Файл справки в формате XML.

## Установка

1.  Убедитесь, что установлен Python 3.x.
2.  Установите необходимые пакеты:

pip install pandas tkinter


## Использование

1.  Запустите приложение в консоли с помощью команды:

python Flash_Cards_main.py


2.  Используйте кнопки "правильно" и "неправильно", чтобы отмечать свой прогресс.
3.  Статистика будет автоматически сохранена при закрытии приложения.

## Лицензия

Этот проект лицензирован в соответствии с [лицензией MIT](https://opensource.org/licenses/MIT).

#TODO: Create a letter using starting_letter.txt 
#for each name in invited_names.txt
#Replace the [name] placeholder with the actual name.
#Save the letters in the folder "ReadyToSend".
    
#Hint1: This method will help you: https://www.w3schools.com/python/ref_file_readlines.asp
    #Hint2: This method will also help you: https://www.w3schools.com/python/ref_string_replace.asp
        #Hint3: THis method will help you: https://www.w3schools.com/python/ref_string_strip.asp

import os
from datetime import datetime
import locale

# Konstanten
EVENT_DATE = "2025-01-31"  # Datum des Events
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Basisverzeichnis
TEMPLATE_PATH = os.path.join(BASE_DIR, "Input", "Letters", "starting_letter.txt")
OUTPUT_DIR = os.path.join(BASE_DIR, "Output", "ReadyToSend")
NAMES_PATH = os.path.join(BASE_DIR, "Input", "Names", "invited_names.txt")
TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Setzen der deutschen Lokalisierung für Wochentage
# locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
# locale.setlocale(locale.LC_TIME, 'uk_UA.UTF-8')
locale.setlocale(locale.LC_TIME, 'en_GB.UTF-8')

def format_event_date(date_string):
    # Konvertiere den Datumsstring in ein datetime-Objekt
    event_date = datetime.strptime(date_string, "%Y-%m-%d")

    # Formatiere das Datum mit Wochentag
    return event_date.strftime("%A, %Y-%m-%d")

def generate_invitations():
    names = read_names()
    letter_template = read_template_file(TEMPLATE_PATH)
    os.makedirs(OUTPUT_DIR, exist_ok=True)  # Sicherstellen, dass der Zielordner existiert

    for name in names:
        letter_content = generate_letter_content(letter_template, name)
        save_letter(letter_content, f"{OUTPUT_DIR}/letter_for_{name}_{TIMESTAMP}.txt")

    print(f"{len(names)} Einladungen wurden erstellt.")

def read_names():
    if not os.path.exists(NAMES_PATH):  # Fehlerbehandlung, wenn die Datei fehlt
        raise FileNotFoundError(f"Die Datei mit den Namen wurde nicht gefunden: {NAMES_PATH}")
    with open(NAMES_PATH, "r") as file:
        return [line.strip() for line in file.readlines()]

def read_template_file(file_path):
    if not os.path.exists(file_path):  # Fehlerbehandlung, wenn die Vorlage fehlt
        raise FileNotFoundError(f"Die Briefvorlage wurde nicht gefunden: {file_path}")
    with open(file_path, "r") as file:
        return file.read()

def generate_letter_content(template, name):
    return (template
            .replace("[name]", name)
            .replace("[event_date]", format_event_date(EVENT_DATE))
            .replace("[date_now]", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

def save_letter(content, file_path):
    with open(file_path, "w") as file:
        file.write(content)


if __name__ == "__main__":
    try:
        generate_invitations()
    except FileNotFoundError as e:
        print(f"Fehler: {e}")
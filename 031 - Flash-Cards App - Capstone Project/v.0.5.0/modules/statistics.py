# modules/statistics.py
import pandas as pd
import os
from datetime import datetime


def save_statistics(click_times, known_count, unknown_count):
    current_time = datetime.now()
    date = current_time.strftime("%d.%m.%Y")
    time_str = current_time.strftime("%H:%M:%S")
    duration = "N/A"  # Die Übungsdauer wird hier nicht berechnet
    avg_reaction_time = 0

    if click_times:
        avg_reaction_time = sum(click_times) / len(click_times)

    data = {
        "Datum": [date],
        "Zeit": [time_str],
        "Übungsdauer": [duration],
        "Richtig": [known_count],
        "Falsch": [unknown_count],
        "Durchschnittliche Reaktionszeit": [f"{avg_reaction_time:.4f}"],
    }

    df = pd.DataFrame(data)

    file_path = "data/achievements.csv"
    if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
        df.to_csv(file_path, index=False)
    else:
        try:
            existing_df = pd.read_csv(file_path)
            combined_df = pd.concat([existing_df, df], ignore_index=True)
            combined_df.to_csv(file_path, index=False)
        except pd.errors.EmptyDataError:
            df.to_csv(file_path, index=False)
        except Exception as e:
            print(f"Unerwarteter Fehler beim Lesen/Schreiben der Datei: {e}")

    return data

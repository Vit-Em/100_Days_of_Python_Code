from tkinter import *
import math
import os
import sys
"""This code implements "The Pomodoro Technique: The Acclaimed Time-Management System That Has Transformed How We Work " by Francesco Cirillo. See also https://de.wikipedia.org/wiki/Pomodoro-Technik"""
# Funktion zur Ermittlung des korrekten Ressourcenpfads
def resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0  # Zählt die Anzahl der Arbeits- und Pausenzyklen
timer = None  # Globale Variable für den Timer

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    window.after_cancel(timer)  # Stoppt den Timer
    canvas.itemconfig(timer_text, text="00:00")  # Setzt den Timer-Text zurück
    title_label.config(text="Timer")  # Setzt den Titel zurück
    check_marks.config(text="")  # Setzt die Häkchen zurück
    global reps
    reps = 0  # Setzt die Zyklen zurück

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:  # Lange Pause nach 4 Arbeitseinheiten
        countdown(long_break_sec)
        title_label.config(text="Pause", fg=RED)
        window.after(long_break_sec * 1000 - 5000, bring_window_to_front)
    elif reps % 2 == 0:  # Kurze Pause nach jeder Arbeitseinheit
        countdown(short_break_sec)
        title_label.config(text="Pause", fg=PINK)
        window.after(short_break_sec * 1000 - 5000, bring_window_to_front)
    else:  # Arbeitseinheit
        countdown(work_sec)
        title_label.config(text="Arbeit", fg=GREEN)
        window.after(5000, minimize_window)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def countdown(count):
    count_min = math.floor(count / 60)  # Minuten berechnen
    count_sec = count % 60  # Sekunden berechnen
    canvas.itemconfig(timer_text, text=f"{count_min:02}:{count_sec:02}")  # Zeit anzeigen

    if count > 0:
        global timer
        timer = window.after(1000, countdown, count - 1)  # Timer aktualisieren
    elif count == 0:
        window.deiconify()  # Stellt sicher, dass das Fenster sichtbar ist, wenn der Countdown endet
    else:
        start_timer()  # Nächsten Zyklus starten
        marks = ""
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            marks += "✔"
        check_marks.config(text=marks)  # Häkchen anzeigen

# ---------------------------- MINIMIZE WINDOW ------------------------------- #
def minimize_window():
    window.iconify()

# ---------------------------- BRING WINDOW TO FRONT ------------------------------- #
def bring_window_to_front():
    window.deiconify()
    window.lift()
    window.attributes('-topmost', True)
    window.after_idle(window.attributes, '-topmost', False)

# ---------------------------- CENTER WINDOW ------------------------------- #
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")
    window.resizable(False, False)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

center_window(window, 700, 500)

title_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50, "bold"), width=10)
title_label.grid(row=0, column=1)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file=resource_path("tomato.png"))
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

start_button = Button(text="Start", bg=YELLOW, font=(FONT_NAME, 10), command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", bg=YELLOW, font=(FONT_NAME, 10), command=reset_timer)
reset_button.grid(column=2, row=2)

check_marks = Label(fg=GREEN, bg=YELLOW)
check_marks.grid(column=1, row=3)

window.mainloop()

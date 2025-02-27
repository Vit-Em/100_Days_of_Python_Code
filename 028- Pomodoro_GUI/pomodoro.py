# This code implements "The Pomodoro Technique: The Acclaimed Time-Management System
# That Has Transformed How We Work " by Francesco Cirillo.
# See also https://de.wikipedia.org/wiki/Pomodoro-Technik

from tkinter import *
import math
import os

# Constants
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

# Global variables
timer = None
reps = 0  # Track repetitions (work/break sessions)


# ---------------------------- RESOURCE PATH ------------------------------- #
def resource_path(relative_path):
    """Get the absolute path for resources such as images."""
    base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    """Reset the timer and UI."""
    global timer, reps
    reps = 0  # Reset repetitions

    if timer is not None:
        try:
            window.after_cancel(timer)  # Cancel any active timer
        except ValueError as e:
            print(f"Error while canceling the timer: {e}")

    # Reset the UI elements
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer", fg=GREEN)
    check_marks.config(text="")


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    """Start the timer for work, short break, or long break sessions."""
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    # Decide whether to start work, short break, or long break
    if reps % 8 == 0:
        # Long break after 4 work sessions
        countdown(long_break_sec)
        title_label.config(text="Long Break", fg=RED)
        window.after(long_break_sec * 1000 - 5000, bring_window_to_front)
    elif reps % 2 == 0:
        # Short break after each work session
        countdown(short_break_sec)
        title_label.config(text="Short Break", fg=PINK)
        window.after(short_break_sec * 1000 - 5000, bring_window_to_front)
    else:
        # Work session
        countdown(work_sec)
        title_label.config(text="Work", fg=GREEN)
        window.after(5000, minimize_window)


# ---------------------------- WINDOW MANAGEMENT ------------------------------- #
def bring_window_to_front():
    """Bring the application window to the front."""
    try:
        window.attributes('-topmost', 1)
        window.attributes('-topmost', 0)
    except Exception as e:
        print(f"Error bringing window to front: {e}")


def minimize_window():
    """Minimize the application window."""
    try:
        window.iconify()
    except Exception as e:
        print(f"Error minimizing window: {e}")


def center_window(window, width, height):
    """Center the tkinter window on the screen."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")
    window.resizable(False, False)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def countdown(count):
    """Countdown mechanism to manage the timer."""
    count_min = math.floor(count / 60)  # Calculate minutes
    count_sec = count % 60  # Calculate seconds
    canvas.itemconfig(timer_text, text=f"{count_min:02}:{count_sec:02}")  # Update UI timer

    if count > 0:
        global timer
        timer = window.after(1000, countdown, count - 1)  # Schedule the next second
    else:
        start_timer()  # Automatically move to the next session
        update_checkmarks()


def update_checkmarks():
    """Update checkmarks to indicate completed work sessions."""
    work_sessions = math.floor(reps / 2)
    marks = "✔" * work_sessions
    check_marks.config(text=marks)


# ---------------------------- MAIN PROGRAM ------------------------------- #
# Create the main UI window
window = Tk()
window.title("Pomodoro Timer")
window.config(padx=100, pady=50, bg=YELLOW)

# Title label
title_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50))
title_label.grid(column=1, row=0)

# Canvas for timer display
try:
    img_path = resource_path("tomato.png")  # Tomato image for the timer
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"'tomato.png' not found at {img_path}")

    tomato_img = PhotoImage(file=img_path)
except Exception as e:
    print(f"Error loading image: {e}")
    tomato_img = None

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
if tomato_img:
    canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 132, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

# Start and reset buttons
start_button = Button(text="Start", highlightbackground=YELLOW, command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", highlightbackground=YELLOW, command=reset_timer)
reset_button.grid(column=2, row=2)

# Checkmarks
check_marks = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 20))
check_marks.grid(column=1, row=3)

if __name__ == "__main__":
    # Start the application
    window.mainloop()

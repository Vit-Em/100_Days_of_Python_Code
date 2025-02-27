import turtle as tr
# Install pandas if not already installed
import pandas as pd
import random
import time
import tkinter as tk
from tkinter.simpledialog import askstring

# Daten laden
data = pd.read_csv("50_states.csv")
states = data["state"].tolist()
x_coords = data["x"].tolist()
y_coords = data["y"].tolist()

# Bildschirm einrichten
screen = tr.Screen()
screen.title("U.S. States Game")
screen.setup(width=725, height=491)
image = "blank_states_img.gif"
screen.addshape(image)
tr.shape(image)

# Punktobjekt für den aktuellen grünen Punkt erstellen
green_point = tr.Turtle()
green_point.shape("circle")
green_point.color("green")
green_point.penup()
green_point.shapesize(0.5, 0.5)
green_point.hideturtle()


# Funktion zum Anzeigen eines zufälligen grünen Punktes
def show_random_green_point():
    available_indices = [i for i in range(len(states)) if states[i] not in guessed_states]
    if not available_indices:
        return None  # Keine verfügbaren Staaten mehr
    index = random.choice(available_indices)
    green_point.goto(x_coords[index], y_coords[index])
    green_point.showturtle()
    return index


# Funktion zur Formatierung der Zeit
def format_time(seconds):
    minutes, secs = divmod(int(seconds), 60)
    return f"{minutes:02d}:{secs:02d}"


# Funktion zum Aktualisieren der Anzeige
def update_display(elapsed_time, guessed_count):
    display_turtle.clear()
    display_turtle.write(f"Zeit: {format_time(elapsed_time)} | Fortschritt: {guessed_count}/50",
                         align="center", font=("Arial", 16, "normal"))
    screen.update()


# Funktion zur kontinuierlichen Zeitaktualisierung
def update_time():
    global start_time
    elapsed_time = time.time() - start_time
    update_display(elapsed_time, len(guessed_states))
    screen.ontimer(update_time, 1000)  # Aktualisiert jede Sekunde


# Funktion für benutzerfreundliche Eingabe mithilfe von Tkinter
def get_answer(title, prompt):
    root = tk.Tk()
    root.withdraw()  # Versteckt das Haupt-Tk-Fenster
    root.focus_force()  # Setzt den Fokus direkt auf den Eingabedialog
    answer = askstring(title, prompt)  # Zeigt ein Eingabefenster an
    root.destroy()  # Schließt das Tkinter-Fenster vollständig
    return answer


# Anzeige-Turtle erstellen
display_turtle = tr.Turtle()
display_turtle.hideturtle()
display_turtle.penup()
display_turtle.goto(0, 220)  # Position oben mittig

# Initialisieren der globalen Variablen
guessed_states = []
start_time = time.time()  # Startzeit festlegen

# Tracer ausschalten für flüssigere Anzeige
screen.tracer(0)

# Starten Sie die Zeitaktualisierung
update_time()

# Hauptspielschleife
current_state_index = show_random_green_point()

while current_state_index is not None:
    answer_state = get_answer(
        title=f"{len(guessed_states)}/50 States Correct",
        prompt="What's another state's name?"
    )

    if answer_state is None or answer_state.title() == "Canada":
        break

    answer_state = answer_state.title()

    if answer_state == states[current_state_index]:  # Richtige Antwort
        guessed_states.append(answer_state)
        green_point.hideturtle()  # Grünen Punkt verstecken

        # Den Namen des Staates anzeigen
        t = tr.Turtle()
        t.hideturtle()
        t.penup()
        t.goto(x_coords[current_state_index], y_coords[current_state_index])
        t.write(answer_state, align="center", font=("Arial", 10, "normal"))

        current_state_index = show_random_green_point()  # Nächsten grünen Punkt anzeigen

    else:  # Falsche Antwort
        red_point = tr.Turtle()
        red_point.shape("circle")
        red_point.color("red")
        red_point.penup()
        red_point.shapesize(0.5, 0.5)
        red_point.goto(green_point.pos())  # Grünen Punkt durch roten ersetzen

        green_point.hideturtle()  # Grünen Punkt verstecken

        current_state_index = show_random_green_point()  # Nächsten grünen Punkt anzeigen

# Spielende
final_time = time.time() - start_time
update_display(final_time, len(guessed_states))

print("Spiel beendet!")
print(f"Sie haben {len(guessed_states)} von 50 Staaten in {format_time(final_time)} erraten.")

# Ressourcen freigeben und Fenster schließen
green_point.clear()
green_point.hideturtle()

for turtle in tr.turtles():
    turtle.clear()
    turtle.hideturtle()

# Automatisches Schließen des Fensters nach dem Spielende
screen.bye()  # Fenster schließen, wenn das Spiel beendet wird

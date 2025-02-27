from pynput import keyboard
import signal
import threading

# Globale Variable zur Steuerung des Listener-Threads
stop_listener = threading.Event()


# Signalhandler für sauberes Beenden bei STRG+C (SIGINT)
def signal_handler(sig, frame):
    print("\nSTRG+C erkannt. Programm wird beendet.")
    stop_listener.set()


# Funktion zum Verarbeiten gedrückter Tasten
def on_press(key):
    try:
        # Sicherstellen, dass key.char einen gültigen Wert hat
        if key.char is not None:
            key_code = ord(key.char)
            print(f"'{key.char}' (ASCII: {key_code})")
        else:
            print(f"{key}")
    except AttributeError:
        # Dieser Block wird für Tastendrücke wie Funktionstasten verwendet
        print(f"{key}")


# Funktion beim Loslassen von Tasten
def on_release(key):
   #print(f"Taste losgelassen: {key}")
    if key == keyboard.Key.esc:
        print("ESC gedrückt. Programm wird beendet...")
        stop_listener.set()
        return False


# Hauptfunktion des Keyloggers
def main():
    print("Drücken Sie Tasten (ESC oder STRG+C zum Beenden):")

    # Registrieren des Signalhandlers für STRG+C
    signal.signal(signal.SIGINT, signal_handler)

    # Tastatureingaben abhören
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        while not stop_listener.is_set():
            listener.join(timeout=0.1)  # Kurzes Timeout für eine reaktive Schleife

    print("Programm erfolgreich beendet.")


if __name__ == "__main__":
    main()

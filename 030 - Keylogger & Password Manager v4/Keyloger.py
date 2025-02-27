from pynput import keyboard


def on_press(key):
    """Verarbeitet Tastendruck-Ereignisse."""
    try:
        # Tasteneigenschaft auslesen und als Hexadezimalwert anzeigen
        hex_code = f"0x{ord(key.char):02X}" if hasattr(key, 'char') else "N/A"
        print(f"Taste gedrückt: '{key}' (Hex: {hex_code})")
    except Exception as e:
        print(f"Fehler beim Drücken der Taste: {e}")


def on_release(key):
    """Verarbeitet das Loslassen einer Taste."""
    print(f"Taste losgelassen: {key}")
    # Programm beenden, wenn ESC gedrückt wird
    if key == keyboard.Key.esc:
        print("ESC gedrückt. Beenden...")
        return False

def main():
    print("Drücken Sie Tasten (ESC zum Beenden):")
    # Listener für Tastatureingaben starten
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()

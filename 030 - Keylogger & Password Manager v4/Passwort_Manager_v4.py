import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import json


class PasswordManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Password Manager")
        self.master.config(padx=50, pady=50)

        # Verschlüsselung Schlüssel Setup
        self.password = b"Yoda loves Milkshake"  # Sicheres Passwort für die Schlüsselgenerierung
        self.salt = b"C5H8NNaO4"                   # Salz sollte einzigartig sein
        self.key = self.generate_key()

        self.setup_ui()

    # ---------------------------- Schlüsselgenerierung ------------------------------- #
    def generate_key(self):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.password))
        return key

    # ---------------------------- Daten verschlüsseln ------------------------------- #
    def encrypt_data(self, data):
        f = Fernet(self.key)
        return f.encrypt(data.encode())

    # ---------------------------- Daten entschlüsseln ------------------------------- #
    def decrypt_data(self, encrypted_data):
        f = Fernet(self.key)
        return f.decrypt(encrypted_data).decode()

    # ---------------------------- Passwort generieren ------------------------------- #
    def generate_password(self):
        try:
            length = int(self.password_length_entry.get())
            if length < 1 or length > 50:
                raise ValueError("Passwortlänge muss zwischen 1 und 50 liegen.")
        except ValueError:
            messagebox.showerror("Ungültige Eingabe", "Bitte geben Sie eine gültige Passwortlänge (1-50) ein.")
            return

        # Dynamische Zeichen basierend auf Checkbutton-Auswahl
        characters = ""
        if self.use_letters.get():
            characters += string.ascii_letters
        if self.use_numbers.get():
            characters += string.digits
        if self.use_symbols.get():
            characters += string.punctuation

        if not characters:
            messagebox.showerror("Fehler", "Sie müssen mindestens eine Zeichentyp auswählen.")
            return

        # Passwort erstellen
        password = ''.join(random.choice(characters) for _ in range(length))
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        pyperclip.copy(password)
        messagebox.showinfo("Passwort generiert", "Ihr Passwort wurde generiert und kopiert!")

    # ---------------------------- Passwort speichern ------------------------------- #
    def save_password(self):
        website = self.website_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if len(website) == 0 or len(password) == 0:
            messagebox.showwarning(title="Fehler", message="Bitte füllen Sie alle Felder aus.")
            return

        try:
            new_data = {
                website: {
                    "email": email,
                    "password": password
                }
            }
            encrypted_data = self.encrypt_data(json.dumps(new_data))

            with open("passwords.json", "ab") as file:
                file.write(encrypted_data + b"\n")

            messagebox.showinfo("Erfolg", "Passwort erfolgreich gespeichert!")
            self.website_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern des Passworts: {e}")

    # ---------------------------- Passwort finden ------------------------------- #
    def find_password(self):
        website = self.website_entry.get()
        if len(website) == 0:
            messagebox.showwarning(title="Fehler", message="Bitte geben Sie eine Website ein.")
            return

        try:
            with open("passwords.json", "rb") as file:
                lines = file.readlines()

            for encrypted_line in lines:
                try:
                    decrypted_line = self.decrypt_data(encrypted_line).strip()
                    data = json.loads(decrypted_line)
                    if website in data:
                        email = data[website]["email"]
                        password = data[website]["password"]
                        self.email_entry.delete(0, tk.END)
                        self.email_entry.insert(0, email)
                        self.password_entry.delete(0, tk.END)
                        self.password_entry.insert(0, password)
                        return
                except Exception:
                    continue

            messagebox.showinfo("Nicht gefunden", f"Keine Details für {website} gefunden.")
        except FileNotFoundError:
            messagebox.showerror("Fehler", "Keine gespeicherten Passwörter gefunden!")

    # ---------------------------- Benutzeroberfläche einrichten ------------------------------- #
    def setup_ui(self):
        # Logo
        self.logo_img = tk.PhotoImage(file="logo.png")
        self.canvas = tk.Canvas(height=self.logo_img.height(), width=self.logo_img.width())
        self.canvas.create_image(self.logo_img.width() // 2, self.logo_img.height() // 2, image=self.logo_img)
        self.canvas.grid(row=0, column=1)

        # Labels
        tk.Label(self.master, text="Website:").grid(row=1, column=0, sticky="e")
        tk.Label(self.master, text="Email/Username:").grid(row=2, column=0, sticky="e")
        tk.Label(self.master, text="Password:").grid(row=3, column=0, sticky="e")
        tk.Label(self.master, text="Passwortlänge:").grid(row=4, column=0, sticky="e")

        # Eingabefelder
        self.website_entry = tk.Entry(self.master, width=35)
        self.website_entry.grid(row=1, column=1, columnspan=2, sticky="ew")
        self.website_entry.focus()

        self.email_entry = tk.Entry(self.master, width=35)
        self.email_entry.grid(row=2, column=1, columnspan=2, sticky="ew")

        self.password_entry = tk.Entry(self.master, width=35)
        self.password_entry.grid(row=3, column=1, columnspan=2, sticky="ew")

        # Passwortlänge und Checkboxen in einer Zeile
        self.password_length_entry = tk.Entry(self.master, width=5)
        self.password_length_entry.grid(row=4, column=1, sticky="w", padx=(0, 10))

        self.use_letters = tk.BooleanVar()
        tk.Checkbutton(self.master, text="Buchstaben", variable=self.use_letters).grid(row=4, column=1, sticky="e")

        self.use_numbers = tk.BooleanVar()
        tk.Checkbutton(self.master, text="Zahlen", variable=self.use_numbers).grid(row=4, column=2, sticky="w")

        self.use_symbols = tk.BooleanVar()
        tk.Checkbutton(self.master, text="Symbole", variable=self.use_symbols).grid(row=4, column=2, sticky="e")

        # Buttons in einer Reihe mit gleicher Größe
        button_width = 18
        tk.Button(self.master, text="Passwort generieren", command=self.generate_password, width=button_width).grid(
            row=6, column=0, pady=(10, 0))
        tk.Button(self.master, text="Passwort speichern", command=self.save_password, width=button_width).grid(
            row=6, column=1, pady=(10, 0))
        tk.Button(self.master, text="Passwort finden", command=self.find_password, width=button_width).grid(
            row=6, column=2, pady=(10, 0))

        # Spalten Gewichtung für gleichmäßige Verteilung
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManager(root)
    root.mainloop()

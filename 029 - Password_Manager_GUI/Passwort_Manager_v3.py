import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class PasswordManager:
    def __init__(self, master):
        self.master = master
        master.title("Password Manager")
        master.config(padx=50, pady=50)

        self.letters = string.ascii_letters
        self.numbers = string.digits
        self.symbols = string.punctuation

        # Encryption key setup
        self.password = b"your_secret_password"  # Change this to a secure password
        self.salt = b"your_salt"  # Change this to a unique salt
        self.key = self.generate_key()

        self.setup_ui()

    def generate_key(self):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.password))
        return key

    def encrypt_data(self, data):
        f = Fernet(self.key)
        return f.encrypt(data.encode())

    def decrypt_data(self, encrypted_data):
        f = Fernet(self.key)
        return f.decrypt(encrypted_data).decode()

    def generate_password(self):
        length = 12
        if self.password_strength.get() == "easy":
            password = ''.join(random.choice(self.letters + self.numbers) for _ in range(length))
        else:
            password = ''.join(random.choice(self.letters + self.numbers + self.symbols) for _ in range(length))

        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        pyperclip.copy(password)
        messagebox.showinfo("Password Generated", "Password has been generated and copied to clipboard!")

    def setup_ui(self):
        # Logo
        self.canvas = tk.Canvas(height=200, width=200)
        self.logo_img = tk.PhotoImage(file="logo.png")
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.grid(row=0, column=1, pady=(0, 20))

        # Labels
        tk.Label(text="Website:").grid(row=1, column=0, sticky="e")
        tk.Label(text="Email/Username:").grid(row=2, column=0, sticky="e")
        tk.Label(text="Password:").grid(row=3, column=0, sticky="e")

        # Entries and Buttons
        self.website_entry = tk.Entry(width=35)
        self.website_entry.grid(row=1, column=1, sticky="ew")
        self.website_entry.focus()

        self.search_button = tk.Button(text="Search", command=self.find_password)
        self.search_button.grid(row=1, column=2, sticky="ew")

        self.email_entry = tk.Entry(width=35)
        self.email_entry.grid(row=2, column=1, columnspan=2, sticky="ew")
        self.email_entry.insert(0, "your_email@example.com")

        self.password_entry = tk.Entry(width=21)
        self.password_entry.grid(row=3, column=1, sticky="ew")

        generate_password_button = tk.Button(text="Generate Password", command=self.generate_password)
        generate_password_button.grid(row=3, column=2, sticky="ew")

        add_button = tk.Button(text="Add Password", command=self.save_password)
        add_button.grid(row=4, column=1, columnspan=2, sticky="ew", pady=(10, 0))

        # Radio buttons
        self.password_strength = tk.StringVar(value="easy")
        tk.Radiobutton(text="Easy Password", value="easy", variable=self.password_strength).grid(row=5, column=1,
                                                                                                 sticky="w")
        tk.Radiobutton(text="Hard Password", value="hard", variable=self.password_strength).grid(row=5, column=2,
                                                                                                 sticky="e")

        # Configure column weights
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)

    def save_password(self):
        website = self.website_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if len(website) == 0 or len(password) == 0:
            messagebox.showwarning(title="Oops", message="Please make sure you haven't left any fields empty.")
        else:
            is_ok = messagebox.askokcancel(title="Confirm",
                                           message=f"These are the details entered: \nWebsite: {website}"
                                                   f"\nEmail: {email} \nPassword: {password} \nIs it ok to save?")
            if is_ok:
                try:
                    encrypted_data = self.encrypt_data(f"{website} | {email} | {password}")
                    with open("passwords.txt", "ab") as data_file:
                        data_file.write(encrypted_data + b"\n")
                    messagebox.showinfo(title="Success", message="Password saved successfully!")
                    self.website_entry.delete(0, tk.END)
                    self.password_entry.delete(0, tk.END)
                except IOError:
                    messagebox.showerror(title="Error", message="Failed to save password. Please try again.")

    def find_password(self):
        website = self.website_entry.get()
        if len(website) == 0:
            messagebox.showwarning(title="Oops", message="Please enter a website to search for.")
            return

        try:
            with open("passwords.txt", "rb") as data_file:
                encrypted_lines = data_file.readlines()

            for encrypted_line in encrypted_lines:
                decrypted_line = self.decrypt_data(encrypted_line.strip())
                stored_website, email, password = decrypted_line.split(" | ")
                if stored_website.lower() == website.lower():
                    self.email_entry.delete(0, tk.END)
                    self.email_entry.insert(0, email)
                    self.password_entry.delete(0, tk.END)
                    self.password_entry.insert(0, password)
                    return

            messagebox.showinfo(title="Not Found", message=f"No details for {website} exists.")
        except IOError:
            messagebox.showerror(title="Error", message="Failed to read passwords.")


if __name__ == "__main__":
    root = tk.Tk()
    password_manager = PasswordManager(root)
    root.mainloop()

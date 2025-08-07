import tkinter as tk
from tkinter import simpledialog, messagebox
from models import authenticate_admin

class LoginWindow(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Login:").grid(row=0)
        tk.Label(master, text="Hasło:").grid(row=1)
        self.username = tk.Entry(master)
        self.password = tk.Entry(master, show='*')
        self.username.grid(row=0, column=1)
        self.password.grid(row=1, column=1)
        return self.username

    def apply(self):
        if authenticate_admin(self.username.get(), self.password.get()):
            self.result = True
        else:
            messagebox.showerror("Błąd", "Nieprawidłowe dane")
            self.result = False

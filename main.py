import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import shutil
import os.path

def carica_impostazioni_luca():
    origine_profile = r"C:\Users\lucad\OneDrive\Documenti\Apex Settings\Luca\profile.cfg"
    origine_settings = r"C:\Users\lucad\OneDrive\Documenti\Apex Settings\Luca\settings.cfg"
    destinazione_profile = r"C:\Users\lucad\Saved Games\Respawn\Apex\profile\profile.cfg"
    destinazione_settings = r"C:\Users\lucad\Saved Games\Respawn\Apex\local\settings.cfg"

    file_mancanti = []

    if not os.path.exists(origine_profile) or not os.path.isfile(origine_profile):
        file_mancanti.append("'profile.cfg'")

    if not os.path.exists(origine_settings) or not os.path.isfile(origine_settings):
        file_mancanti.append("'settings.cfg'")

    if file_mancanti:
        messagebox.showerror("Errore", f"I seguenti file di origine non sono stati trovati: {', '.join(file_mancanti)}")
        return

    shutil.copyfile(origine_profile, destinazione_profile)
    shutil.copyfile(origine_settings, destinazione_settings)

    messagebox.showinfo("Avviso", "Impostazioni di Luca caricate con successo!")


def carica_impostazioni_matteo():
    origine_profile = r"C:\Users\lucad\OneDrive\Documenti\Apex Settings\Luca\profile.cfg"
    origine_settings = r"C:\Users\lucad\OneDrive\Documenti\Apex Settings\Luca\settings.cfg"
    destinazione_profile = r"C:\Users\lucad\Saved Games\Respawn\Apex\profile\profile.cfg"
    destinazione_settings = r"C:\Users\lucad\Saved Games\Respawn\Apex\local\settings.cfg"

    file_mancanti = []

    if not os.path.exists(origine_profile) or not os.path.isfile(origine_profile):
        file_mancanti.append("'profile.cfg'")

    if not os.path.exists(origine_settings) or not os.path.isfile(origine_settings):
        file_mancanti.append("'settings.cfg'")

    if file_mancanti:
        messagebox.showerror("Errore", f"I seguenti file di origine non sono stati trovati: {', '.join(file_mancanti)}")
        return

    shutil.copyfile(origine_profile, destinazione_profile)
    shutil.copyfile(origine_settings, destinazione_settings)

    messagebox.showinfo("Avviso", "Impostazioni di Luca caricate con successo!")



def aggiorna_file_origine():
    dialog = AccountDialog(finestra)
    account = dialog.result
    if account is not None:
        origine_profile = r"C:\Users\lucad\Saved Games\Respawn\Apex\profile\profile.cfg"
        origine_settings = r"C:\Users\lucad\Saved Games\Respawn\Apex\local\settings.cfg"
        destinazione = fr"""C:\Users\lucad\OneDrive\Documenti\Apex Settings\{account}\""""

        file_mancanti = []

        if not os.path.exists(origine_profile) or not os.path.isfile(origine_profile):
            file_mancanti.append("'profile.cfg'")

        if not os.path.exists(origine_settings) or not os.path.isfile(origine_settings):
            file_mancanti.append("'settings.cfg'")

        if file_mancanti:
            messagebox.showerror("Errore", f"I seguenti file di origine non sono stati trovati: {', '.join(file_mancanti)}")
            return

        shutil.copyfile(origine_profile, os.path.join(destinazione, "profile.cfg"))
        shutil.copyfile(origine_settings, os.path.join(destinazione, "settings.cfg"))

        messagebox.showinfo("Avviso", f"Impostazioni di {account} caricate con successo!")


class AccountDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Seleziona l'account a cui aggiornare le impostazioni").grid(row=0, column=0, padx=10, pady=10)
        self.result = None

    def buttonbox(self):
        box = tk.Frame(self)

        button_luca = tk.Button(box, text="Luca", width=10, command=self.choose_luca)
        button_luca.pack(side=tk.LEFT, padx=5, pady=10)

        button_matteo = tk.Button(box, text="Matteo", width=10, command=self.choose_matteo)
        button_matteo.pack(side=tk.LEFT, padx=5, pady=10)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def choose_luca(self):
        self.result = "Luca"
        self.ok()

    def choose_matteo(self):
        self.result = "Matteo"
        self.ok()

# Creazione della finestra principale
finestra = tk.Tk()
finestra.title("Apex settings changer")
finestra.geometry("300x200")  # Dimensioni della finestra (opzionale)

# Creazione dei bottoni
bottone_luca = tk.Button(finestra, text="Carica impostazioni Luca", command=carica_impostazioni_luca)
bottone_luca.pack(pady=20)  # Spaziatura dal bordo superiore (opzionale)

bottone_matteo = tk.Button(finestra, text="Carica impostazioni Matteo", command=carica_impostazioni_matteo)
bottone_matteo.pack()

bottone_aggiorna = tk.Button(finestra, text="Aggiorna file di origine", command=aggiorna_file_origine)
bottone_aggiorna.pack(pady=20)

# Avvio del ciclo di eventi della finestra
finestra.mainloop()

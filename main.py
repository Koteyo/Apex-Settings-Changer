import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import shutil
import os.path
import sys
import zipfile
import requests
import threading

# Definizione dei percorsi di base
base_dir = os.path.expanduser("~")
apex_settings_dir = os.path.join(base_dir, "OneDrive", "Documenti", "Apex Settings")
respawn_dir = os.path.join(base_dir, "Saved Games", "Respawn", "Apex")
profile_dir = os.path.join(respawn_dir, "profile")
local_dir = os.path.join(respawn_dir, "local")

def verifica_presenza_file(file_path):
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return False
    return True

def gestisci_copia_file(origine, destinazione):
    if verifica_presenza_file(origine):
        shutil.copyfile(origine, destinazione)
    else:
        messagebox.showerror("Errore", f"Il file di origine {origine} non è stato trovato")

def carica_impostazioni(nome):
    origine_profile = os.path.join(apex_settings_dir, nome, "profile.cfg")
    origine_settings = os.path.join(apex_settings_dir, nome, "settings.cfg")

    gestisci_copia_file(origine_profile, os.path.join(profile_dir, "profile.cfg"))
    gestisci_copia_file(origine_settings, os.path.join(local_dir, "settings.cfg"))

    messagebox.showinfo("Avviso", f"Impostazioni di {nome} caricate con successo!")

def aggiorna_file_origine():
    dialog = AccountDialog(finestra)
    account = dialog.result
    if account is not None:
        destinazione = os.path.join(apex_settings_dir, account)

        gestisci_copia_file(os.path.join(profile_dir, "profile.cfg"), os.path.join(destinazione, "profile.cfg"))
        gestisci_copia_file(os.path.join(local_dir, "settings.cfg"), os.path.join(destinazione, "settings.cfg"))

        messagebox.showinfo("Avviso", f"Impostazioni di {account} aggiornate con successo!")

def get_latest_release_info():
    api_url = "https://api.github.com/repos/Koteyo/Apex-Settings-Changer/releases/latest"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        latest_version = data.get("tag_name", "")
        assets = data.get("assets", [])
        download_url = assets[0].get("browser_download_url") if assets else None
        return latest_version, download_url
    except (requests.RequestException, KeyError):
        return None, None

def check_for_updates():
    current_version = "1.0.0"  # La tua versione corrente
    latest_version, download_url = get_latest_release_info()

    if latest_version and latest_version > current_version:
        messagebox.showinfo("Aggiornamento disponibile", f"È disponibile una nuova versione ({latest_version}).")
        threading.Thread(target=download_and_install_package, args=(download_url,)).start()

    else:
        messagebox.showinfo("Aggiornamento", "Il programma è aggiornato alla versione più recente.")

def download_and_install_package(download_url):
    if not download_url:
        messagebox.showerror("Errore", "URL di download non disponibile.")
        return

    try:
        response = requests.get(download_url)
        response.raise_for_status()

        # Specifica il percorso e il nome del file di destinazione
        destination_path = os.path.join(base_dir, "Downloads", "Apex_Settings_Changer.zip")

        with open(destination_path, "wb") as file:
            file.write(response.content)

        # Controlla se il file scaricato è un archivio ZIP valido
        if not zipfile.is_zipfile(destination_path):
            messagebox.showerror("Errore", "Il file scaricato non è un archivio ZIP valido.")
            return

        # Estrai il pacchetto ZIP nella cartella di destinazione
        extraction_path = os.path.join(base_dir, "Downloads", "Apex_Settings_Changer")
        with zipfile.ZipFile(destination_path, 'r') as zip_ref:
            zip_ref.extractall(extraction_path)

        # Trova il file eseguibile .exe all'interno dell'archivio
        exe_file = None
        for root, dirs, files in os.walk(extraction_path):
            for file in files:
                if file.endswith(".exe"):
                    exe_file = os.path.join(root, file)
                    break
            if exe_file:
                break

        if not exe_file:
            messagebox.showerror("Errore", "Nessun file .exe trovato nell'archivio ZIP.")
            return

        # Esegui l'applicazione
        os.startfile(exe_file)

    except requests.RequestException as e:
        messagebox.showerror("Errore", f"Errore durante il download: {e}")

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

class AccountDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Seleziona l'account a cui aggiornare le impostazioni").grid(row=0, column=0, padx=10, pady=10)
        self.result = None

    def buttonbox(self):
        box = tk.Frame(self)

        button_luca = tk.Button(box, text="Luca", width=10, command=lambda: self.choose_account("Luca"))
        button_luca.pack(side=tk.LEFT, padx=5, pady=10)

        button_matteo = tk.Button(box, text="Matteo", width=10, command=lambda: self.choose_account("Matteo"))
        button_matteo.pack(side=tk.LEFT, padx=5, pady=10)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def choose_account(self, account):
        self.result = account
        self.ok()

# Creazione della finestra principale
finestra = tk.Tk()
finestra.title("Apex settings changer")
finestra.geometry("300x300")  # Dimensioni della finestra (opzionale)

# Creazione dei bottoni
bottone_luca = tk.Button(finestra, text="Carica impostazioni Luca", command=lambda: carica_impostazioni("Luca"))
bottone_luca.pack(pady=20)  # Spaziatura dal bordo superiore (opzionale)

bottone_matteo = tk.Button(finestra, text="Carica impostazioni Matteo", command=lambda: carica_impostazioni("Matteo"))
bottone_matteo.pack()

bottone_aggiorna = tk.Button(finestra, text="Aggiorna file di origine", command=aggiorna_file_origine)
bottone_aggiorna.pack(pady=20)

# Creazione del pulsante di controllo degli aggiornamenti
bottone_aggiornamenti = tk.Button(finestra, text="Controlla gli aggiornamenti", command=check_for_updates)
bottone_aggiornamenti.pack(pady=20)

# Avvio del ciclo principale
finestra.mainloop()

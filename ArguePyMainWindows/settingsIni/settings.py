import configparser

import contextlib
default_settings = {
    "username": "",
    "language": "en",
    "projectPath": "",
    "lastProject": "",
    "recentProjects": [],
    "consoleFont": "Consolas",
    "consoleFontSize": 10,
    "consoleTextColor": "#ffffff",
    "consoleBackgroundColor": "#0a0a0a",
    "consoleTextColorError": "#f00a0a",
    "consoleTextColorWarning": "#dd5e30",
    "consoleTextColorSuccess": "#46dc78",
    "consoleTextColorInfo": "#5a3280",
    "consoleTextColorDebug": "#8c8cff",
}


class Settings:
    def __init__(self, filename):
        self.filename = filename
        self.config = configparser.ConfigParser()

    def load(self):
        # Carica le impostazioni dal file di configurazione, se esiste
        with contextlib.suppress(FileNotFoundError):
            with open(self.filename, "r") as f:
                self.config.read_file(f)
            print("Settings loaded from", self.filename)
            print("Settings:", self.config)

    def save(self):
        # Salva le impostazioni nel file di configurazione
        with open(self.filename, "w") as f:
            self.config.write(f)

    def get(self, key):
        # Restituisce il valore dell'impostazione specificata
        # Se l'impostazione non esiste, restituisce il valore di default
        try:
            return self.config.get("settings", key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return None

    def set(self, key, value):
        # Imposta il valore dell'impostazione specificata
        if "settings" not in self.config.sections():
            self.config.add_section("settings")
        self.config.set("settings", key, value)

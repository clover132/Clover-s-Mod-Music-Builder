import os
import json
import customtkinter as ctk
from tkinter import filedialog

class ModManager:
    def __init__(self):
        self.config_file = "config.json"
        
    def load_mod_path(self):
        """Intenta leer la ruta desde config.json. Retorna None si falla."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    data = json.load(f)
                    path = data.get("mod_path")
                    if path and os.path.exists(path):
                        return path
            except:
                pass
        return None

    def save_mod_path(self, path):
        """Guarda la ruta validada en config.json"""
        with open(self.config_file, "w") as f:
            json.dump({"mod_path": path}, f)

    def ask_for_directory(self):
        """Abre ventana para seleccionar carpeta y guarda la elección"""
        path = filedialog.askdirectory(title="Selecciona la carpeta RAÍZ de tu Mod (donde está metadata.xml)")
        if path:
            self.save_mod_path(path)
            return path
        return None
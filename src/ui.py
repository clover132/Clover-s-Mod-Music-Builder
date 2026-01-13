import customtkinter as ctk
from tkinterdnd2 import TkinterDnD
from tkinter import filedialog, messagebox # <--- IMPORTANTE: messagebox
import os
import sys

from src.xml_handler import MusicXMLHandler
from src.models import Track
from src.mod_manager import ModManager     # <--- IMPORTANTE
from src.file_handler import FileHandler   # <--- IMPORTANTE

def resource_path(relative_path):
    """ Obtiene la ruta absoluta al recurso, funcione como script o como exe frozen """
    try:
        # PyInstaller crea una carpeta temporal en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# ... (La clase SongRow se queda IGUAL, no la toques) ...
class SongRow(ctk.CTkFrame):
    def __init__(self, parent, track: Track):
        super().__init__(parent)
        self.track = track 
        
        # Configuración del Grid
        self.grid_columnconfigure(1, weight=1) 
        
        # --- ID y Nombre ---
        display_name = (track.name[:20] + '..') if len(track.name) > 20 else track.name
        self.lbl_info = ctk.CTkLabel(self, text=display_name, width=180, anchor="w", font=("Roboto", 12, "bold"))
        self.lbl_info.grid(row=0, column=0, rowspan=2, padx=10, pady=5)
        
        # --- ZONA DE ARCHIVOS ---
        self.files_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.files_frame.grid(row=0, column=1, sticky="ew", padx=5)
        
        # Labels (Intro y Loop)
        intro_color = "#858585" if track.intro else "#858585"
        intro_text = f"Intro: {os.path.basename(track.intro)}" if track.intro else "Intro: (Ninguno)"
        self.lbl_intro = ctk.CTkLabel(self.files_frame, text=intro_text, text_color=intro_color, font=("Arial", 10), anchor="w")
        self.lbl_intro.pack(fill="x")

        loop_text = f"Loop: {os.path.basename(track.path)}"
        self.lbl_loop = ctk.CTkLabel(self.files_frame, text=loop_text, text_color="white", font=("Arial", 11, "bold"), anchor="w")
        self.lbl_loop.pack(fill="x")
        
        # --- ZONA DE BOTONES ---
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.grid(row=0, column=2, padx=5)

        # 1. FILA DEL INTRO (Botón Seleccionar + Botón Borrar)
        self.intro_row = ctk.CTkFrame(self.buttons_frame, fg_color="transparent")
        self.intro_row.pack(pady=2)

        self.btn_intro = ctk.CTkButton(
            self.intro_row, 
            text="Intro", 
            width=50, 
            height=20, 
            fg_color="#555", 
            font=("Arial", 10), 
            command=self.on_change_intro
        )
        self.btn_intro.pack(side="left", padx=1)

        # EL BOTÓN NUEVO "X" PARA BORRAR INTRO
        self.btn_del_intro = ctk.CTkButton(
            self.intro_row, 
            text="✕", # Carácter X bonito
            width=20, 
            height=20, 
            fg_color="#C0392B", # Rojo oscuro
            hover_color="#E74C3C", # Rojo brillante al pasar mouse
            font=("Arial", 10, "bold"), 
            command=self.on_clear_intro
        )
        self.btn_del_intro.pack(side="left", padx=1)

        # 2. FILA DEL LOOP (Solo botón Loop)
        self.btn_loop = ctk.CTkButton(
            self.buttons_frame, 
            text="Loop", 
            width=75, # Un poco más ancho para llenar el espacio
            height=20, 
            fg_color="#c09670", 
            font=("Arial", 10), 
            command=self.on_change_loop
        )
        self.btn_loop.pack(pady=2)

    def on_change_intro(self):
        filename = filedialog.askopenfilename(
            title=f"Intro para {self.track.name}", 
            filetypes=[("Archivos OGG", "*.ogg"), ("Todos los archivos", "*.*")]
        )
        if filename:
            if not filename.lower().endswith(".ogg"):
                messagebox.showerror("Formato Incorrecto", f"El archivo no es .ogg válido.")
                return 
            
            self.track.intro = filename 
            self.lbl_intro.configure(text=f"Intro: {os.path.basename(filename)}", text_color="#42f5bf")

    def on_clear_intro(self):
        """Borra el intro de la memoria y actualiza la interfaz"""
        self.track.intro = None
        self.lbl_intro.configure(text="Intro: (Ninguno)", text_color="#858585")
        # No necesitamos borrar el archivo físico, simplemente al guardar el XML
        # ya no incluirá el atributo 'intro="..."'.

    def on_change_loop(self):
        filename = filedialog.askopenfilename(
            title=f"Loop para {self.track.name}", 
            filetypes=[("Archivos OGG", "*.ogg"), ("Todos los archivos", "*.*")]
        )
        if filename:
            if not filename.lower().endswith(".ogg"):
                messagebox.showerror("Formato Incorrecto", f"El archivo no es .ogg válido.")
                return 

            self.track.path = filename 
            self.lbl_loop.configure(text=f"Loop: {os.path.basename(filename)}", text_color="#42f5bf")

class MusicModApp(ctk.CTk, TkinterDnD.DnDWrapper):
    
    # HE COMBINADO TUS LISTAS AQUÍ.
    # Si quieres editar los Jefes, ¡tienen que estar en esta lista!
    TARGET_IDS = [
        1, 2, 3, 4, 5, 6, 7, 8, 
        9, 20, 21, 26, 27, 28,  # <--- Agregados los Jefes para que salgan en la UI
        10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 
        30, 31, 33, 34, 35, 36, 
        63, 102
    ]

    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)
        self.title("Clover's Mod Music Builder")
        self.geometry("900x600")
        ctk.set_appearance_mode("Dark")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        self.header = ctk.CTkFrame(self, height=50, fg_color="transparent")
        self.header.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        ctk.CTkLabel(self.header, text="Editor de Setlist", font=("Roboto", 22, "bold")).pack(side="left", padx=10)
        
        # --- CORRECCIÓN AQUÍ: AGREGADO command=self.on_save ---
        self.btn_save = ctk.CTkButton(self.header, text="Guardar", fg_color="#2b1d1c", width=120, command=self.on_save)
        self.btn_save.pack(side="right", padx=10)

        # Scroll Frame
        self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="Canciones Activas")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        self.tracks_data = [] 
        self.load_data()

    def load_data(self):
        handler = MusicXMLHandler()
        manager = ModManager()
        
        # 1. Intentar cargar la configuración existente
        mod_path = manager.load_mod_path()
        
        # --- NUEVA LÓGICA: PRIMERA VEZ ---
        if not mod_path:
            # Si es la primera vez (no hay config), pedimos la carpeta INMEDIATAMENTE
            messagebox.showinfo("Bienvenido", "Para comenzar, por favor selecciona la carpeta raíz del Mod.\n(Clover's Mod Music Builder)")
            mod_path = manager.ask_for_directory()
            
            if not mod_path:
                # Si el usuario le da a "Cancelar", cerramos la app o mostramos error
                messagebox.showerror("Error", "Es necesario seleccionar una carpeta de mod para continuar.\n")
                self.destroy() # Cierra la ventana
                return

        # 2. Definir rutas posibles
        ruta_xml_mod = os.path.join(mod_path, "resources", "music.xml")
        ruta_xml_interna = resource_path("music.xml") # La plantilla dentro del .exe
        
        target_xml = None
        source_type = ""

        # 3. Decidir qué cargar
        if os.path.exists(ruta_xml_mod):
            # CASO A: El usuario ya tiene un music.xml en su mod -> Lo editamos
            print(f"📂 Editando mod existente: {ruta_xml_mod}")
            target_xml = ruta_xml_mod
            source_type = "EXISTING"
        elif os.path.exists(ruta_xml_interna):
            # CASO B: Carpeta nueva/vacía -> Usamos la plantilla interna para empezar de cero
            print(f"✨ Creando nuevo mod (Usando plantilla interna)")
            target_xml = ruta_xml_interna
            source_type = "TEMPLATE"
        
        # 4. Parsear y Mostrar
        if target_xml:
            try:
                self.all_tracks = handler.parse(target_xml)
                
                # Si estamos usando la plantilla, reseteamos las rutas absolutas para evitar problemas
                # (Opcional, pero recomendado para limpieza)
                if source_type == "TEMPLATE":
                    for t in self.all_tracks:
                        t.path = os.path.basename(t.path) # Solo nombre de archivo
                        if t.intro: t.intro = os.path.basename(t.intro)

                # Filtrar IDs
                filtered_tracks = [t for t in self.all_tracks if t.id in self.TARGET_IDS]
                filtered_tracks.sort(key=lambda x: x.id)

                # Limpiar UI
                for widget in self.scroll_frame.winfo_children():
                    widget.destroy()

                # Generar filas
                for t in filtered_tracks:
                    row = SongRow(self.scroll_frame, t)
                    row.pack(fill="x", pady=2, padx=5)
                    
            except Exception as e:
                messagebox.showerror("Error Corrupto", f"No se pudo leer el archivo XML.\n{e}")
        else:
            messagebox.showerror("Error Crítico", "No se encontró la base de datos interna (music.xml).\nReinstala la aplicación.")

    def on_save(self):
        manager = ModManager()
        mod_path = manager.load_mod_path()
        
        if not mod_path:
            messagebox.showinfo("Configuración", "Primero selecciona la carpeta de tu Mod.")
            mod_path = manager.ask_for_directory()
            if not mod_path: return 

        copier = FileHandler()
        
        # --- CAMBIO CRÍTICO AQUÍ ---
        # Procesamos self.all_tracks (TODOS) en lugar de solo los visibles
        files_copied = copier.process_mod(self.all_tracks, mod_path)
        
        xml_writer = MusicXMLHandler()
        xml_dest = os.path.join(mod_path, "resources", "music.xml")
        
        # Guardamos TODOS
        success = xml_writer.write(self.all_tracks, xml_dest)
        
        if success:
            messagebox.showinfo("¡Éxito!", f"Mod actualizado.\n- Archivos nuevos copiados: {files_copied}\n- XML generado con {len(self.all_tracks)} canciones.")
        else:
            messagebox.showerror("Error", "Hubo un problema guardando el XML.")
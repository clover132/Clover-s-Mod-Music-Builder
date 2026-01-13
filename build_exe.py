import PyInstaller.__main__
import customtkinter
import tkinterdnd2
import os

# Obtener rutas de las librerías para incluirlas
ctk_path = os.path.dirname(customtkinter.__file__)
dnd_path = os.path.dirname(tkinterdnd2.__file__)
# Separador para Windows (;)
separator = ";"
print("Iniciando compilación de Clovers Mod Music Builder...")
print(f"CustomTkinter encontrado en: {ctk_path}")
args = [
    'main.py',                        # Tu archivo principal
    '--name=CloversModMusicBuilder', # Nombre del archivo .exe final
    '--onefile',                      # Empaquetar todo en un solo archivo
    '--noconsole',                    # No mostrar la ventana negra de comandos (terminal)
    '--clean',                        # Limpiar caché de compilaciones anteriores
    
    f'--add-data={ctk_path}{separator}customtkinter',
    f'--add-data={dnd_path}{separator}tkinterdnd2',
    f'--add-data=src/splash.png{separator}src',
    '--icon=assets/app.ico',
]

# Ejecutar la compilación
try:
    PyInstaller.__main__.run(args)
    print("\n ¡Compilación exitosa! Busca tu archivo en la carpeta 'dist'.")
except Exception as e:
    print(f"\n Error durante la compilación: {e}")
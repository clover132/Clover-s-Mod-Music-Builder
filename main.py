# main.py
from src.ui import MusicModApp
from src.splash_screen import show_splash_screen

if __name__ == "__main__":
    # 1. PRIMERO: Mostrar la pantalla de carga
    show_splash_screen()
    # 2. DESPUÉS: Iniciar la aplicación principal
    app = MusicModApp()
    app.mainloop()
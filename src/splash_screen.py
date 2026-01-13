import customtkinter as ctk
from PIL import Image
import os

def show_splash_screen():
    """
    Muestra una ventana de carga sin bordes con una imagen durante 3 segundos.
    """
    # Configuración básica
    splash_root = ctk.CTk()
    splash_root.overrideredirect(True) # QUITA los bordes y la barra de título (importante)
    
    # --- 1. Cargar la Imagen ---
    # Asumimos que splash.png está en la misma carpeta 'src' que este script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(current_dir, "splash.png")

    try:
        pil_image = Image.open(img_path)
        
        # --- CAMBIO AQUÍ ---
        # En lugar de leer el tamaño de la imagen:
        # w, h = pil_image.size 
        
        # Define tú mismo el tamaño que quieras:
        w, h = 400, 400 
        
        # Esto redimensiona la imagen visualmente para que quepa en ese tamaño
        ctk_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(w, h))
    except FileNotFoundError:
        print(f"Error: No se encontró {img_path}")
        # Si falla, creamos una ventana pequeñita y salimos rápido
        splash_root.geometry("200x100")
        ctk.CTkLabel(splash_root, text="Cargando...").pack()
        splash_root.after(1000, splash_root.destroy)
        splash_root.mainloop()
        return

    # --- 2. Centrar la Ventana en la Pantalla ---
    ws = splash_root.winfo_screenwidth()
    hs = splash_root.winfo_screenheight()
    # Calculamos la posición X e Y para que quede centrada
    x = int((ws/2) - (w/2))
    y = int((hs/2) - (h/2))
    splash_root.geometry(f'{w}x{h}+{x}+{y}')

    # --- 3. Mostrar la Imagen ---
    # Usamos un label que ocupa toda la ventana para mostrar la imagen
    label = ctk.CTkLabel(splash_root, text="", image=ctk_image)
    label.pack(expand=True, fill="both")

    # --- 4. Programar el cierre ---
    # .after(milisegundos, funcion_a_ejecutar)
    # 3000 ms = 3 segundos
    splash_root.after(3000, splash_root.destroy)
    
    # Iniciar el bucle de esta ventana temporal
    splash_root.mainloop()
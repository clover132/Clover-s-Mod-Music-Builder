import customtkinter as ctk
from PIL import Image
import os

def show_splash_screen():
    """
    Muestra una ventana de carga sin bordes con una imagen durante 3 segundos.
    """
    # Configuración básica
    splash_root = ctk.CTk()
    splash_root.overrideredirect(True) 
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(current_dir, "splash.png")

    try:
        pil_image = Image.open(img_path)

        w, h = 400, 400 
        
        ctk_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(w, h))
    except FileNotFoundError:
        print(f"Error: No se encontró {img_path}")
        splash_root.geometry("200x100")
        ctk.CTkLabel(splash_root, text="Cargando...").pack()
        splash_root.after(1000, splash_root.destroy)
        splash_root.mainloop()
        return

    ws = splash_root.winfo_screenwidth()
    hs = splash_root.winfo_screenheight()
    x = int((ws/2) - (w/2))
    y = int((hs/2) - (h/2))
    splash_root.geometry(f'{w}x{h}+{x}+{y}')

    label = ctk.CTkLabel(splash_root, text="", image=ctk_image)
    label.pack(expand=True, fill="both")




    splash_root.after(3000, splash_root.destroy)
    



    splash_root.mainloop()
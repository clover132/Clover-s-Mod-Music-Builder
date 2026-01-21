from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class SubLayer:
    path: str
    mul: float = 1.0  # Volumen por defecto
    name: Optional[str] = None # A veces útil para debug

# --- Estructura Principal para <track> ---
@dataclass
class Track:
    def __init__(self, id, name, path, intro=None, loop="true", **kwargs):
        # 1. Aseguramos que el ID sea un ENTERO (int)
        # Si llega como texto "1", lo convertimos a número 1.
        try:
            self.id = int(id)
        except ValueError:
            self.id = 9999  # Fallback por si el ID no es número

        self.name = name
        self.path = path
        self.intro = intro
        self.loop = loop
        
        # 2. Guardamos los extras (layermode, etc.)
        self.extra_attributes = kwargs 

    # --- MAGIA PARA EVITAR ERRORES EN LA UI ---
    def __getattr__(self, name):
        # Intentar buscar en los atributos extra
        if name in self.extra_attributes:
            return self.extra_attributes[name]
        
        # Si el nombre tiene guion bajo (ej: layer_mode) pero en el XML
        # viene junto (layermode), intentamos buscarlo quitando el guion.
        simple_name = name.replace("_", "")
        if simple_name in self.extra_attributes:
            return self.extra_attributes[simple_name]
            
        # Si no existe, devolvemos None en vez de lanzar error
        return None

    def __repr__(self):
        return f"Track({self.id}, {self.name})"
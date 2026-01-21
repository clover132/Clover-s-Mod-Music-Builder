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
        # 1. Datos que nuestra App NECESITA leer y editar
        self.id = id
        self.name = name
        self.path = path
        self.intro = intro
        
        # 2. Datos críticos que debemos preservar pero quizás no editamos siempre
        self.loop = loop  # Por defecto "true" para evitar el silencio
        
        # 3. El "Bolsillo Mágico": Aquí guardamos todo lo demás.
        # layermode, layerfadespeed, volume, y cosas que ni conocemos.
        # **kwargs captura cualquier atributo extra que venga del XML.
        self.extra_attributes = kwargs

    def __repr__(self):
        return f"Track({self.id}, {self.name})"
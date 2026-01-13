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
    # 1. Identificadores Obligatorios
    id: int
    name: str          # El nombre legible (ej: "Basement")
    
    # 2. Archivos de Audio Principales
    path: str          # El loop principal
    intro: Optional[str] = None  # La intro (si tiene)
    loop: bool = True
    
    # 3. Control de Volumen
    mul: float = 1.0   # Multiplicador de volumen global
    
    # 4. Atributos de Capas (Inline - Cuando la capa se define en la misma linea)
    layer_path: Optional[str] = None 
    layer_intro: Optional[str] = None
    layer_mul: float = 1.0
    
    # 5. Configuración de Mezcla
    layer_mode: int = 1         # 1=Normal, 2=Capas dinámicas
    layer_fade_speed: float = 1.0 # Velocidad de transición entre capas
    
    # 6. Sub-Capas (Nodos hijos)
    sub_layers: List[SubLayer] = field(default_factory=list)

    def __post_init__(self):
        """
        Este método se ejecuta automáticamente después del constructor.
        Sirve para validar datos o convertir tipos si es necesario.
        """
        # ID sea siempre un entero
        self.id = int(self.id)
import xml.etree.ElementTree as ET
from typing import List, Optional
# Importamos las clases que definimos en el paso anterior
from src.models import Track, SubLayer

class MusicXMLHandler:
    def parse(self, xml_path: str) -> List[Track]:
        """
        Lee el archivo XML y devuelve una lista de objetos Track.
        """
        tracks_found = []

        try:
            # 1. Cargar el árbol DOM en memoria
            tree = ET.parse(xml_path)
            root = tree.getroot()

            # 2. Buscar todas las etiquetas <track>
            # Es como un foreach en C++
            for element in root.findall('track'):
                
                # --- Extracción de Datos Segura ---
                # Usamos .get() que devuelve None si el atributo no existe.
                # Es vital convertir tipos (str -> int/float/bool) aquí.
                
                # Conversión de Booleano (XML usa "true"/"false" texto)
                is_loop = element.get('loop', 'true').lower() == 'true'
                
                # Creación del Objeto Principal
                track = Track(
                    id=int(element.get('id')), # Obligatorio
                    name=element.get('name'),  # Obligatorio
                    path=element.get('path'),  # Obligatorio
                    loop=is_loop,
                    
                    # Opcionales (si no existen, pasan como None o su default)
                    intro=element.get('intro'),
                    mul=float(element.get('mul', 1.0)),
                    
                    # Lógica de Capas (Inline)
                    layer_path=element.get('layer'),
                    layer_intro=element.get('layerintro'),
                    layer_mul=float(element.get('layermul', 1.0)),
                    
                    # Configuración avanzada
                    layer_mode=int(element.get('layermode', 1)),
                    layer_fade_speed=float(element.get('layerfadespeed', 1.0))
                )

                # 3. Detección de Sub-Capas (Nodos Hijos)
                # Buscamos si dentro de este <track> hay etiquetas <layer>
                # Ejemplo: The Beast o Dogma en tu archivo
                for child_layer in element.findall('layer'):
                    sub = SubLayer(
                        path=child_layer.get('path'),
                        mul=float(child_layer.get('mul', 1.0)),
                        name=child_layer.get('name')
                    )
                    # Agregamos la sub-capa a la lista del track padre
                    track.sub_layers.append(sub)

                # Añadimos el track completo a la lista maestra
                tracks_found.append(track)

            return tracks_found

        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {xml_path}")
            return []
        except ET.ParseError:
            print(f"Error: El archivo {xml_path} tiene errores de sintaxis (tags mal cerrados).")
            return []
        except Exception as e:
            print(f"Error desconocido al leer XML: {e}")
            return []

# ... (El método parse se queda igual arriba) ...

    def write(self, tracks: List[Track], output_path: str):
        """
        Convierte la lista de objetos Track a un archivo music.xml físico.
        """
        # 1. Crear el nodo raíz
        root = ET.Element("music")
        root.set("root", "music/") # Añadimos el atributo root="music/" que tenías original
        
        # 2. Iterar sobre cada objeto Track
        for track in tracks:
            # Creamos la etiqueta <track>
            t_node = ET.SubElement(root, "track")
            
            # Asignamos atributos OBLIGATORIOS
            t_node.set("id", str(track.id))
            t_node.set("name", track.name)
            
            # NOTA IMPORTANTE:
            # Aquí guardamos solo el nombre del archivo, no la ruta completa de Windows.
            # Ejemplo: Guardamos "Metallica.ogg", NO "C:/Users/Mateo/Downloads/Metallica.ogg"
            # Nos aseguramos de usar forward slash (/) por si acaso
            #clean_path = track.path.replace("\\", "/").split("/")[-1]
            #t_node.set("path", clean_path)
            
            t_node.set("path", track.path.replace("\\", "/"))
            
            # Asignamos atributos OPCIONALES (Solo si existen)
            if track.intro:
                t_node.set("intro", track.intro.replace("\\", "/"))
                
            if track.mul != 1.0:
                t_node.set("mul", str(track.mul))
                
            # Atributos de capas complejas (Inline)
            if track.layer_path:
                t_node.set("layer", track.layer_path)
            if track.layer_mode != 1:
                t_node.set("layermode", str(track.layer_mode))
                
            # 3. Generar Sub-Capas (Hijos) <layer>
            # Para jefes como The Beast o Dogma
            for sub in track.sub_layers:
                l_node = ET.SubElement(t_node, "layer")
                l_node.set("path", sub.path)
                if sub.mul != 1.0:
                    l_node.set("mul", str(sub.mul))

        # 4. Escribir el archivo final bonito (Indentado)
        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0) # Esto hace que el XML sea legible y no una sola línea
        
        try:
            tree.write(output_path, encoding="UTF-8", xml_declaration=False)
            print(f"✅ XML generado exitosamente en: {output_path}")
            return True
        except Exception as e:
            print(f"❌ Error escribiendo XML: {e}")
            return False
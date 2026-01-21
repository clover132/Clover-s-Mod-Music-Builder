import xml.etree.ElementTree as ET
import os
from src.models import Track

class MusicXMLHandler:
    def parse(self, xml_path):
        if not os.path.exists(xml_path):
            raise FileNotFoundError(f"No se encontró el archivo: {xml_path}")
        
        tree = ET.parse(xml_path)
        root = tree.getroot()
        tracks = []
        
        for child in root.findall("track"):
            # 1. Copiamos TODOS los atributos que tenga la línea del XML
            attrs = child.attrib.copy()
            
            # 2. Extraemos ("pop") los atributos que nuestra App conoce y maneja.
            # Al hacer .pop(), se guardan en la variable y SE BORRAN del diccionario 'attrs'.
            t_id = attrs.pop("id", None)
            t_name = attrs.pop("name", "Unknown")
            t_path = attrs.pop("path", "")
            t_intro = attrs.pop("intro", None)
            
            # El loop es vital. Si no viene, asumimos "true" para que no haya silencio.
            t_loop = attrs.pop("loop", "true") 
            
            if t_id is not None:
                # 3. Pasamos lo que sobro en 'attrs' (ej: layermode) como **kwargs
                track = Track(t_id, t_name, t_path, t_intro, t_loop, **attrs)
                tracks.append(track)
                
        return tracks

    def save(self, tracks, output_path):
        root = ET.Element("music", root="music/")
        
        # Ordenamos los tracks por ID numérico para que el XML quede limpio y ordenado
        # Usamos una lambda segura por si algún ID no es número
        tracks.sort(key=lambda t: int(t.id) if str(t.id).isdigit() else 9999)
        
        for track in tracks:
            track_elem = ET.SubElement(root, "track")
            
            # --- Escribir atributos ESTÁNDAR ---
            track_elem.set("id", str(track.id))
            track_elem.set("name", track.name)
            
            if track.path:
                track_elem.set("path", track.path)
            if track.intro:
                track_elem.set("intro", track.intro)
            
            # --- Escribir LOOP (Crítico) ---
            # Si track.loop es True booleano, lo convertimos a string "true"
            loop_val = str(track.loop).lower() 
            track_elem.set("loop", loop_val)
            # Aquí devolvemos layermode, volume, etc. al archivo
            for key, value in track.extra_attributes.items():
                track_elem.set(key, str(value))
        
        # Formatear \\(Indentación)
        self._indent(root)
        tree = ET.ElementTree(root)
        tree.write(output_path, encoding="UTF-8", xml_declaration=False)

    def _indent(self, elem, level=0):
        """Función auxiliar para que el XML no quede en una sola línea fea"""
        i = "\n" + level * "    "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "    "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for child in elem:
                self._indent(child, level + 1)
            if not child.tail or not child.tail.strip():
                child.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
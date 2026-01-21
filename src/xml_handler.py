import xml.etree.ElementTree as ET
import os
from src.models import Track

class MusicXMLHandler:
    def parse(self, xml_path):
        if not os.path.exists(xml_path):
            return [] # Retorna lista vacía en vez de error si no hay archivo
        
        tree = ET.parse(xml_path)
        root = tree.getroot()
        tracks = []
        
        for child in root.findall("track"):
            attrs = child.attrib.copy()
            
            t_id = attrs.pop("id", None)
            t_name = attrs.pop("name", "Unknown")
            t_path = attrs.pop("path", "")
            t_intro = attrs.pop("intro", None)
            t_loop = attrs.pop("loop", "true") 
            
            if t_id is not None:
                # Pasamos el resto de atributos (layermode, volume) como kwargs
                track = Track(t_id, t_name, t_path, t_intro, t_loop, **attrs)
                tracks.append(track)
                
        # Ordenamos por ID numérico para que la UI los muestre en orden (1, 2, 3...)
        tracks.sort(key=lambda x: x.id)
        return tracks

    def write(self, tracks, output_path):
        root = ET.Element("music", root="music/")
        
        # Aseguramos orden antes de guardar
        tracks.sort(key=lambda x: x.id)
        
        for track in tracks:
            track_elem = ET.SubElement(root, "track")
            
            track_elem.set("id", str(track.id))
            track_elem.set("name", track.name)
            
            if track.path:
                track_elem.set("path", track.path)
            if track.intro:
                track_elem.set("intro", track.intro)
            
            # Loop
            loop_val = str(track.loop).lower()
            track_elem.set("loop", loop_val)
            
            # Extras: Escribimos todo lo que haya en extra_attributes
            for key, value in track.extra_attributes.items():
                track_elem.set(key, str(value))
        
        self._indent(root)
        tree = ET.ElementTree(root)
        tree.write(output_path, encoding="UTF-8", xml_declaration=False)

        return True

    def _indent(self, elem, level=0):
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
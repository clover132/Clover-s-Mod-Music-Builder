import os
import shutil
from typing import List
from src.models import Track

class FileHandler:
    BOSS_IDS = [9,20,21,26,27,28]

    def process_mod(self, tracks: List[Track], mod_root_path: str):
        """
        Recorre los tracks, copia los archivos nuevos a la carpeta del mod
        y actualiza las rutas relativas para el XML.
        """
        base_music_dir = os.path.join(mod_root_path, "resources", "music")
        fights_dir = os.path.join(base_music_dir, "Fights")
        
        os.makedirs(base_music_dir, exist_ok=True)
        os.makedirs(fights_dir, exist_ok=True)

        count = 0

        for track in tracks:
            if os.path.isabs(track.path):
                relative_path = self._copy_file(track.path, track.id, base_music_dir, fights_dir)
                if relative_path:
                    track.path = relative_path # Actualizamos el objeto con la ruta relativa
                    count += 1

            if track.intro and os.path.isabs(track.intro):
                relative_path = self._copy_file(track.intro, track.id, base_music_dir, fights_dir)
                if relative_path:
                    track.intro = relative_path
        
        return count

    def _copy_file(self, source_path, track_id, base_dir, fights_dir):
        if not source_path.endswith(".ogg"):
            return None
        
        filename = os.path.basename(source_path)
        
        if track_id in self.BOSS_IDS:
            dest_folder = fights_dir
            relative_prefix = "Fights/"
        else:
            dest_folder = base_dir
            relative_prefix = "" 

        dest_path = os.path.join(dest_folder, filename)
        abs_source = os.path.abspath(source_path)
        abs_dest = os.path.abspath(dest_path)
        if abs_source == abs_dest:
            print(f" Archivo reutilizado (no se copia): {filename}")
            return f"{relative_prefix}{filename}"
        try:
            shutil.copy2(source_path, dest_path)
            return f"{relative_prefix}{filename}"
        except Exception as e:
            print(f" Error copiando {filename}: {e}")
            return None
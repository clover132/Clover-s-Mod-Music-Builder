# 🎵 Isaac Music Builder (Repentance)

![Version](https://img.shields.io/badge/version-1.0%20Beta-blue) ![Python](https://img.shields.io/badge/Built%20with-Python%20%26%20CustomTkinter-yellow)

Una herramienta moderna y visual para gestionar y modificar la música en **The Binding of Isaac: Repentance/Repentance+**.

<img width="1113" height="785" alt="isaac_screen_mod_builder" src="https://github.com/user-attachments/assets/305f75e5-11e2-45ff-b0e8-7345c3fe1142" />

## ✨ Características

* **Interfaz Moderna:** GUI oscura y limpia
* **Seleccion archivos:** Drag & Drop: (Próximamente) 
* **Gestión Inteligente de Audio:**
    * Soporte completo para **Intro + Loop**.
    * Validación automática de archivos `.ogg`.
* **Portable:** Genera un archivo `music.xml` limpio y una estructura de carpetas lista para subir a la Workshop tu paquete de musica **(Opcional)**.

## 🚀 Instalación (Para Usuarios)

1.  Ve a la sección de **[Releases](../../releases)** de este repositorio.
2.  Descarga el archivo `CloversModMusicBuilder.exe`.
3.  Colócalo en una carpeta vacía en tu escritorio.
4.  Ejecútalo y sigue las instrucciones para seleccionar la carpeta del Mod.

## 🛠️ Instalación (Para Desarrolladores)

Si quieres contribuir al código o ejecutarlo desde Python:

1.  Clona el repositorio:
    ```bash
    git clone https://github.com/clover132/Clover-s-Mod-Music-Builder.git
    ```
2.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
3.  Ejecuta la aplicación:
    ```bash
    python main.py
    ```

## 📦 Cómo Compilar (.exe)

Para generar el ejecutable tú mismo:

```bash
python build_exe.py

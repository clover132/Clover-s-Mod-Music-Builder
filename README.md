# 🎵 Isaac Music Builder (Repentance)

![Version](https://img.shields.io/badge/version-1.0%20Beta-blue) ![Python](https://img.shields.io/badge/Built%20with-Python%20%26%20CustomTkinter-yellow)

Una herramienta moderna y visual para gestionar y crear mods de música para **The Binding of Isaac: Repentance**. Olvídate de editar archivos XML a mano o renombrar carpetas.

Desarrollado por **Clover (Mateo)**.

![Screenshot](src/splash.png)
*(Aquí podrías poner una captura de la interfaz más adelante)*

## ✨ Características

* **Interfaz Moderna:** GUI oscura y limpia basada en CustomTkinter.
* **Drag & Drop:** (Próximamente) Soporte para arrastrar archivos.
* **Gestión Inteligente de Audio:**
    * Soporte completo para **Intro + Loop**.
    * Validación automática de archivos `.ogg`.
* **Ruteo Automático:** Detecta si la canción es para un Jefe y la mueve automáticamente a la carpeta `Fights/`.
* **Portable:** Genera un archivo `music.xml` limpio y una estructura de carpetas lista para subir a la Workshop.

## 🚀 Instalación (Para Usuarios)

1.  Ve a la sección de **[Releases](../../releases)** de este repositorio.
2.  Descarga el archivo `IsaacMusicModder.exe`.
3.  Colócalo en una carpeta vacía en tu escritorio.
4.  Ejecútalo y sigue las instrucciones para seleccionar la carpeta de tu Mod.

## 🛠️ Instalación (Para Desarrolladores)

Si quieres contribuir al código o ejecutarlo desde Python:

1.  Clona el repositorio:
    ```bash
    git clone [https://github.com/TU_USUARIO/IsaacMusicBuilder.git](https://github.com/TU_USUARIO/IsaacMusicBuilder.git)
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
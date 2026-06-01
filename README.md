
# 🎵 MusicDownloader

![Estado](https://img.shields.io/badge/Estado-v1.0%20Released-brightgreen?style=for-the-badge&logo=github)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

**MusicDownloader** es una aplicación web creada con **Python** y **Streamlit** que permite descargar música de YouTube Music de forma personalizada y controlada.

---

## 🎉 Primera versión disponible

La **v1.0** ya está operativa. Incluye descarga de canciones individuales y álbumes completos, editor de metadatos ID3, portada personalizada, recorte de audio y acceso directo en el escritorio generado automáticamente al primer arranque.

---

## ✨ Características

* 🛠️ **Control Manual:** Tú introduces los metadatos (Artista, Álbum, Título) para que la librería esté a tu gusto.
* 🖼️ **Portada Personalizada:** Sube o selecciona la imagen de portada que prefieras.
* 💿 **Modo Álbum:** Descarga un álbum entero manteniendo los datos comunes y cambiando solo lo necesario por canción.
* ✂️ **Recorte de Audio:** Escucha la canción descargada y recorta el inicio o el final antes de guardarla.
* 🔗 **Integración con YouTube Music:** Solo necesitas el enlace de la canción o del vídeo.
* ⚙️ **Motores de descarga:** Utiliza **yt-dlp** para obtener el audio y **FFmpeg** para el procesado y la incrustación de metadatos.

---

## 🚀 Instalación y primer arranque

### 1. Clonar el repositorio

```bash
git clone https://github.com/RMTorrabadella04/MusicDownloader.git
cd MusicDownloader
```

### 2. Configurar el entorno

Copia el archivo de ejemplo y rellena la ruta donde quieres que se guarden las canciones:

```bash
copy .env.example .env
```

Abre `.env` y edita la línea `OUTPUT_DIR`:

```env
OUTPUT_DIR=C:/Users/TuNombre/Music
```

### 3. Arrancar la app

Haz doble clic en **`MusicDL.bat`** — instala las dependencias si es necesario, lanza el servidor y abre la app en el navegador automáticamente.

> La primera vez que arranques se creará un acceso directo en el Escritorio para futuros usos.

---

## 🛠️ Requisitos técnicos

* **Python 3.11+**
* **FFmpeg** instalado y en el PATH del sistema ([descarga aquí](https://ffmpeg.org/download.html))
* El resto de dependencias Python se instalan automáticamente desde `requirement.txt`

---

## 📁 Estructura del proyecto

```
MusicDownloader/
├── app/
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── album_tab.py    # Tab de álbum completo
│   │   ├── cover_panel.py  # Panel de portada
│   │   ├── log_panel.py    # Consola de log
│   │   ├── single_tab.py   # Tab de canción individual
│   │   └── trim_panel.py   # Panel de recorte de audio
│   ├── __init__.py
│   ├── audio.py            # Descarga (yt-dlp) y metadatos (ffmpeg)
│   ├── config.py           # Variables de entorno y constantes
│   ├── shortcut.py         # Generación del acceso directo
│   ├── state.py            # Estado de la sesión
│   ├── styles.py           # CSS de la interfaz
│   └── utils.py            # Funciones auxiliares
├── images/
│   ├── icono.png
│   ├── icono.ico
│   └── temp/               # Portadas temporales (se limpian automáticamente)
├── temp/           # MP3 temporales durante la descarga (se limpian automáticamente)
├── .env                    # Tu configuración local (no se sube a Git, la tienes que crear tu)
├── .env.example            # Plantilla de configuración
├── main.py                 # Entry point
└── MusicDL.bat             # Lanzador de la app
```

---

*Nota: Este proyecto requiere tener FFmpeg configurado correctamente en el PATH del sistema.*

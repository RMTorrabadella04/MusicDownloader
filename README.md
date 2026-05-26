# 🎵 MusicDownloader

![Estado](https://img.shields.io/badge/Estado-En%20Desarrollo-orange?style=for-the-badge&logo=github)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

**MusicDownloader** es una aplicación web creada con **Python** y **Streamlit** que permite descargar música de YouTube Music de forma personalizada y controlada.

## 🚧 Estado del Proyecto
Actualmente en desarrollo. El objetivo es ofrecer una herramienta **semi-automática** donde el usuario tenga el control total sobre la estética y la información del archivo final.

## ✨ Características
- 🛠️ **Control Manual:** Tú introduces los metadatos (Artista, Álbum, Título) para que la librería esté a tu gusto.
- 🖼️ **Portada Personalizada:** Sube o descarga la imagen de portada que prefieras para el archivo.
- 🔗 **Integración con YouTube Music:** Solo necesitas el enlace de la canción.
- ⚙️ **Motores de descarga:** Utiliza **yt-dlp** para obtener el audio y **FFmpeg** para el procesado y la unión de metadatos.

## 🛠️ Requisitos técnicos
* **Python 3.x**
* **Streamlit** (para la interfaz web)
* **yt-dlp** (para la descarga)
* **FFmpeg** (instalado en el sistema para la conversión de audio)

## 🚀 Flujo de uso
1. **Enlace:** Pegas el link de YouTube Music.
2. **Imagen:** Subes o seleccionas la foto de la portada.
3. **Metadatos:** Rellenas manualmente la información de la canción (Título, Artista, etc.).
4. **Descarga:** La app procesa todo y te entrega el archivo listo para tu reproductor.

---
*Nota: Este proyecto requiere tener FFmpeg configurado correctamente en el PATH del sistema.*

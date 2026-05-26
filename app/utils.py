import streamlit as st
import re
import time
from pathlib import Path
import validators

# ══════════════════════════════════════════════════════════════════
#  HELPERS — CORE
# ══════════════════════════════════════════════════════════════════
def add_log(msg: str, level: str = "ok"):
    ts = time.strftime("%H:%M:%S")
    st.session_state.download_log.append((ts, level, msg))
    if len(st.session_state.download_log) > 200:
        st.session_state.download_log = st.session_state.download_log[-200:]

def sanitize_filename(name: str) -> str:
    """Remove characters illegal in filenames."""
    return re.sub(r'[<>:"/\\|?*]', "_", name).strip()

def build_filename(artist: str, title: str) -> str:
    """
    Construye el nombre de archivo en el formato:
      [ARTISTA] - [TITULO].mp3
      [ARTISTA 1], [ARTISTA 2] - [TITULO].mp3
    """
    artist_safe = sanitize_filename(artist.strip()) if artist.strip() else "Desconocido"
    title_safe  = sanitize_filename(title.strip())  if title.strip()  else "Sin titulo"
    return f"{artist_safe} - {title_safe}.mp3"

def validate_yt_url(url: str) -> tuple[bool, str]:
    """Return (is_valid, message)."""
    if not url.strip():
        return False, "URL vacía"
    if not validators.url(url):
        return False, "URL con formato inválido"
    if not any(d in url for d in ["youtube.com", "youtu.be", "music.youtube.com"]):
        return False, "No parece una URL de YouTube"
    return True, "OK"

def ensure_output_dir(path: str) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p

def get_audio_duration(mp3_path: str) -> float:
    """Return duration in seconds using moviepy."""
    try:
        from moviepy import AudioFileClip
        with AudioFileClip(mp3_path) as clip:
            return clip.duration
    except Exception:
        return 0.0

def seconds_to_hms(s: float) -> str:
    s = int(s)
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{sec:02d}"
    return f"{m:02d}:{sec:02d}"
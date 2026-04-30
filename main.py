"""
MusicDL — YouTube Music Downloader with Metadata Editor
Streamlit App · Dark Vinyl Aesthetic
"""

import streamlit as st
import subprocess
import os
import sys
import shutil
import platform
import tempfile
import re
import time
from pathlib import Path
from dotenv import load_dotenv
import validators

# Carga el .env desde la raíz del proyecto (antes de cualquier otra cosa)
_ENV_FILE = Path(__file__).parent / ".env"
load_dotenv(_ENV_FILE)

# ══════════════════════════════════════════════════════════════════
#  PAGE CONFIG  (must be the VERY FIRST Streamlit call)
# ══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="MusicDL",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════
#  CONSTANTS  —  rutas resueltas desde .env
# ══════════════════════════════════════════════════════════════════
PROJECT_ROOT     = Path(__file__).parent
FIRST_RUN_MARKER = PROJECT_ROOT / ".firstrun_done"

# Directorios configurables via .env (con fallback si no están definidos)
IMAGES_DIR = Path(os.getenv("IMAGES_DIR", str(PROJECT_ROOT / "images")))
TEMP_DIR   = Path(os.getenv("TEMP_DIR",   str(PROJECT_ROOT / ".tmp_musicdl")))

IMAGES_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# Carpeta de salida por defecto (sobreescribible en la UI también)
DEFAULT_OUTPUT_DIR = os.getenv("OUTPUT_DIR", str(Path.home() / "Music" / "MusicDL"))

GENRE_LIST = [
    "Pop", "Rock", "Hip-Hop", "R&B / Soul", "Electronic / Dance",
    "Indie", "Alternative", "Jazz", "Blues", "Classical",
    "Reggaeton", "Latin Pop", "Flamenco", "Metal", "Punk",
    "Folk", "Country", "Soundtrack / Score", "Ambient", "Lo-Fi",
    "Funk", "Gospel", "Trap", "Drill", "House", "Techno",
    "Drum & Bass", "Reggae", "Ska", "Bossa Nova", "Otro"
]

# ══════════════════════════════════════════════════════════════════
#  CSS — DARK VINYL AESTHETIC
# ══════════════════════════════════════════════════════════════════
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg:          #080808;
        --surface:     #111111;
        --surface2:    #181818;
        --surface3:    #202020;
        --gold:        #c9a84c;
        --gold-light:  #e8c86a;
        --gold-dim:    #7a6530;
        --gold-glow:   rgba(201,168,76,0.12);
        --text:        #ddd6c8;
        --text-dim:    #5e5850;
        --groove:      #1e1e1e;
        --success:     #4caf87;
        --error:       #c0392b;
        --warn:        #e67e22;
        --radius:      3px;
    }

    /* ── Base ── */
    .stApp { background: var(--bg) !important; font-family: 'DM Sans', sans-serif; }
    .block-container { max-width: 1300px !important; padding: 0 2rem 4rem !important; }
    p, li, span { color: var(--text); font-family: 'DM Sans', sans-serif; }
    h1,h2,h3,h4 {
        font-family: 'Bebas Neue', sans-serif !important;
        letter-spacing: 3px !important;
        color: var(--gold) !important;
    }
    hr { border-color: var(--groove) !important; margin: 1.5rem 0 !important; }

    /* ── App header ── */
    .app-header {
        text-align: center;
        padding: 2.5rem 0 1.5rem;
        border-bottom: 1px solid var(--groove);
        margin-bottom: 0;
    }
    .app-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 5rem;
        letter-spacing: 14px;
        color: var(--gold);
        text-shadow: 0 0 60px var(--gold-glow), 0 0 120px var(--gold-glow);
        margin: 0; line-height: 1;
    }
    .app-subtitle {
        color: var(--text-dim);
        font-family: 'DM Sans', sans-serif;
        font-size: 0.72rem;
        letter-spacing: 5px;
        text-transform: uppercase;
        margin-top: 0.4rem;
    }

    /* ── Section labels ── */
    .sec-label {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 1.25rem;
        letter-spacing: 5px;
        color: var(--gold);
        border-left: 3px solid var(--gold);
        padding-left: 0.7rem;
        margin: 1.4rem 0 0.6rem;
        text-transform: uppercase;
    }

    /* ── Cover frame ── */
    .cover-wrap {
        border: 1px solid var(--groove);
        border-radius: var(--radius);
        background: var(--surface);
        overflow: hidden;
        aspect-ratio: 1 / 1;
        display: flex; align-items: center; justify-content: center;
        position: sticky; top: 1rem;
    }
    .cover-placeholder {
        color: var(--text-dim);
        font-size: 5rem;
        text-align: center;
        line-height: 1;
    }
    .cover-placeholder small {
        display: block;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.7rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-top: 0.5rem;
    }

    /* ── Queue ── */
    .queue-wrap {
        background: var(--surface);
        border: 1px solid var(--groove);
        border-radius: var(--radius);
        padding: 0.8rem;
        max-height: 260px;
        overflow-y: auto;
    }
    .q-item {
        display: flex; align-items: baseline; gap: 0.6rem;
        background: var(--surface2);
        border-left: 3px solid var(--gold-dim);
        border-radius: 0 2px 2px 0;
        padding: 0.5rem 0.8rem;
        margin-bottom: 0.35rem;
        transition: border-color 0.2s;
    }
    .q-item:hover { border-left-color: var(--gold); }
    .q-num {
        font-family: 'Bebas Neue', sans-serif;
        color: var(--gold); font-size: 1rem;
        letter-spacing: 2px; min-width: 2ch;
    }
    .q-title { color: var(--text); font-size: 0.9rem; font-weight: 500; }
    .q-artist { color: var(--text-dim); font-size: 0.8rem; font-style: italic; margin-left: auto; }

    /* ── Log console ── */
    .log-console {
        background: #050505;
        border: 1px solid #1a1a1a;
        border-radius: var(--radius);
        padding: 1rem 1.2rem;
        font-family: 'JetBrains Mono', 'Courier New', monospace;
        font-size: 0.78rem;
        color: #6bff6b;
        max-height: 220px;
        overflow-y: auto;
        white-space: pre-wrap;
        word-break: break-all;
        line-height: 1.6;
    }
    .log-line-err  { color: #ff6b6b; }
    .log-line-info { color: #6bc8ff; }
    .log-line-ok   { color: #6bff6b; }
    .log-line-warn { color: #ffa84c; }

    /* ── Trim section ── */
    .trim-section {
        background: var(--surface);
        border: 1px solid var(--groove);
        border-top: 3px solid var(--gold-dim);
        border-radius: var(--radius);
        padding: 1.2rem 1.4rem;
        margin-top: 1rem;
    }

    /* ── Status pills ── */
    .pill {
        display: inline-block;
        padding: 0.15rem 0.7rem;
        border-radius: 20px;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.75rem;
        font-weight: 500;
        letter-spacing: 1px;
    }
    .pill-ok   { background: rgba(76,175,135,0.15); color: var(--success); border: 1px solid rgba(76,175,135,0.3); }
    .pill-err  { background: rgba(192,57,43,0.15);  color: var(--error);   border: 1px solid rgba(192,57,43,0.3); }
    .pill-warn { background: rgba(230,126,34,0.15); color: var(--warn);    border: 1px solid rgba(230,126,34,0.3); }
    .pill-info { background: rgba(201,168,76,0.1);  color: var(--gold);    border: 1px solid rgba(201,168,76,0.25); }

    /* ── Streamlit widget overrides ── */
    .stTextInput  > label,
    .stSelectbox  > label,
    .stTextArea   > label,
    .stNumberInput > label,
    .stFileUploader > label {
        color: var(--text-dim) !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.7rem !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        font-weight: 500 !important;
    }
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: var(--surface2) !important;
        color: var(--text) !important;
        border: 1px solid #252525 !important;
        border-radius: var(--radius) !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--gold-dim) !important;
        box-shadow: 0 0 0 1px var(--gold-glow) !important;
    }
    .stTextArea > div > textarea {
        background: var(--surface2) !important;
        color: var(--text) !important;
        border: 1px solid #252525 !important;
        border-radius: var(--radius) !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    div[data-baseweb="select"] > div {
        background: var(--surface2) !important;
        border-color: #252525 !important;
        border-radius: var(--radius) !important;
        color: var(--text) !important;
    }
    div[data-baseweb="select"] li {
        background: var(--surface3) !important;
        color: var(--text) !important;
    }
    div[data-baseweb="select"] li:hover {
        background: var(--surface2) !important;
        color: var(--gold) !important;
    }
    .stButton > button {
        background: var(--gold) !important;
        color: #080808 !important;
        border: none !important;
        border-radius: var(--radius) !important;
        font-family: 'Bebas Neue', sans-serif !important;
        letter-spacing: 4px !important;
        font-size: 1.05rem !important;
        padding: 0.5rem 1.5rem !important;
        width: 100% !important;
        transition: all 0.15s ease !important;
    }
    .stButton > button:hover {
        background: var(--gold-light) !important;
        box-shadow: 0 4px 24px var(--gold-glow) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:active { transform: translateY(0) !important; }
    div[data-testid="stTabs"] button {
        font-family: 'Bebas Neue', sans-serif !important;
        letter-spacing: 4px !important;
        color: var(--text-dim) !important;
        font-size: 1.1rem !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: var(--gold) !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"]::after {
        background: var(--gold) !important;
    }
    .stProgress > div > div > div { background: var(--gold) !important; }
    .stAlert { border-radius: var(--radius) !important; }
    div[data-testid="stFileUploader"] {
        background: var(--surface2) !important;
        border: 1px dashed #2a2a2a !important;
        border-radius: var(--radius) !important;
    }
    div[data-testid="stFileUploader"]:hover {
        border-color: var(--gold-dim) !important;
    }
    .stSpinner > div { border-top-color: var(--gold) !important; }
    .stCheckbox > label > span { color: var(--text) !important; }
    div[data-baseweb="checkbox"] > div { border-color: var(--gold-dim) !important; }
    div[data-baseweb="checkbox"][aria-checked="true"] > div {
        background: var(--gold) !important;
        border-color: var(--gold) !important;
    }
    .stRadio > label > div { color: var(--text) !important; }

    /* ── Hide Streamlit chrome ── */
    #MainMenu, footer, header, .stDeployButton { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════
def init_state():
    defaults = {
        # shared
        "output_dir":       DEFAULT_OUTPUT_DIR,
        "cover_path":       "",
        # album queue
        "album_queue":      [],         # list of dicts
        "album_title":      "",
        "album_artist":     "",
        "album_year":       str(time.localtime().tm_year),
        # single
        "single_fields":    {},
        # post-download
        "last_raw_mp3":     None,       # path to downloaded raw mp3 (before trim/metadata)
        "last_trimmed_mp3": None,       # path after trim
        "download_log":     [],
        "trim_start":       0.0,
        "trim_end":         0.0,
        "audio_duration":   0.0,
        "pending_metadata": None,       # dict with metadata to embed after trim
        "pending_mode":     None,       # "single" | "album_item"
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


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

    El campo 'artist' ya puede contener varios artistas separados por coma
    (p.ej. "Bad Bunny, J Balvin") — se respeta tal cual, solo se sanea.
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


# ══════════════════════════════════════════════════════════════════
#  HELPERS — YT-DLP DOWNLOAD
# ══════════════════════════════════════════════════════════════════
def download_audio(url: str, output_path: str) -> tuple[bool, str]:
    """
    Download audio with yt-dlp.
    output_path: full path WITHOUT extension — yt-dlp adds .mp3
    Returns (success, message)
    """
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "-f", "ba",
        "-x", "--audio-format", "mp3",
        "--audio-quality", "0",
        "-o", output_path + ".%(ext)s",
        "--no-playlist",
        url,
    ]
    add_log(f"Descargando: {url}", "info")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.returncode != 0:
            err = result.stderr[-800:] if result.stderr else "Error desconocido"
            add_log(f"yt-dlp error: {err}", "err")
            return False, err
        add_log("Descarga completada ✓", "ok")
        return True, "OK"
    except subprocess.TimeoutExpired:
        add_log("Timeout al descargar", "err")
        return False, "Timeout"
    except Exception as e:
        add_log(f"Excepción: {e}", "err")
        return False, str(e)


# ══════════════════════════════════════════════════════════════════
#  HELPERS — FFMPEG METADATA
# ══════════════════════════════════════════════════════════════════
def embed_metadata(
    input_mp3: str,
    output_mp3: str,
    cover_path: str,
    title: str,
    artist: str,
    album_artist: str,
    album: str,
    date: str,
    track: str,
    genre: str,
) -> tuple[bool, str]:
    """Embed metadata + cover art using ffmpeg."""
    add_log(f"Embebiendo metadatos en: {Path(output_mp3).name}", "info")

    # Build ffmpeg command
    cmd = ["ffmpeg", "-y", "-i", input_mp3]

    has_cover = cover_path and Path(cover_path).is_file()
    if has_cover:
        cmd += ["-i", cover_path]
        cmd += ["-map", "0:0", "-map", "1:0"]
        cmd += ["-c:a", "copy", "-c:v", "mjpeg"]
    else:
        cmd += ["-c:a", "copy"]

    cmd += [
        "-id3v2_version", "3",
        "-metadata", f"title={title}",
        "-metadata", f"artist={artist}",
        "-metadata", f"album_artist={album_artist}",
        "-metadata", f"album={album}",
        "-metadata", f"date={date}",
        "-metadata", f"track={track}",
        "-metadata", f"genre={genre}",
        output_mp3,
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            err = result.stderr[-600:] if result.stderr else "Error desconocido"
            add_log(f"ffmpeg error: {err}", "err")
            return False, err
        add_log(f"Metadatos embebidos ✓  →  {Path(output_mp3).name}", "ok")
        return True, "OK"
    except FileNotFoundError:
        msg = "ffmpeg no encontrado. ¿Está instalado y en el PATH?"
        add_log(msg, "err")
        return False, msg
    except Exception as e:
        add_log(f"Excepción ffmpeg: {e}", "err")
        return False, str(e)


# ══════════════════════════════════════════════════════════════════
#  HELPERS — MOVIEPY TRIM
# ══════════════════════════════════════════════════════════════════
def trim_audio(input_path: str, output_path: str, start: float, end: float) -> tuple[bool, str]:
    """Trim MP3 from start to end seconds using moviepy."""
    try:
        from moviepy import AudioFileClip
        add_log(f"Recortando: {seconds_to_hms(start)} → {seconds_to_hms(end)}", "info")
        with AudioFileClip(input_path) as clip:
            trimmed = clip.subclipped(start, end)
            trimmed.write_audiofile(output_path, logger=None)
        add_log("Recorte completado ✓", "ok")
        return True, "OK"
    except Exception as e:
        add_log(f"Error al recortar: {e}", "err")
        return False, str(e)


# ══════════════════════════════════════════════════════════════════
#  HELPERS — SHORTCUT CREATION
# ══════════════════════════════════════════════════════════════════
def _get_icon_path() -> tuple[Path | None, Path | None]:
    """
    Devuelve (png_path, ico_path).
    En Windows convierte el PNG a ICO usando Pillow si es necesario.
    """
    png = PROJECT_ROOT / "images" / "icono.png"
    if not png.is_file():
        return None, None

    ico = PROJECT_ROOT / "images" / "icono.ico"
    if not ico.is_file():
        try:
            from PIL import Image
            img = Image.open(png)
            # Genera el .ico con varios tamaños estándar
            img.save(ico, format="ICO", sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
        except Exception:
            ico = None   # Si falla, el .lnk se creará sin icono personalizado

    return png, ico


def create_shortcut():
    """Crea un acceso directo en el Escritorio con el icono images/icono.png."""
    # Intentar encontrar el Escritorio en español e inglés
    desktop = None
    for candidate in [
        Path.home() / "Escritorio",
        Path.home() / "Desktop",
        Path.home() / "OneDrive" / "Escritorio",
        Path.home() / "OneDrive" / "Desktop",
    ]:
        if candidate.is_dir():
            desktop = candidate
            break
    if desktop is None:
        desktop = Path.home() / "Desktop"
        desktop.mkdir(exist_ok=True)

    python   = sys.executable
    app_path = PROJECT_ROOT / "main.py"
    system   = platform.system()
    png_icon, ico_icon = _get_icon_path()

    try:
        if system == "Windows":
            # ── Lanzador .bat ──────────────────────────────────
            bat_path = PROJECT_ROOT / "MusicDL.bat"
            bat_path.write_text(
                f'@echo off\ntitle MusicDL\n\"{python}\" -m streamlit run \"{app_path}\" --server.headless false\npause\n',
                encoding="utf-8",
            )

            # ── Acceso directo .lnk con icono vía VBScript ─────
            lnk_path  = desktop / "MusicDL.lnk"
            icon_line = f'oLink.IconLocation = "{ico_icon}, 0"\n' if ico_icon and ico_icon.is_file() else ""
            vbs = tempfile.NamedTemporaryFile(suffix=".vbs", delete=False, mode="w", encoding="utf-8")
            vbs.write(
                f'Set oShell = CreateObject("WScript.Shell")\n'
                f'Set oLink = oShell.CreateShortcut("{lnk_path}")\n'
                f'oLink.TargetPath = "{bat_path}"\n'
                f'oLink.WorkingDirectory = "{PROJECT_ROOT}"\n'
                f'oLink.Description = "MusicDL — YouTube Music Downloader"\n'
                f'{icon_line}'
                f'oLink.Save\n'
            )
            vbs.close()
            subprocess.run(["cscript", "//Nologo", vbs.name], capture_output=True)
            Path(vbs.name).unlink(missing_ok=True)

        elif system == "Linux":
            sh_path = PROJECT_ROOT / "MusicDL.sh"
            sh_path.write_text(
                f'#!/bin/bash\ncd "{PROJECT_ROOT}"\n"{python}" -m streamlit run "{app_path}"\n',
                encoding="utf-8",
            )
            sh_path.chmod(0o755)
            icon_line = f"Icon={png_icon}\n" if png_icon else "Icon=audio-x-generic\n"
            desktop_entry = desktop / "MusicDL.desktop"
            desktop_entry.write_text(
                f"[Desktop Entry]\nType=Application\nName=MusicDL\n"
                f"Comment=YouTube Music Downloader\n"
                f"Exec=bash -c '{sh_path}'\n"
                f"{icon_line}"
                f"Terminal=true\nCategories=Music;AudioVideo;\n",
                encoding="utf-8",
            )
            desktop_entry.chmod(0o755)

        elif system == "Darwin":  # macOS
            sh_path = PROJECT_ROOT / "MusicDL.sh"
            sh_path.write_text(
                f'#!/bin/bash\ncd "{PROJECT_ROOT}"\n"{python}" -m streamlit run "{app_path}"\n',
                encoding="utf-8",
            )
            sh_path.chmod(0o755)
            # En macOS creamos un alias .command (doble-click lo abre en Terminal)
            cmd_path = desktop / "MusicDL.command"
            cmd_path.write_text(
                f'#!/bin/bash\ncd "{PROJECT_ROOT}"\n"{python}" -m streamlit run "{app_path}"\n',
                encoding="utf-8",
            )
            cmd_path.chmod(0o755)

        FIRST_RUN_MARKER.write_text("done")
        return True, system
    except Exception as e:
        return False, str(e)


# ══════════════════════════════════════════════════════════════════
#  FIRST-RUN CHECK
# ══════════════════════════════════════════════════════════════════
def check_first_run():
    if not FIRST_RUN_MARKER.exists():
        ok, info = create_shortcut()
        if ok:
            st.toast(f"✅ Acceso directo creado en el Escritorio ({info})", icon="🎵")
        else:
            st.toast(f"⚠️ No se pudo crear el acceso directo: {info}", icon="⚠️")


# ══════════════════════════════════════════════════════════════════
#  UI — LOG CONSOLE
# ══════════════════════════════════════════════════════════════════
def render_log():
    if not st.session_state.download_log:
        return
    lines_html = ""
    for ts, level, msg in reversed(st.session_state.download_log[-40:]):
        css_class = {"ok": "log-line-ok", "err": "log-line-err",
                     "info": "log-line-info", "warn": "log-line-warn"}.get(level, "")
        safe_msg = msg.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        lines_html += f'<div class="{css_class}">[{ts}] {safe_msg}</div>\n'
    st.markdown(f'<div class="log-console">{lines_html}</div>', unsafe_allow_html=True)
    if st.button("🗑 Limpiar log", key="clear_log"):
        st.session_state.download_log = []
        st.rerun()


# ══════════════════════════════════════════════════════════════════
#  UI — COVER PREVIEW COLUMN
# ══════════════════════════════════════════════════════════════════
def render_cover_panel(prefix: str = ""):
    cover = st.session_state.cover_path
    cover_path = Path(cover) if cover else None

    if cover_path and cover_path.is_file() and cover_path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}:
        st.image(str(cover_path), use_container_width=True)
        st.markdown(
            f'<div style="text-align:center; margin-top:0.4rem;">'
            f'<span class="pill pill-ok">✓ Portada cargada</span></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="cover-wrap"><div class="cover-placeholder">'
            '🎵<small>Sin portada</small></div></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="sec-label">Portada</div>', unsafe_allow_html=True)
    cover_input = st.text_input(
        "Ruta de la imagen (JPG / PNG)",
        value=st.session_state.cover_path,
        placeholder="C:/ruta/portada.jpg  o  ./images/cover.jpg",
        key=f"{prefix}cover_path_input",
    )
    if cover_input != st.session_state.cover_path:
        st.session_state.cover_path = cover_input
        st.rerun()

    uploaded = st.file_uploader(
        "O sube la imagen aquí",
        type=["jpg", "jpeg", "png", "webp"],
        key=f"{prefix}cover_upload",
    )
    if uploaded:
        dest = IMAGES_DIR / uploaded.name
        dest.write_bytes(uploaded.getbuffer())
        st.session_state.cover_path = str(dest)
        st.rerun()

    # Output folder
    st.markdown('<div class="sec-label">Destino</div>', unsafe_allow_html=True)
    out_dir = st.text_input(
        "Carpeta de salida",
        value=st.session_state.output_dir,
        key=f"{prefix}out_dir_input",
    )
    if out_dir != st.session_state.output_dir:
        st.session_state.output_dir = out_dir


# ══════════════════════════════════════════════════════════════════
#  UI — TRIM SECTION
# ══════════════════════════════════════════════════════════════════
def render_trim_section():
    raw = st.session_state.last_raw_mp3
    if not raw or not Path(raw).is_file():
        return

    st.markdown('<div class="sec-label">✂ Recortar Audio</div>', unsafe_allow_html=True)
    st.markdown('<div class="trim-section">', unsafe_allow_html=True)

    duration = st.session_state.audio_duration or get_audio_duration(raw)
    if duration > 0:
        st.session_state.audio_duration = duration
        dur_str = seconds_to_hms(duration)
        st.markdown(
            f'<p style="color:var(--text-dim); font-size:0.8rem; margin-bottom:0.5rem;">'
            f'Duración total: <strong style="color:var(--gold);">{dur_str}</strong> · '
            f'Reproduce el audio, apunta los tiempos y corta lo que no quieras.</p>',
            unsafe_allow_html=True,
        )

    # Audio player
    with open(raw, "rb") as f:
        st.audio(f.read(), format="audio/mp3")

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        start_str = st.text_input(
            "Inicio del recorte (mm:ss o segundos)",
            value="0",
            key="trim_start_input",
            placeholder="0  o  00:30",
        )
    with c2:
        end_str = st.text_input(
            "Fin del recorte (mm:ss o segundos, 0 = hasta el final)",
            value="0",
            key="trim_end_input",
            placeholder="0  o  03:45",
        )

    def parse_time(s: str, fallback: float) -> float:
        s = s.strip()
        if not s or s == "0":
            return fallback
        if ":" in s:
            parts = s.split(":")
            try:
                if len(parts) == 2:
                    return int(parts[0]) * 60 + float(parts[1])
                elif len(parts) == 3:
                    return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
            except Exception:
                return fallback
        try:
            return float(s)
        except Exception:
            return fallback

    t_start = parse_time(start_str, 0.0)
    t_end   = parse_time(end_str, duration if duration > 0 else 0.0)
    if t_end == 0.0 and duration > 0:
        t_end = duration

    if t_start > 0 or (t_end < duration and t_end > 0):
        info_txt = f"Se recortará desde {seconds_to_hms(t_start)} hasta {seconds_to_hms(t_end)}"
        st.markdown(f'<span class="pill pill-info">{info_txt}</span>', unsafe_allow_html=True)

    col_trim, col_skip = st.columns(2)
    with col_trim:
        if st.button("✂ Aplicar Recorte", key="btn_trim"):
            if t_start == 0.0 and (t_end == 0.0 or t_end >= duration):
                st.warning("Sin cambios: introduce tiempos de inicio/fin.")
            elif t_start >= t_end:
                st.error("El inicio debe ser menor que el fin.")
            else:
                trimmed_path = str(TEMP_DIR / "trimmed_temp.mp3")
                with st.spinner("Recortando con moviepy…"):
                    ok, msg = trim_audio(raw, trimmed_path, t_start, t_end)
                if ok:
                    st.session_state.last_trimmed_mp3 = trimmed_path
                    st.session_state.audio_duration   = t_end - t_start
                    st.session_state.last_raw_mp3     = trimmed_path  # update for re-render
                    st.success("✓ Recorte aplicado. Puedes escucharlo arriba.")
                    st.rerun()
                else:
                    st.error(f"Error al recortar: {msg}")
    with col_skip:
        if st.button("➡ Sin Recorte", key="btn_skip_trim"):
            st.session_state.last_trimmed_mp3 = raw
            st.info("Se usará el audio sin recortar.")

    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#  CORE PROCESS — Download → (trim) → embed metadata
# ══════════════════════════════════════════════════════════════════
def process_song(metadata: dict, url: str, mode: str):
    """
    Download audio, save raw to temp, set session state for trim/finalize.
    metadata: dict with title, artist, album_artist, album, date, track, genre
    mode: "single" | "album_item"
    """
    title_safe = sanitize_filename(metadata["title"] or "track")
    temp_base  = str(TEMP_DIR / f"raw_{title_safe}")

    # Reset previous state
    st.session_state.last_raw_mp3     = None
    st.session_state.last_trimmed_mp3 = None
    st.session_state.audio_duration   = 0.0
    st.session_state.pending_metadata = metadata
    st.session_state.pending_mode     = mode

    with st.spinner(f"Descargando «{metadata['title']}»…"):
        ok, msg = download_audio(url, temp_base)

    if not ok:
        st.error(f"Error al descargar: {msg}")
        return

    # Find the downloaded file (yt-dlp may adjust extension)
    raw_mp3 = Path(temp_base + ".mp3")
    if not raw_mp3.is_file():
        # Look for any mp3 matching the base name
        candidates = list(TEMP_DIR.glob(f"raw_{title_safe}*"))
        if not candidates:
            st.error("No se encontró el archivo descargado.")
            return
        raw_mp3 = candidates[0]

    st.session_state.last_raw_mp3   = str(raw_mp3)
    st.session_state.audio_duration = get_audio_duration(str(raw_mp3))
    st.success(f"✓ Audio descargado. Ahora puedes recortarlo o proceder a finalizar.")
    st.rerun()


def finalize_song():
    """Embed metadata into the (optionally trimmed) audio and save to output dir."""
    meta = st.session_state.pending_metadata
    mode = st.session_state.pending_mode
    if not meta:
        st.error("No hay metadatos pendientes.")
        return

    source = st.session_state.last_trimmed_mp3 or st.session_state.last_raw_mp3
    if not source or not Path(source).is_file():
        st.error("No hay audio descargado para finalizar.")
        return

    out_dir  = ensure_output_dir(st.session_state.output_dir)
    out_name = build_filename(meta["artist"], meta["title"])
    out_path = str(out_dir / out_name)

    with st.spinner("Embebiendo metadatos…"):
        ok, msg = embed_metadata(
            input_mp3    = source,
            output_mp3   = out_path,
            cover_path   = st.session_state.cover_path,
            title        = meta["title"],
            artist       = meta["artist"],
            album_artist = meta["album_artist"],
            album        = meta["album"],
            date         = meta["date"],
            track        = str(meta.get("track", "")),
            genre        = meta["genre"],
        )

    if not ok:
        st.error(f"Error al embeber: {msg}")
        return

    st.success(f"✅ Guardado en: `{out_path}`")
    st.balloons()

    # Cleanup temp files
    for p in [st.session_state.last_raw_mp3, st.session_state.last_trimmed_mp3]:
        if p and Path(p).is_file() and Path(p).parent == TEMP_DIR:
            try:
                Path(p).unlink()
            except Exception:
                pass

    # Reset state based on mode
    st.session_state.last_raw_mp3     = None
    st.session_state.last_trimmed_mp3 = None
    st.session_state.audio_duration   = 0.0
    st.session_state.pending_metadata = None
    st.session_state.pending_mode     = None

    if mode == "single":
        # Clear all single-song fields
        for k in ["s_url", "s_title", "s_artist", "s_album_artist",
                  "s_album", "s_year", "s_track", "s_genre"]:
            if k in st.session_state:
                del st.session_state[k]
        st.info("Campos limpiados para la siguiente canción.")

    st.rerun()


# ══════════════════════════════════════════════════════════════════
#  UI — SINGLE SONG TAB
# ══════════════════════════════════════════════════════════════════
def render_single_tab():
    left, right = st.columns([3, 2], gap="large")

    with right:
        render_cover_panel(prefix="single_")

    with left:
        st.markdown('<div class="sec-label">URL de YouTube</div>', unsafe_allow_html=True)
        url = st.text_input(
            "Enlace de YouTube",
            key="s_url",
            placeholder="https://www.youtube.com/watch?v=...",
            label_visibility="collapsed",
        )
        if url:
            valid, vmsg = validate_yt_url(url)
            badge_cls = "pill-ok" if valid else "pill-err"
            badge_txt = f"✓ URL válida" if valid else f"✗ {vmsg}"
            st.markdown(f'<span class="pill {badge_cls}">{badge_txt}</span>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

        st.markdown('<div class="sec-label">Metadatos</div>', unsafe_allow_html=True)
        r1c1, r1c2 = st.columns(2)
        with r1c1:
            title = st.text_input("Título de la canción", key="s_title", placeholder="Nombre del tema")
        with r1c2:
            artist = st.text_input("Artista / Colaboradores", key="s_artist",
                                   placeholder="Artista Feat. Otro")

        r2c1, r2c2 = st.columns(2)
        with r2c1:
            album_artist = st.text_input("Artista principal del álbum", key="s_album_artist",
                                         placeholder="Artista Principal")
        with r2c2:
            album = st.text_input("Nombre del álbum", key="s_album",
                                  placeholder="Nombre del álbum")

        r3c1, r3c2, r3c3 = st.columns([1, 1, 2])
        with r3c1:
            year = st.text_input("Año", key="s_year",
                                 value=str(time.localtime().tm_year))
        with r3c2:
            track = st.number_input("Nº Pista", key="s_track",
                                    min_value=0, max_value=999, value=1, step=1)
        with r3c3:
            genre = st.selectbox("Género", GENRE_LIST, key="s_genre")

        st.markdown("<br>", unsafe_allow_html=True)

        # State-aware button area
        raw_exists = st.session_state.last_raw_mp3 and Path(st.session_state.last_raw_mp3).is_file()
        pending_is_single = st.session_state.pending_mode == "single"

        if raw_exists and pending_is_single:
            st.markdown(
                '<span class="pill pill-warn">⏸ Audio descargado — recorta o finaliza</span>',
                unsafe_allow_html=True,
            )
            render_trim_section()
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("💾 Finalizar y Guardar", key="btn_finalize_single"):
                finalize_song()
        else:
            can_download = bool(
                st.session_state.get("s_url", "").strip() and
                st.session_state.get("s_title", "").strip()
            )
            if not can_download:
                st.markdown(
                    '<span class="pill pill-warn">Rellena al menos la URL y el Título</span>',
                    unsafe_allow_html=True,
                )
            if st.button("⬇ Descargar y Procesar", key="btn_dl_single",
                         disabled=not can_download):
                meta = {
                    "title":        st.session_state.get("s_title", ""),
                    "artist":       st.session_state.get("s_artist", ""),
                    "album_artist": st.session_state.get("s_album_artist", ""),
                    "album":        st.session_state.get("s_album", ""),
                    "date":         st.session_state.get("s_year", ""),
                    "track":        st.session_state.get("s_track", 0),
                    "genre":        st.session_state.get("s_genre", ""),
                }
                process_song(meta, st.session_state.get("s_url", ""), mode="single")

        # Log
        if st.session_state.download_log:
            st.markdown('<div class="sec-label">Log</div>', unsafe_allow_html=True)
            render_log()


# ══════════════════════════════════════════════════════════════════
#  UI — ALBUM TAB
# ══════════════════════════════════════════════════════════════════
def render_album_tab():
    left, right = st.columns([3, 2], gap="large")

    with right:
        render_cover_panel(prefix="album_")

        # Album-level persistent fields in sidebar column
        st.markdown('<div class="sec-label">Datos del Álbum</div>', unsafe_allow_html=True)
        st.session_state.album_title = st.text_input(
            "Nombre del Álbum", key="alb_title_inp",
            value=st.session_state.album_title,
            placeholder="Título del álbum",
        )
        st.session_state.album_artist = st.text_input(
            "Artista Principal (Album Artist)", key="alb_artist_inp",
            value=st.session_state.album_artist,
            placeholder="Artista del álbum",
        )
        st.session_state.album_year = st.text_input(
            "Año", key="alb_year_inp",
            value=st.session_state.album_year,
        )

        # Queue display
        if st.session_state.album_queue:
            st.markdown('<div class="sec-label">Cola del Álbum</div>', unsafe_allow_html=True)
            items_html = ""
            for i, item in enumerate(st.session_state.album_queue, 1):
                items_html += (
                    f'<div class="q-item">'
                    f'<span class="q-num">{str(item["track"]).zfill(2)}</span>'
                    f'<span class="q-title">{item["title"]}</span>'
                    f'<span class="q-artist">{item["artist"] or item["album_artist"]}</span>'
                    f'</div>'
                )
            st.markdown(f'<div class="queue-wrap">{items_html}</div>', unsafe_allow_html=True)

            cola, colb = st.columns(2)
            with cola:
                if st.button("🗑 Limpiar cola", key="btn_clear_queue"):
                    st.session_state.album_queue = []
                    st.rerun()
            with colb:
                if st.button("⬇ Descargar todo", key="btn_dl_all"):
                    _download_album_queue()

    with left:
        st.markdown('<div class="sec-label">URL de YouTube</div>', unsafe_allow_html=True)
        url_alb = st.text_input(
            "Enlace de YouTube", key="alb_url",
            placeholder="https://www.youtube.com/watch?v=...",
            label_visibility="collapsed",
        )
        if url_alb:
            valid, vmsg = validate_yt_url(url_alb)
            badge_cls = "pill-ok" if valid else "pill-err"
            badge_txt = "✓ URL válida" if valid else f"✗ {vmsg}"
            st.markdown(f'<span class="pill {badge_cls}">{badge_txt}</span>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

        st.markdown('<div class="sec-label">Metadatos por Canción</div>', unsafe_allow_html=True)

        r1c1, r1c2 = st.columns(2)
        with r1c1:
            title_alb = st.text_input("Título de la canción", key="alb_song_title",
                                      placeholder="Nombre del tema")
        with r1c2:
            artist_alb = st.text_input(
                "Artista / Colaboradores (deja en blanco si solo el principal)",
                key="alb_song_artist",
                placeholder="Artista Feat. Otro  (opcional)",
            )

        r2c1, r2c2 = st.columns(2)
        with r2c1:
            track_alb = st.number_input("Nº Pista", key="alb_song_track",
                                        min_value=1, max_value=999,
                                        value=len(st.session_state.album_queue) + 1,
                                        step=1)
        with r2c2:
            genre_alb = st.selectbox("Género", GENRE_LIST, key="alb_song_genre")

        st.markdown("<br>", unsafe_allow_html=True)

        # Pending album song actions
        raw_exists      = st.session_state.last_raw_mp3 and Path(st.session_state.last_raw_mp3).is_file()
        pending_is_alb  = st.session_state.pending_mode == "album_item"

        if raw_exists and pending_is_alb:
            cur_meta = st.session_state.pending_metadata or {}
            st.markdown(
                f'<span class="pill pill-warn">⏸ Audio descargado: «{cur_meta.get("title","")}» — recorta o finaliza</span>',
                unsafe_allow_html=True,
            )
            render_trim_section()
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("💾 Finalizar esta canción", key="btn_finalize_alb"):
                finalize_song()
        else:
            can_add = bool(
                st.session_state.get("alb_url", "").strip() and
                st.session_state.get("alb_song_title", "").strip() and
                st.session_state.get("alb_title_inp", "").strip() and
                st.session_state.get("alb_artist_inp", "").strip()
            )

            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button("➕ Añadir a la Cola", key="btn_add_queue",
                             disabled=not can_add):
                    valid, vmsg = validate_yt_url(url_alb)
                    if valid:
                        st.session_state.album_queue.append({
                            "url":          url_alb,
                            "title":        title_alb,
                            "artist":       artist_alb or st.session_state.album_artist,
                            "album_artist": st.session_state.album_artist,
                            "album":        st.session_state.album_title,
                            "date":         st.session_state.album_year,
                            "track":        int(track_alb),
                            "genre":        genre_alb,
                        })
                        # Clear song-specific fields
                        for k in ["alb_url", "alb_song_title", "alb_song_artist"]:
                            if k in st.session_state:
                                del st.session_state[k]
                        st.success(f"✓ «{title_alb}» añadida a la cola.")
                        st.rerun()
                    else:
                        st.error(f"URL inválida: {vmsg}")

            with btn_col2:
                if st.button("⬇ Descargar esta canción", key="btn_dl_one",
                             disabled=not can_add):
                    valid, vmsg = validate_yt_url(url_alb)
                    if valid:
                        meta = {
                            "title":        title_alb,
                            "artist":       artist_alb or st.session_state.album_artist,
                            "album_artist": st.session_state.album_artist,
                            "album":        st.session_state.album_title,
                            "date":         st.session_state.album_year,
                            "track":        int(track_alb),
                            "genre":        genre_alb,
                        }
                        process_song(meta, url_alb, mode="album_item")
                    else:
                        st.error(f"URL inválida: {vmsg}")

            if not can_add:
                st.markdown(
                    '<span class="pill pill-warn">Rellena URL, Título y los datos del Álbum (derecha)</span>',
                    unsafe_allow_html=True,
                )

        # Log
        if st.session_state.download_log:
            st.markdown('<div class="sec-label">Log</div>', unsafe_allow_html=True)
            render_log()


def _download_album_queue():
    """Download and process all songs in the album queue sequentially."""
    queue = list(st.session_state.album_queue)
    if not queue:
        st.warning("La cola está vacía.")
        return

    progress = st.progress(0, text="Iniciando descarga del álbum…")
    total    = len(queue)

    for i, item in enumerate(queue):
        progress.progress((i) / total, text=f"Descargando {i+1}/{total}: «{item['title']}»")
        url_item   = item.pop("url")
        title_safe = sanitize_filename(item["title"] or f"track_{item['track']}")
        temp_base  = str(TEMP_DIR / f"raw_{title_safe}")

        ok, msg = download_audio(url_item, temp_base)
        if not ok:
            st.error(f"Error en «{item['title']}»: {msg}")
            continue

        raw_mp3 = Path(temp_base + ".mp3")
        if not raw_mp3.is_file():
            candidates = list(TEMP_DIR.glob(f"raw_{title_safe}*"))
            if not candidates:
                st.error(f"No se encontró el archivo de «{item['title']}»")
                continue
            raw_mp3 = candidates[0]

        out_dir  = ensure_output_dir(st.session_state.output_dir)
        out_name = build_filename(item["artist"], item["title"])
        out_path = str(out_dir / out_name)

        embed_ok, embed_msg = embed_metadata(
            input_mp3    = str(raw_mp3),
            output_mp3   = out_path,
            cover_path   = st.session_state.cover_path,
            title        = item["title"],
            artist       = item["artist"],
            album_artist = item["album_artist"],
            album        = item["album"],
            date         = item["date"],
            track        = str(item["track"]),
            genre        = item["genre"],
        )
        if not embed_ok:
            st.error(f"Error al embeber metadatos en «{item['title']}»: {embed_msg}")
        else:
            progress.progress((i + 1) / total, text=f"✓ {i+1}/{total}: «{item['title']}» guardado")

        try:
            raw_mp3.unlink()
        except Exception:
            pass

    progress.progress(1.0, text="✅ Álbum descargado completo")
    st.session_state.album_queue = []
    st.balloons()
    st.success(f"✅ {total} canciones guardadas en: `{st.session_state.output_dir}`")


# ══════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════
def main():
    inject_css()
    init_state()
    check_first_run()

    # ── Header ──────────────────────────────────────────
    st.markdown(
        '<div class="app-header">'
        '<div class="app-title">MusicDL</div>'
        '<div class="app-subtitle">YouTube · Download · Tag · Organize</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Mode Tabs ────────────────────────────────────────
    tab_single, tab_album = st.tabs(["🎵  CANCIÓN INDIVIDUAL", "💿  ÁLBUM COMPLETO"])

    with tab_single:
        st.markdown("<br>", unsafe_allow_html=True)
        render_single_tab()

    with tab_album:
        st.markdown("<br>", unsafe_allow_html=True)
        render_album_tab()


if __name__ == "__main__":
    main()
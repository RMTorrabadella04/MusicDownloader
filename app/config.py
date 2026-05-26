import os
from pathlib import Path
from dotenv import load_dotenv

# ══════════════════════════════════════════════════════════════════
#  CONSTANTS  —  rutas resueltas desde .env
# ══════════════════════════════════════════════════════════════════
# PROJECT_ROOT apunta a la carpeta principal (padre de 'app')
PROJECT_ROOT     = Path(__file__).parent.parent
FIRST_RUN_MARKER = PROJECT_ROOT / ".firstrun_done"

_ENV_FILE = PROJECT_ROOT / ".env"
load_dotenv(_ENV_FILE)

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
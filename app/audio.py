import sys
import subprocess
from pathlib import Path
from app.utils import add_log, seconds_to_hms

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
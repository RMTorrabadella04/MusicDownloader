import platform
import sys
import subprocess
import tempfile
from pathlib import Path
import streamlit as st

from app.config import PROJECT_ROOT, FIRST_RUN_MARKER

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
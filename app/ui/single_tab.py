import time
import streamlit as st
from pathlib import Path

from app.config import TEMP_DIR, GENRE_LIST
from app.utils import validate_yt_url, sanitize_filename, build_filename, ensure_output_dir, get_audio_duration
from app.audio import download_audio, embed_metadata
from app.ui.log_panel import render_log
from app.ui.cover_panel import render_cover_panel
from app.ui.trim_panel import render_trim_section

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
            render_log(prefix="single_")
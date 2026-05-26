import streamlit as st
from pathlib import Path

from app.config import TEMP_DIR, GENRE_LIST
from app.utils import validate_yt_url, sanitize_filename, build_filename, ensure_output_dir
from app.audio import download_audio, embed_metadata
from app.ui.log_panel import render_log
from app.ui.cover_panel import render_cover_panel
from app.ui.trim_panel import render_trim_section
from app.ui.single_tab import process_song, finalize_song

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
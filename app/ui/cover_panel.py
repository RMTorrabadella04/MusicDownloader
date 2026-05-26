import streamlit as st
from pathlib import Path
from app.config import IMAGES_DIR

# ══════════════════════════════════════════════════════════════════
#  UI — COVER PREVIEW COLUMN
# ══════════════════════════════════════════════════════════════════

def ensure_output_dir(path: str) -> Path:
    # Solo quitamos comillas accidentales de los extremos, nada de magia negra
    clean_path = str(path).strip(' "\'')
    p = Path(clean_path)
    p.mkdir(parents=True, exist_ok=True)
    return p

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
    output_dir = ensure_output_dir(st.session_state.output_dir)  # Aseguramos que la carpeta exista
    out_dir = st.text_input(
        "Carpeta de salida",
        value=output_dir,
        key=f"{prefix}out_dir_input",
    )
    if out_dir != st.session_state.output_dir:
        st.session_state.output_dir = out_dir


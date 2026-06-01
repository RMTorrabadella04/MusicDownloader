import streamlit as st
from pathlib import Path
from app.config import IMAGES_DIR

# ══════════════════════════════════════════════════════════════════
#  UI — COVER PREVIEW COLUMN
# ══════════════════════════════════════════════════════════════════

def ensure_output_dir(path: str) -> Path:
    clean_path = str(path).strip(' "\'')
    p = Path(clean_path)
    p.mkdir(parents=True, exist_ok=True)
    return p

def cleanup_cover_temp() -> None:
    """Borra todo el contenido de images/temp."""
    temp_dir = IMAGES_DIR 
    for f in temp_dir.iterdir():
        if f.is_file():
            try:
                f.unlink()
            except Exception:
                pass


def render_cover_panel(prefix: str = ""):
    input_key  = f"{prefix}cover_path_input"
    upload_key = f"{prefix}cover_upload"
    outdir_key = f"{prefix}out_dir_input"

    # ── PASO 1: procesar el archivo subido ANTES de dibujar ningún widget ──
    # En Streamlit, el valor del file_uploader del ciclo anterior sigue
    # disponible en session_state al inicio del nuevo ciclo, antes de que
    # se instancie ningún widget. Es el único momento en que podemos
    # actualizar input_key sin que Streamlit se queje.
    uploaded_file = st.session_state.get(upload_key)
    if uploaded_file is not None:
        dest = IMAGES_DIR / uploaded_file.name
        dest.write_bytes(uploaded_file.getbuffer())
        st.session_state.cover_path = str(dest)
        st.session_state[input_key] = str(dest)   # seguro: widget aún no instanciado

    # ── PASO 2: inicializar claves la primera vez ───────────────────────────
    if input_key not in st.session_state:
        st.session_state[input_key] = st.session_state.cover_path
    if outdir_key not in st.session_state:
        st.session_state[outdir_key] = st.session_state.output_dir

    # ── PASO 3: callbacks de sincronización ────────────────────────────────
    def _sync_cover():
        st.session_state.cover_path = st.session_state[input_key]

    def _sync_outdir():
        st.session_state.output_dir = st.session_state[outdir_key]

    # ── PASO 4: dibujar widgets ────────────────────────────────────────────
    cover      = st.session_state.cover_path
    cover_path = Path(cover) if cover else None

    if cover_path and cover_path.is_file() and cover_path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}:
        st.image(str(cover_path), use_container_width=True)
        st.markdown(
            '<div style="text-align:center; margin-top:0.4rem;">'
            '<span class="pill pill-ok">✓ Portada cargada</span></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="cover-wrap"><div class="cover-placeholder">'
            '🎵<small>Sin portada</small></div></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="sec-label">Portada</div>', unsafe_allow_html=True)
    st.text_input(
        "Ruta de la imagen (JPG / PNG)",
        placeholder="C:/ruta/portada.jpg  o  ./images/temp/cover.jpg",
        key=input_key,
        on_change=_sync_cover,
    )

    st.file_uploader(
        "O sube la imagen aquí",
        type=["jpg", "jpeg", "png", "webp"],
        key=upload_key,
    )

    st.markdown('<div class="sec-label">Destino</div>', unsafe_allow_html=True)
    ensure_output_dir(st.session_state.output_dir)
    st.text_input(
        "Carpeta de salida",
        key=outdir_key,
        on_change=_sync_outdir,
    )
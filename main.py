import streamlit as st

# ══════════════════════════════════════════════════════════════════
#  PAGE CONFIG  (must be the VERY FIRST Streamlit call)
# ══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="MusicDL",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Importamos los módulos de la app después del page_config
from app.state import init_state
from app.styles import inject_css
from app.shortcut import check_first_run
from app.ui.single_tab import render_single_tab
from app.ui.album_tab import render_album_tab

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
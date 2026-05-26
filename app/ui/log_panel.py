import streamlit as st

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
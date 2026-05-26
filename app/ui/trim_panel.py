import streamlit as st
from pathlib import Path
from app.config import TEMP_DIR
from app.utils import get_audio_duration, seconds_to_hms
from app.audio import trim_audio

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
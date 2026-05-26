import time
import streamlit as st
from app.config import DEFAULT_OUTPUT_DIR

# ══════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════
def init_state():
    defaults = {
        # shared
        "output_dir":       DEFAULT_OUTPUT_DIR,
        "cover_path":       "",
        # album queue
        "album_queue":      [],         # list of dicts
        "album_title":      "",
        "album_artist":     "",
        "album_year":       str(time.localtime().tm_year),
        # single
        "single_fields":    {},
        # post-download
        "last_raw_mp3":     None,       # path to downloaded raw mp3 (before trim/metadata)
        "last_trimmed_mp3": None,       # path after trim
        "download_log":     [],
        "trim_start":       0.0,
        "trim_end":         0.0,
        "audio_duration":   0.0,
        "pending_metadata": None,       # dict with metadata to embed after trim
        "pending_mode":     None,       # "single" | "album_item"
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
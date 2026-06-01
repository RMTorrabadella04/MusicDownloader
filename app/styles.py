import streamlit as st

# ══════════════════════════════════════════════════════════════════
#  CSS — DARK MUSIC DOWNLOADER AESTHETIC
# ══════════════════════════════════════════════════════════════════
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg:          #07080f;
        --surface:     #0e1020;
        --surface2:    #151829;
        --surface3:    #1c2035;
        --purple:      #7C3AED;
        --blue:        #2563EB;
        --cyan:        #06B6D4;
        --accent:      #6D28D9;
        --accent-light:#8B5CF6;
        --accent-glow: rgba(109,40,217,0.18);
        --grad:        linear-gradient(135deg, #7C3AED 0%, #2563EB 60%, #06B6D4 100%);
        --text:        #e2e8f8;
        --text-dim:    #4a5280;
        --groove:      #1a1d30;
        --success:     #10b981;
        --error:       #ef4444;
        --warn:        #f59e0b;
        --radius:      4px;
    }

    /* ── Base ── */
    .stApp { background: var(--bg) !important; font-family: 'DM Sans', sans-serif; }
    .block-container { max-width: 1300px !important; padding: 0 2rem 4rem !important; }
    p, li, span { color: var(--text); font-family: 'DM Sans', sans-serif; }
    h1,h2,h3,h4 {
        font-family: 'Bebas Neue', sans-serif !important;
        letter-spacing: 3px !important;
        color: var(--accent-light) !important;
    }
    hr { border-color: var(--groove) !important; margin: 1.5rem 0 !important; }

    /* ── App header ── */
    .app-header {
        text-align: center;
        padding: 2.5rem 0 1.5rem;
        border-bottom: 1px solid var(--groove);
        margin-bottom: 0;
    }
    .app-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 5rem;
        letter-spacing: 14px;
        background: var(--grad);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        filter: drop-shadow(0 0 40px rgba(109,40,217,0.4));
        margin: 0; line-height: 1;
    }
    .app-subtitle {
        color: var(--text-dim);
        font-family: 'DM Sans', sans-serif;
        font-size: 0.72rem;
        letter-spacing: 5px;
        text-transform: uppercase;
        margin-top: 0.4rem;
    }

    /* ── Section labels ── */
    .sec-label {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 1.25rem;
        letter-spacing: 5px;
        background: var(--grad);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        border-left: 3px solid var(--purple);
        padding-left: 0.7rem;
        margin: 1.4rem 0 0.6rem;
        text-transform: uppercase;
    }

    /* ── Cover frame ── */
    .cover-wrap {
        border: 1px solid var(--groove);
        border-radius: var(--radius);
        background: var(--surface);
        overflow: hidden;
        aspect-ratio: 1 / 1;
        display: flex; align-items: center; justify-content: center;
        position: sticky; top: 1rem;
    }
    .cover-placeholder {
        color: var(--text-dim);
        font-size: 5rem;
        text-align: center;
        line-height: 1;
    }
    .cover-placeholder small {
        display: block;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.7rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-top: 0.5rem;
    }

    /* ── Queue ── */
    .queue-wrap {
        background: var(--surface);
        border: 1px solid var(--groove);
        border-radius: var(--radius);
        padding: 0.8rem;
        max-height: 260px;
        overflow-y: auto;
    }
    .q-item {
        display: flex; align-items: baseline; gap: 0.6rem;
        background: var(--surface2);
        border-left: 3px solid var(--accent);
        border-radius: 0 2px 2px 0;
        padding: 0.5rem 0.8rem;
        margin-bottom: 0.35rem;
        transition: border-color 0.2s;
    }
    .q-item:hover { border-left-color: var(--cyan); }
    .q-num {
        font-family: 'Bebas Neue', sans-serif;
        color: var(--accent-light); font-size: 1rem;
        letter-spacing: 2px; min-width: 2ch;
    }
    .q-title { color: var(--text); font-size: 0.9rem; font-weight: 500; }
    .q-artist { color: var(--text-dim); font-size: 0.8rem; font-style: italic; margin-left: auto; }

    /* ── Log console ── */
    .log-console {
        background: #050508;
        border: 1px solid #1a1d30;
        border-radius: var(--radius);
        padding: 1rem 1.2rem;
        font-family: 'JetBrains Mono', 'Courier New', monospace;
        font-size: 0.78rem;
        color: #6bffea;
        max-height: 220px;
        overflow-y: auto;
        white-space: pre-wrap;
        word-break: break-all;
        line-height: 1.6;
    }
    .log-line-err  { color: #ff6b6b; }
    .log-line-info { color: #6bb3ff; }
    .log-line-ok   { color: #6bffea; }
    .log-line-warn { color: #fbbf24; }

    /* ── Trim section ── */
    .trim-section {
        background: var(--surface);
        border: 1px solid var(--groove);
        border-top: 3px solid var(--accent);
        border-radius: var(--radius);
        padding: 1.2rem 1.4rem;
        margin-top: 1rem;
    }

    /* ── Status pills ── */
    .pill {
        display: inline-block;
        padding: 0.15rem 0.7rem;
        border-radius: 20px;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.75rem;
        font-weight: 500;
        letter-spacing: 1px;
    }
    .pill-ok   { background: rgba(16,185,129,0.12); color: var(--success); border: 1px solid rgba(16,185,129,0.3); }
    .pill-err  { background: rgba(239,68,68,0.12);  color: var(--error);   border: 1px solid rgba(239,68,68,0.3); }
    .pill-warn { background: rgba(245,158,11,0.12); color: var(--warn);    border: 1px solid rgba(245,158,11,0.3); }
    .pill-info { background: rgba(109,40,217,0.12); color: var(--accent-light); border: 1px solid rgba(109,40,217,0.3); }

    /* ── Streamlit widget overrides ── */
    .stTextInput  > label,
    .stSelectbox  > label,
    .stTextArea   > label,
    .stNumberInput > label,
    .stFileUploader > label {
        color: var(--text-dim) !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.7rem !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        font-weight: 500 !important;
    }
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: var(--surface2) !important;
        color: var(--text) !important;
        border: 1px solid #1c2035 !important;
        border-radius: var(--radius) !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 1px var(--accent-glow) !important;
    }
    .stTextArea > div > textarea {
        background: var(--surface2) !important;
        color: var(--text) !important;
        border: 1px solid #1c2035 !important;
        border-radius: var(--radius) !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    div[data-baseweb="select"] > div {
        background: var(--surface2) !important;
        border-color: #1c2035 !important;
        border-radius: var(--radius) !important;
        color: var(--text) !important;
    }
    div[data-baseweb="select"] li {
        background: var(--surface3) !important;
        color: var(--text) !important;
    }
    div[data-baseweb="select"] li:hover {
        background: var(--surface2) !important;
        color: var(--accent-light) !important;
    }
    .stButton > button {
        background: var(--grad) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: var(--radius) !important;
        font-family: 'Bebas Neue', sans-serif !important;
        letter-spacing: 4px !important;
        font-size: 1.05rem !important;
        padding: 0.5rem 1.5rem !important;
        width: 100% !important;
        transition: all 0.15s ease !important;
    }
    .stButton > button:hover {
        filter: brightness(1.15) !important;
        box-shadow: 0 4px 24px var(--accent-glow) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:active { transform: translateY(0) !important; }
    div[data-testid="stTabs"] button {
        font-family: 'Bebas Neue', sans-serif !important;
        letter-spacing: 4px !important;
        color: var(--text-dim) !important;
        font-size: 1.1rem !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: var(--accent-light) !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"]::after {
        background: var(--grad) !important;
    }
    .stProgress > div > div > div { background: var(--grad) !important; }
    .stAlert { border-radius: var(--radius) !important; }
    div[data-testid="stFileUploader"] {
        background: var(--surface2) !important;
        border: 1px dashed #1c2035 !important;
        border-radius: var(--radius) !important;
    }
    div[data-testid="stFileUploader"]:hover {
        border-color: var(--accent) !important;
    }
    .stSpinner > div { border-top-color: var(--cyan) !important; }
    .stCheckbox > label > span { color: var(--text) !important; }
    div[data-baseweb="checkbox"] > div { border-color: var(--accent) !important; }
    div[data-baseweb="checkbox"][aria-checked="true"] > div {
        background: var(--accent) !important;
        border-color: var(--accent) !important;
    }
    .stRadio > label > div { color: var(--text) !important; }

    /* ── Hide Streamlit chrome ── */
    #MainMenu, footer, header, .stDeployButton { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)
import streamlit as st

# ══════════════════════════════════════════════════════════════════
#  CSS — DARK VINYL AESTHETIC
# ══════════════════════════════════════════════════════════════════
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg:          #080808;
        --surface:     #111111;
        --surface2:    #181818;
        --surface3:    #202020;
        --gold:        #c9a84c;
        --gold-light:  #e8c86a;
        --gold-dim:    #7a6530;
        --gold-glow:   rgba(201,168,76,0.12);
        --text:        #ddd6c8;
        --text-dim:    #5e5850;
        --groove:      #1e1e1e;
        --success:     #4caf87;
        --error:       #c0392b;
        --warn:        #e67e22;
        --radius:      3px;
    }

    /* ── Base ── */
    .stApp { background: var(--bg) !important; font-family: 'DM Sans', sans-serif; }
    .block-container { max-width: 1300px !important; padding: 0 2rem 4rem !important; }
    p, li, span { color: var(--text); font-family: 'DM Sans', sans-serif; }
    h1,h2,h3,h4 {
        font-family: 'Bebas Neue', sans-serif !important;
        letter-spacing: 3px !important;
        color: var(--gold) !important;
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
        color: var(--gold);
        text-shadow: 0 0 60px var(--gold-glow), 0 0 120px var(--gold-glow);
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
        color: var(--gold);
        border-left: 3px solid var(--gold);
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
        border-left: 3px solid var(--gold-dim);
        border-radius: 0 2px 2px 0;
        padding: 0.5rem 0.8rem;
        margin-bottom: 0.35rem;
        transition: border-color 0.2s;
    }
    .q-item:hover { border-left-color: var(--gold); }
    .q-num {
        font-family: 'Bebas Neue', sans-serif;
        color: var(--gold); font-size: 1rem;
        letter-spacing: 2px; min-width: 2ch;
    }
    .q-title { color: var(--text); font-size: 0.9rem; font-weight: 500; }
    .q-artist { color: var(--text-dim); font-size: 0.8rem; font-style: italic; margin-left: auto; }

    /* ── Log console ── */
    .log-console {
        background: #050505;
        border: 1px solid #1a1a1a;
        border-radius: var(--radius);
        padding: 1rem 1.2rem;
        font-family: 'JetBrains Mono', 'Courier New', monospace;
        font-size: 0.78rem;
        color: #6bff6b;
        max-height: 220px;
        overflow-y: auto;
        white-space: pre-wrap;
        word-break: break-all;
        line-height: 1.6;
    }
    .log-line-err  { color: #ff6b6b; }
    .log-line-info { color: #6bc8ff; }
    .log-line-ok   { color: #6bff6b; }
    .log-line-warn { color: #ffa84c; }

    /* ── Trim section ── */
    .trim-section {
        background: var(--surface);
        border: 1px solid var(--groove);
        border-top: 3px solid var(--gold-dim);
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
    .pill-ok   { background: rgba(76,175,135,0.15); color: var(--success); border: 1px solid rgba(76,175,135,0.3); }
    .pill-err  { background: rgba(192,57,43,0.15);  color: var(--error);   border: 1px solid rgba(192,57,43,0.3); }
    .pill-warn { background: rgba(230,126,34,0.15); color: var(--warn);    border: 1px solid rgba(230,126,34,0.3); }
    .pill-info { background: rgba(201,168,76,0.1);  color: var(--gold);    border: 1px solid rgba(201,168,76,0.25); }

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
        border: 1px solid #252525 !important;
        border-radius: var(--radius) !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--gold-dim) !important;
        box-shadow: 0 0 0 1px var(--gold-glow) !important;
    }
    .stTextArea > div > textarea {
        background: var(--surface2) !important;
        color: var(--text) !important;
        border: 1px solid #252525 !important;
        border-radius: var(--radius) !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    div[data-baseweb="select"] > div {
        background: var(--surface2) !important;
        border-color: #252525 !important;
        border-radius: var(--radius) !important;
        color: var(--text) !important;
    }
    div[data-baseweb="select"] li {
        background: var(--surface3) !important;
        color: var(--text) !important;
    }
    div[data-baseweb="select"] li:hover {
        background: var(--surface2) !important;
        color: var(--gold) !important;
    }
    .stButton > button {
        background: var(--gold) !important;
        color: #080808 !important;
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
        background: var(--gold-light) !important;
        box-shadow: 0 4px 24px var(--gold-glow) !important;
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
        color: var(--gold) !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"]::after {
        background: var(--gold) !important;
    }
    .stProgress > div > div > div { background: var(--gold) !important; }
    .stAlert { border-radius: var(--radius) !important; }
    div[data-testid="stFileUploader"] {
        background: var(--surface2) !important;
        border: 1px dashed #2a2a2a !important;
        border-radius: var(--radius) !important;
    }
    div[data-testid="stFileUploader"]:hover {
        border-color: var(--gold-dim) !important;
    }
    .stSpinner > div { border-top-color: var(--gold) !important; }
    .stCheckbox > label > span { color: var(--text) !important; }
    div[data-baseweb="checkbox"] > div { border-color: var(--gold-dim) !important; }
    div[data-baseweb="checkbox"][aria-checked="true"] > div {
        background: var(--gold) !important;
        border-color: var(--gold) !important;
    }
    .stRadio > label > div { color: var(--text) !important; }

    /* ── Hide Streamlit chrome ── */
    #MainMenu, footer, header, .stDeployButton { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)
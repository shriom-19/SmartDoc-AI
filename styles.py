import streamlit as st


# ==========================================================
# NEON DARK THEME - Shared CSS
# ==========================================================

NEON_CSS = """
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap');

/* ---- Variables ---- */
:root {
    --bg:        #050816;
    --bg2:       #0D1325;
    --card:      #0a1628;
    --card2:     #111f3a;
    --cyan:      #00E5FF;
    --cyan2:     #00b8cc;
    --purple:    #9D4EDD;
    --purple2:   #7b3db0;
    --green:     #39FF14;
    --green2:    #28c40e;
    --pink:      #FF006E;
    --yellow:    #FFD60A;
    --text:      #F0F4FF;
    --muted:     #8892a4;
    --border:    rgba(0,229,255,0.18);
}

/* ---- Reset & Base ---- */
#MainMenu, footer, header { visibility: hidden; }

html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif !important;
    background: var(--bg) !important;
    color: var(--text) !important;
}

.stApp {
    background: linear-gradient(135deg, #050816 0%, #0D1325 50%, #0a1020 100%) !important;
    color: var(--text);
}

/* ---- Scrollbar ---- */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg2); }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, var(--cyan), var(--purple));
    border-radius: 20px;
}

/* ---- Sidebar ---- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060d1a 0%, #091120 100%) !important;
    border-right: 1px solid var(--border) !important;
    box-shadow: 4px 0 20px rgba(0,229,255,0.08) !important;
}

[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] a {
    color: var(--text) !important;
}

[data-testid="stSidebarNav"] a {
    color: var(--muted) !important;
    border-radius: 8px !important;
    transition: all 0.2s !important;
}

[data-testid="stSidebarNav"] a:hover,
[data-testid="stSidebarNav"] a[aria-selected="true"] {
    color: var(--cyan) !important;
    background: rgba(0,229,255,0.08) !important;
    text-shadow: 0 0 8px var(--cyan);
}

/* ---- Block Container ---- */
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 1300px;
}

/* ---- Headings ---- */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter', sans-serif !important;
    color: var(--text) !important;
}

/* ---- Buttons ---- */
.stButton > button {
    background: linear-gradient(90deg, var(--cyan), var(--purple)) !important;
    color: #000 !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    border: none !important;
    border-radius: 10px !important;
    height: 46px !important;
    letter-spacing: 0.5px;
    transition: all 0.25s ease !important;
    box-shadow: 0 0 0px var(--cyan);
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 0 18px rgba(0,229,255,0.55), 0 0 35px rgba(157,78,221,0.3) !important;
    filter: brightness(1.1);
}

.stButton > button:active {
    transform: translateY(0px) !important;
}

/* Secondary button */
[data-testid="baseButton-secondary"] {
    background: transparent !important;
    border: 1px solid var(--purple) !important;
    color: var(--purple) !important;
    font-weight: 600 !important;
}

[data-testid="baseButton-secondary"]:hover {
    background: rgba(157,78,221,0.12) !important;
    box-shadow: 0 0 15px rgba(157,78,221,0.4) !important;
    color: var(--purple) !important;
}

/* Download button */
.stDownloadButton > button {
    background: linear-gradient(90deg, var(--green2), #1a8a0a) !important;
    color: #000 !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
}

.stDownloadButton > button:hover {
    box-shadow: 0 0 18px rgba(57,255,20,0.5) !important;
    transform: translateY(-2px) !important;
}

/* ---- Metrics ---- */
[data-testid="metric-container"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 18px 16px !important;
    box-shadow: 0 0 14px rgba(0,229,255,0.1), inset 0 0 20px rgba(0,229,255,0.03) !important;
    transition: all 0.3s;
}

[data-testid="metric-container"]:hover {
    border-color: var(--cyan) !important;
    box-shadow: 0 0 22px rgba(0,229,255,0.25) !important;
    transform: translateY(-2px);
}

[data-testid="metric-container"] label {
    color: var(--muted) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}

[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: var(--cyan) !important;
    font-size: 28px !important;
    font-weight: 700 !important;
    text-shadow: 0 0 10px rgba(0,229,255,0.4);
}

/* ---- Divider ---- */
hr {
    border: none !important;
    border-top: 1px solid rgba(0,229,255,0.15) !important;
    margin: 1.2rem 0 !important;
}

/* ---- Alerts ---- */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border-left-width: 4px !important;
    backdrop-filter: blur(6px) !important;
}

/* ---- Text Input / Select / Textarea ---- */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--cyan) !important;
    box-shadow: 0 0 12px rgba(0,229,255,0.2) !important;
}

/* ---- File Uploader ---- */
[data-testid="stFileUploader"] {
    background: var(--card) !important;
    border: 2px dashed var(--border) !important;
    border-radius: 14px !important;
    transition: all 0.3s;
}

[data-testid="stFileUploader"]:hover {
    border-color: var(--cyan) !important;
    box-shadow: 0 0 20px rgba(0,229,255,0.15) !important;
}

/* ---- DataFrames / Tables ---- */
.stDataFrame {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid var(--border) !important;
}

/* ---- Expander ---- */
.stExpander {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    margin-bottom: 10px !important;
}

.stExpander:hover {
    border-color: rgba(0,229,255,0.35) !important;
    box-shadow: 0 0 12px rgba(0,229,255,0.1) !important;
}

/* ---- Progress Bar ---- */
[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, var(--cyan), var(--purple)) !important;
    border-radius: 4px !important;
    box-shadow: 0 0 8px var(--cyan) !important;
}

[data-testid="stProgressBar"] {
    background: rgba(255,255,255,0.08) !important;
    border-radius: 4px !important;
}

/* ---- JSON Viewer ---- */
.stJson {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}

/* ===========================================================
   CUSTOM COMPONENT CLASSES
   =========================================================== */

.neon-hero {
    text-align: center;
    font-family: 'Orbitron', 'Inter', sans-serif;
    font-size: 52px;
    font-weight: 900;
    background: linear-gradient(90deg, #00E5FF 0%, #9D4EDD 50%, #39FF14 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 8px 0 4px;
    letter-spacing: -1px;
    filter: drop-shadow(0 0 20px rgba(0,229,255,0.3));
}

.neon-subtitle {
    text-align: center;
    font-size: 17px;
    color: var(--muted);
    margin-bottom: 20px;
    letter-spacing: 0.3px;
}

.neon-card {
    background: linear-gradient(135deg, var(--card) 0%, var(--card2) 100%);
    padding: 20px 22px;
    border-radius: 16px;
    margin-bottom: 16px;
    border: 1px solid var(--border);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.neon-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--cyan), transparent);
    opacity: 0.6;
}

.neon-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 32px rgba(0,229,255,0.2), 0 0 0 1px rgba(0,229,255,0.15);
}

.neon-card h4 {
    font-size: 12px !important;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--muted) !important;
    margin: 0 0 8px !important;
    font-weight: 500 !important;
}

.neon-card h2 {
    font-size: 26px !important;
    font-weight: 700 !important;
    margin: 0 !important;
}

.neon-card.cyan  { border-left: 3px solid var(--cyan);   }
.neon-card.cyan h2  { color: var(--cyan) !important; text-shadow: 0 0 10px rgba(0,229,255,0.5); }
.neon-card.purple { border-left: 3px solid var(--purple); }
.neon-card.purple h2 { color: var(--purple) !important; text-shadow: 0 0 10px rgba(157,78,221,0.5); }
.neon-card.green { border-left: 3px solid var(--green);  }
.neon-card.green h2  { color: var(--green) !important; text-shadow: 0 0 10px rgba(57,255,20,0.5); }

.activity-card {
    background: rgba(10,22,40,0.8);
    border: 1px solid var(--border);
    border-left: 4px solid var(--green);
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 12px;
    transition: all 0.25s;
}

.activity-card:hover {
    background: rgba(14,28,50,0.9);
    box-shadow: 0 0 16px rgba(57,255,20,0.15);
    transform: translateX(3px);
}

.activity-card b { color: var(--cyan); font-size: 15px; }
.activity-card span { color: var(--muted); font-size: 13px; }

.storage-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 22px;
    transition: all 0.3s;
}

.storage-card:hover { box-shadow: 0 0 20px rgba(0,229,255,0.15); }

.storage-card h3 {
    color: var(--cyan) !important;
    margin-bottom: 14px !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

.storage-card .item {
    color: var(--text);
    padding: 6px 0;
    font-size: 14px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    display: flex;
    align-items: center;
    gap: 8px;
}

.neon-footer {
    text-align: center;
    padding: 22px;
    border-radius: 16px;
    background: linear-gradient(135deg, rgba(0,229,255,0.07), rgba(157,78,221,0.07));
    border: 1px solid var(--border);
    color: var(--muted);
    font-size: 14px;
    margin-top: 10px;
    box-shadow: 0 0 30px rgba(0,229,255,0.07);
}

.neon-footer b { color: var(--cyan); }
.neon-footer .tagline { color: var(--text); font-size: 17px; font-weight: 700; margin-bottom: 6px; }
.neon-footer .pills {
    display: flex; justify-content: center;
    gap: 10px; flex-wrap: wrap; margin-top: 12px;
}
.neon-footer .pill {
    background: rgba(0,229,255,0.1);
    border: 1px solid rgba(0,229,255,0.2);
    border-radius: 20px;
    padding: 3px 14px;
    font-size: 12px;
    color: var(--cyan);
    font-weight: 500;
    letter-spacing: 0.5px;
}

</style>
"""


def load_css():
    """Inject the global neon dark theme into any Streamlit page."""
    st.markdown(NEON_CSS, unsafe_allow_html=True)
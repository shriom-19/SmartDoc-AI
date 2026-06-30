# pyrefly: ignore [missing-import]

from pandas.core import apply
import streamlit as st

from database.save_document import DocumentDatabase
from styles import load_css

# ==========================================================
# CONFIG
# ==========================================================

st.set_page_config(
    page_title="SmartDoc AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()

# ==========================================================
# SAFE DB INIT
# ==========================================================

@st.cache_resource(show_spinner=False)
def get_database():
    try:
        return DocumentDatabase()
    except Exception as e:
        return None

db = get_database()

def get_documents():
    if db is None:
        return []
    try:
        return db.get_all_documents()
    except Exception:
        return []

documents = get_documents()
total_docs = len(documents)

# ==========================================================
# HELPERS
# ==========================================================

def neon_card(title, value, color="cyan"):
    st.markdown(f"""
    <div class="neon-card {color}">
        <h4>{title}</h4>
        <h2>{value}</h2>
    </div>
    """, unsafe_allow_html=True)

# ==========================================================
# HERO
# ==========================================================

st.markdown('<div class="neon-hero">🧠 SmartDoc AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="neon-subtitle">AI-Powered Intelligent Document Understanding Platform</div>',
    unsafe_allow_html=True
)
st.divider()

# ==========================================================
# QUICK ACTIONS
# ==========================================================

st.subheader("🚀 Quick Actions")

c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("📤 Upload", use_container_width=True):
        st.switch_page("pages/1_Upload.py")

with c2:
    if st.button("📁 Documents", use_container_width=True):
        st.switch_page("pages/2_Documents.py")

with c3:
    if st.button("📊 Dashboard", use_container_width=True):
        st.switch_page("pages/3_Dashboard.py")

with c4:
    if st.button("⚙ Settings", use_container_width=True):
        st.switch_page("pages/4_Settings.py")

st.divider()

# ==========================================================
# DASHBOARD SUMMARY
# ==========================================================

st.subheader("📊 Dashboard Summary")

m1, m2, m3, m4 = st.columns(4)

with m1:
    neon_card("📄 Documents", total_docs, "cyan")

with m2:
    neon_card("🧠 Classes", "18", "purple")

with m3:
    neon_card("👁 OCR Engine", "EasyOCR", "green")

with m4:
    neon_card("💾 Database", "MongoDB", "cyan")

st.divider()

# ==========================================================
# SYSTEM STATUS
# ==========================================================

st.subheader("🟢 System Status")

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.success("🧠 AI Model Ready")

with s2:
    st.success("👁 OCR Ready")

with s3:
    if db is not None:
        st.success("💾 MongoDB Connected")
    else:
        st.error("💾 MongoDB Disconnected")

with s4:
    st.success("📄 PDF Support Enabled")

st.divider()

# ==========================================================
# RECENT DOCUMENTS
# ==========================================================

st.subheader("📁 Recent Documents")

if documents:
    recent = sorted(
        documents,
        key=lambda x: str(x.get("created_at", "")),
        reverse=True
    )[:5]

    table = []
    for doc in recent:
        conf = doc.get("classification", {}).get("confidence", 0)
        table.append({
            "Document": doc.get("document_type", "Unknown").replace("_", " ").title(),
            "Confidence": f"{conf * 100:.1f}%",
            "Created": str(doc.get("created_at", "-"))[:19]
        })

    st.dataframe(table, use_container_width=True, hide_index=True)

else:
    st.info("No documents processed yet. Upload your first document to get started.")

st.divider()

# ==========================================================
# DOCUMENT DISTRIBUTION
# ==========================================================

st.subheader("📈 Document Distribution")

if documents:
    counts = {}
    for doc in documents:
        dtype = doc.get("document_type", "Unknown")
        counts[dtype] = counts.get(dtype, 0) + 1
    st.bar_chart(counts)
else:
    st.info("Upload documents to view analytics.")

st.divider()

# ==========================================================
# RECENT ACTIVITY
# ==========================================================

st.subheader("🕒 Recent Activity")

if documents:
    recent = sorted(
        documents,
        key=lambda x: str(x.get("created_at", "")),
        reverse=True
    )[:5]

    for doc in recent:
        dtype = doc.get("document_type", "Unknown").replace("_", " ").title()
        created = str(doc.get("created_at", ""))[:19]
        st.markdown(f"""
        <div class="activity-card">
            <b>📄 {dtype}</b><br>
            <span>✔ Processed Successfully &nbsp;•&nbsp; {created}</span>
        </div>
        """, unsafe_allow_html=True)

else:
    st.info("No recent activity available.")

st.divider()

# ==========================================================
# MODEL INFORMATION
# ==========================================================

st.subheader("🧠 AI Information")

ai1, ai2, ai3 = st.columns(3)

with ai1:
    neon_card("Model Architecture", "ResNet50", "purple")

with ai2:
    neon_card("Document Classes", "18", "cyan")

with ai3:
    neon_card("OCR Engine", "EasyOCR", "green")

st.divider()

# ==========================================================
# STORAGE
# ==========================================================

st.subheader("💾 Storage")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
<div class="storage-card">
<h3>🗄 MongoDB</h3>
<div class="item">✔ &nbsp;Atlas Cloud Connected</div>
<div class="item">✔ &nbsp;Document Storage</div>
<div class="item">✔ &nbsp;JSON Record Format</div>
<div class="item">✔ &nbsp;Fast Retrieval</div>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div class="storage-card">
<h3>📂 Supported Formats</h3>
<div class="item">🖼 &nbsp;JPG / JPEG / PNG</div>
<div class="item">🖼 &nbsp;BMP / TIFF / TIF</div>
<div class="item">📄 &nbsp;PDF (Page 1)</div>
<div class="item">🔍 &nbsp;Auto-classify on Upload</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("""
<div class="neon-footer">
    <div class="tagline">🧠 <b>SmartDoc AI</b></div>
    Intelligent Document Understanding Platform<br>
    <div class="pills">
        <span class="pill">Classify</span>
        <span class="pill">OCR</span>
        <span class="pill">Extract</span>
        <span class="pill">Store</span>
        <span class="pill">Analyze</span>
    </div>
</div>
""", unsafe_allow_html=True)


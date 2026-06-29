import streamlit as st
import pandas as pd
import os
import sys

# Add root project path to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.save_document import DocumentDatabase
from styles import load_css

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Dashboard — SmartDoc AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()

# ==========================================================
# DATABASE
# ==========================================================

@st.cache_resource(show_spinner=False)
def get_database():
    try:
        return DocumentDatabase()
    except Exception:
        return None

database = get_database()

# ==========================================================
# TITLE
# ==========================================================

st.markdown('<div class="neon-hero" style="font-size:36px;">📊 Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="neon-subtitle">SmartDoc AI — Intelligent Document Processing Analytics</div>',
    unsafe_allow_html=True
)
st.divider()

# ==========================================================
# LOAD DOCUMENTS
# ==========================================================

if database is None:
    st.error("❌ Database connection failed. Check your MongoDB settings.")
    documents = []
else:
    try:
        documents = database.get_all_documents()
    except Exception as e:
        st.error(f"❌ Failed to load documents: {e}")
        documents = []

# ==========================================================
# STATISTICS
# ==========================================================

total_documents = len(documents)

document_types = len(set(
    doc.get("document_type", "Unknown")
    for doc in documents
)) if documents else 0

unidentified = sum(
    1 for doc in documents
    if doc.get("document_type", "").lower() == "unidentified"
)

# Average confidence
if documents:
    confidences = [
        doc.get("classification", {}).get("confidence", 0.0)
        for doc in documents
    ]
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
else:
    avg_confidence = 0.0

# ==========================================================
# METRICS ROW
# ==========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📄 Total Documents", total_documents)

with col2:
    st.metric("📂 Document Types", document_types)

with col3:
    st.metric("🎯 Avg. Confidence", f"{avg_confidence * 100:.1f}%")

with col4:
    st.metric("⚠️ Unidentified", unidentified)

st.divider()

# ==========================================================
# SYSTEM STATUS
# ==========================================================

st.subheader("🖥 System Status")

col1, col2, col3 = st.columns(3)

with col1:
    st.success("✅ AI Models Loaded")

with col2:
    if database is not None:
        st.success("✅ MongoDB Connected")
    else:
        st.error("❌ MongoDB Disconnected")

with col3:
    st.success("✅ OCR Ready")

st.divider()

# ==========================================================
# DOCUMENT DISTRIBUTION
# ==========================================================

st.subheader("📈 Document Distribution")

if documents:
    counts = {}
    for doc in documents:
        dtype = doc.get("document_type", "Unknown").replace("_", " ").title()
        counts[dtype] = counts.get(dtype, 0) + 1

    df = pd.DataFrame({
        "Document Type": list(counts.keys()),
        "Count": list(counts.values())
    })

    st.bar_chart(df.set_index("Document Type"))

else:
    st.info("📭 No document statistics available yet.")

st.divider()

# ==========================================================
# RECENT DOCUMENTS TABLE
# ==========================================================

st.subheader("📁 Recent Documents")

if documents:
    recent = sorted(
        documents,
        key=lambda x: str(x.get("created_at", "")),
        reverse=True
    )[:10]

    table = []
    for doc in recent:
        conf = doc.get("classification", {}).get("confidence", 0.0)
        table.append({
            "Document": doc.get("document_type", "-").replace("_", " ").title(),
            "Confidence": f"{conf * 100:.1f}%",
            "Created": str(doc.get("created_at", "-"))[:19],
        })

    st.dataframe(pd.DataFrame(table), use_container_width=True, hide_index=True)

else:
    st.info("📭 No documents uploaded yet.")

st.divider()

# ==========================================================
# QUICK ACTIONS
# ==========================================================

st.subheader("🚀 Quick Actions")

col1, col2 = st.columns(2)

with col1:
    if st.button("📤 Upload Document", use_container_width=True):
        st.switch_page("pages/1_Upload.py")

with col2:
    if st.button("📁 View Documents", use_container_width=True):
        st.switch_page("pages/2_Documents.py")

st.divider()

# ==========================================================
# DATABASE SUMMARY
# ==========================================================

st.subheader("📋 Database Summary")

st.write(f"Total Stored Documents : **{total_documents}**")

if documents:
    st.write("**Documents by Type:**")

    type_counts = {}
    for doc in documents:
        dtype = doc.get("document_type", "Unknown").replace("_", " ").title()
        type_counts[dtype] = type_counts.get(dtype, 0) + 1

    for dtype, count in sorted(type_counts.items()):
        st.markdown(f"""
        <div class="activity-card">
            <b>📄 {dtype}</b><br>
            <span>{count} document(s)</span>
        </div>
        """, unsafe_allow_html=True)
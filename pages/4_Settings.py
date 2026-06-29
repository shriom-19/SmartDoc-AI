import os
import sys
import streamlit as st

# Add root project path to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.mongodb import MongoDB
from database.save_document import DocumentDatabase

# ==========================================================
# CONFIG
# ==========================================================

st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide"
)

database = DocumentDatabase()
mongo = MongoDB()

DATABASE_STATUS = mongo.test_connection()
OCR_STATUS = True

# ==========================================================
# TITLE
# ==========================================================

st.title("⚙️ Settings")

st.write(
    "Manage SmartDoc AI preferences, storage and application settings."
)

st.divider()

# ==========================================================
# APPLICATION
# ==========================================================

st.subheader("📦 Application")

col1, col2 = st.columns(2)

with col1:

    st.write("**Application**")
    st.write("SmartDoc AI")

    st.write("**Version**")
    st.write("1.0.0")

with col2:

    st.write("**Theme**")
    st.write("Cyber Dark")

    st.write("**Storage**")
    st.write("MongoDB")

st.divider()

# ==========================================================
# STATUS
# ==========================================================

st.subheader("🖥 System Status")

c1, c2 = st.columns(2)

with c1:

    if OCR_STATUS:
        st.success("✅ Text Recognition Ready")
    else:
        st.error("❌ Text Recognition Error")

with c2:

    if DATABASE_STATUS:
        st.success("✅ Storage Connected")
    else:
        st.error("❌ Storage Disconnected")

st.divider()

# ==========================================================
# DATABASE
# ==========================================================

st.subheader("💾 Document Library")

st.metric(
    "Documents Stored",
    database.total_documents()
)

st.divider()

# ==========================================================
# MAINTENANCE
# ==========================================================

st.subheader("🛠 Maintenance")

c1, c2 = st.columns(2)

with c1:

    if st.button(
        "🔄 Refresh",
        use_container_width=True
    ):
        st.rerun()

with c2:

    if st.button(
        "🗑 Clear Library",
        use_container_width=True
    ):

        deleted = database.delete_all_documents()

        st.success(
            f"{deleted} document(s) removed."
        )

        st.rerun()

st.divider()

# ==========================================================
# ABOUT
# ==========================================================

st.subheader("ℹ About SmartDoc AI")

st.info(
"""
SmartDoc AI is an intelligent document processing platform.

### Features

• Intelligent document classification

• Automatic text recognition

• Key information extraction

• Secure document storage

• Search & analytics

• Export processed results
"""
)

st.divider()

# ==========================================================
# FOOTER
# ==========================================================

st.caption(
    "SmartDoc AI • Version 1.0 • Intelligent Document Processing Platform"
)
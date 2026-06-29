import json
import os
import sys

import streamlit as st

# Add root project path to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.save_document import DocumentDatabase
from styles import load_css

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Documents — SmartDoc AI",
    page_icon="📁",
    layout="wide"
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

st.markdown('<div class="neon-hero" style="font-size:36px;">📁 Documents</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="neon-subtitle">Browse, search and manage your analyzed documents.</div>',
    unsafe_allow_html=True
)
st.divider()

# ==========================================================
# LOAD DOCUMENTS
# ==========================================================

if database is None:
    st.error("❌ Database connection failed. Check your MongoDB settings.")
    st.stop()

try:
    documents = database.get_all_documents()
except Exception as e:
    st.error(f"❌ Failed to load documents: {e}")
    documents = []

# ==========================================================
# FILTERS
# ==========================================================

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    search = st.text_input("🔍 Search by type, text or keyword…")

with col2:
    document_type = st.selectbox(
        "📄 Document Type",
        [
            "All",
            "Advertisement",
            "Adhar",
            "Budget",
            "Email",
            "File Folder",
            "Form",
            "Handwritten",
            "Invoice",
            "Letter",
            "Memo",
            "News Article",
            "Pan",
            "Presentation",
            "Questionnaire",
            "Resume",
            "Scientific Publication",
            "Scientific Report",
            "Specification",
            "Unidentified",
        ]
    )

with col3:
    sort_by = st.selectbox("Sort", ["Newest", "Oldest"])

# ==========================================================
# SORT
# ==========================================================

documents = sorted(
    documents,
    key=lambda x: str(x.get("created_at", "")),
    reverse=(sort_by == "Newest")
)

# ==========================================================
# FILTER
# ==========================================================

filtered_documents = []

for doc in documents:

    if document_type != "All":
        if doc.get("document_type", "").lower() != document_type.lower():
            continue

    if search:
        try:
            doc_json = json.dumps(doc, default=str).lower()
        except Exception:
            doc_json = ""
        if search.lower() not in doc_json:
            continue

    filtered_documents.append(doc)

# ==========================================================
# RESULTS COUNT
# ==========================================================

st.divider()

if not filtered_documents:
    st.info("📭 No matching documents found.")
    st.stop()

st.success(f"✅ {len(filtered_documents)} document(s) found.")
st.divider()

# ==========================================================
# DOCUMENT CARDS
# ==========================================================

for index, doc in enumerate(filtered_documents):

    confidence = doc.get("classification", {}).get("confidence", 0.0)
    doc_type   = doc.get("document_type", "Unknown").replace("_", " ").title()
    created    = str(doc.get("created_at", "-"))[:19]

    expander_title = f"📄 {doc_type}  •  {confidence * 100:.1f}%  •  {created}"

    with st.expander(expander_title):

        # ---- Summary ----
        st.markdown(f"""
<div class="neon-card cyan">
<h4>📌 Summary</h4>
<h2 style="font-size:15px !important; color: var(--text) !important; text-shadow:none;">
{doc_type} — analyzed successfully. Text recognition and key-information extraction completed.
</h2>
</div>
""", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Document Type", doc_type)

        with col2:
            st.metric("Confidence", f"{confidence * 100:.2f}%")
            st.progress(min(float(confidence), 1.0))
            if confidence >= 0.90:
                st.success("🟢 High Confidence")
            elif confidence >= 0.70:
                st.warning("🟡 Medium Confidence")
            else:
                st.error("🔴 Low Confidence")

        with col3:
            st.metric("Created", created)

        st.divider()

        # ---- Key Information ----
        st.subheader("📋 Key Information")
        extracted = doc.get("extracted_data", {})
        if extracted:
            st.json(extracted)
        else:
            st.info("No structured data available.")

        # ---- Document Text ----
        if "ocr" in doc:
            st.divider()
            st.subheader("📝 Document Text")
            st.text_area(
                "Recognized Text",
                doc.get("ocr", {}).get("text", ""),
                height=220,
                key=f"text_{index}"
            )

        st.divider()

        # ---- Export / Delete ----
        try:
            json_data = json.dumps(doc, indent=4, default=str)
        except Exception:
            json_data = "{}"

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                "📥 Export Results (JSON)",
                data=json_data,
                file_name=f"{doc.get('_id', 'document')}.json",
                mime="application/json",
                use_container_width=True,
                key=f"download_{index}"
            )

        with col2:
            if st.button(
                "🗑 Delete",
                use_container_width=True,
                key=f"delete_{index}",
                type="secondary"
            ):
                doc_id = doc.get("_id", "")
                if doc_id:
                    try:
                        database.delete_document(doc_id)
                        st.success("🗑 Document deleted successfully.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Delete failed: {e}")
                else:
                    st.error("❌ Invalid document ID.")
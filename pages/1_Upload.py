import os
import sys
import json
import time
import tempfile

import streamlit as st
from PIL import Image

# Add root project path to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.save_document import DocumentDatabase
from models.extractor import DocumentProcessingPipeline
from styles import load_css


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Upload • SmartDoc AI",
    page_icon="📤",
    layout="wide"
)

load_css()


# ==========================================================
# CACHE
# ==========================================================

@st.cache_resource(show_spinner=False)
def load_pipeline():
    return DocumentProcessingPipeline()


@st.cache_resource(show_spinner=False)
def load_database():
    return DocumentDatabase()


# ==========================================================
# INITIALIZATION
# ==========================================================

try:
    processor = load_pipeline()
except Exception as e:
    st.error("❌ Failed to initialize AI Pipeline")
    st.exception(e)
    st.stop()


try:
    database = load_database()
except Exception:
    database = None


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==========================================================
# HEADER
# ==========================================================

st.markdown(
    """
    <div class="neon-hero">
        📤 Upload Document
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="neon-subtitle">
        Upload a document and let SmartDoc AI classify,
        extract information and store it automatically.
    </div>
    """,
    unsafe_allow_html=True
)

if database is None:
    st.warning("Database unavailable. Analysis will work but saving is disabled.")

st.divider()

# ==========================================================
# FILE UPLOAD
# ==========================================================

uploaded_file = st.file_uploader(
    "Choose a document",
    type=["jpg", "jpeg", "png", "bmp", "tif", "tiff", "pdf"]
)

if uploaded_file:
    # Clear session state if a new file is uploaded
    if st.session_state.get("last_uploaded_file") != uploaded_file.name:
        st.session_state["last_uploaded_file"] = uploaded_file.name
        if "analysis_result" in st.session_state:
            del st.session_state["analysis_result"]
        if "processing_time" in st.session_state:
            del st.session_state["processing_time"]

    filename = uploaded_file.name
    extension = filename.rsplit(".", 1)[-1].lower()

    # ------------------------------------------------------
    # IMAGE / PDF PREVIEW
    # ------------------------------------------------------

    try:
        if extension == "pdf":
            from pdf2image import convert_from_bytes
            preview = convert_from_bytes(
                uploaded_file.getvalue(),
                first_page=1,
                last_page=1
            )[0]
        else:
            preview = Image.open(uploaded_file).convert("RGB")
    except Exception as e:
        st.error(f"Unable to open document.\n\n{e}")
        st.stop()

    # ------------------------------------------------------
    # SAVE FILE
    # ------------------------------------------------------

    save_path = os.path.join(UPLOAD_FOLDER, filename)
    try:
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    except Exception as e:
        st.error(f"Unable to save document.\n\n{e}")
        st.stop()

    # ------------------------------------------------------
    # PREVIEW LAYOUT
    # ------------------------------------------------------

    left, right = st.columns([1.2, 1])

    with left:
        st.image(
            preview,
            caption=filename,
            use_container_width=True
        )

    with right:
        st.markdown(
            f"""
            <div class="neon-card cyan">
            <h3>📄 File Information</h3>
            <hr>
            <b>Name</b><br>
            {filename}
            <br><br>
            <b>Type</b><br>
            {extension.upper()}
            <br><br>
            <b>Size</b><br>
            {uploaded_file.size/1024:.2f} KB
            </div>
            """,
            unsafe_allow_html=True
        )

    st.success("✅ Document uploaded successfully.")
    st.divider()

    # ==========================================================
    # ANALYZE DOCUMENT
    # ==========================================================

    if st.button("🚀 Analyze Document", use_container_width=True, type="primary"):
        start_time = time.time()
        with st.spinner("Analyzing document..."):
            try:
                # ------------------------------------------
                # PDF
                # ------------------------------------------
                if extension == "pdf":
                    image_path = os.path.join(
                        UPLOAD_FOLDER,
                        f"{os.path.splitext(filename)[0]}.jpg"
                    )
                    preview.save(image_path, "JPEG")
                    result = processor.process(image_path)
                # ------------------------------------------
                # IMAGE
                # ------------------------------------------
                else:
                    result = processor.process(save_path)

                st.session_state["analysis_result"] = result
                st.session_state["processing_time"] = round(time.time() - start_time, 2)

            except Exception as e:
                st.error("❌ Document analysis failed")
                st.exception(e)

    if "analysis_result" in st.session_state:
        result = st.session_state["analysis_result"]
        processing_time = st.session_state.get("processing_time", 0.0)

        classification = result.get("classification", {})
        confidence = classification.get("confidence", 0.0)
        document_type = result.get("document_type", "Unknown").replace("_", " ").title()
        ocr = result.get("ocr", {})
        extracted = result.get("extracted_data", {})

        st.success("✅ Analysis Completed")
        st.divider()

        # ==========================================================
        # RESULTS
        # ==========================================================

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Document Type", document_type)

        with col2:
            st.metric("Confidence", f"{confidence*100:.2f}%")

        with col3:
            st.metric("Processing Time", f"{processing_time:.2f} sec")

        st.progress(min(float(confidence), 1.0))

        if confidence >= 0.90:
            st.success("🟢 High Confidence")
        elif confidence >= 0.70:
            st.warning("🟡 Medium Confidence")
        else:
            st.error("🔴 Low Confidence")

        st.divider()

        # ==========================================================
        # OCR TEXT
        # ==========================================================

        st.subheader("📝 OCR Text")

        st.text_area(
            "Recognized Text",
            value=ocr.get("text", ""),
            height=250
        )

        st.divider()

        # ==========================================================
        # EXTRACTED DATA
        # ==========================================================

        st.subheader("📋 Extracted Information")

        if extracted:
            st.json(extracted)
        else:
            st.info("No structured data extracted.")

        st.divider()

        # ==========================================================
        # EXPORT
        # ==========================================================

        json_result = json.dumps(
            result,
            indent=4,
            default=str
        )

        left, right = st.columns(2)

        with left:
            st.download_button(
                "📥 Download JSON",
                data=json_result,
                file_name=f"{os.path.splitext(filename)[0]}_result.json",
                mime="application/json",
                use_container_width=True
            )

        with right:
            if database:
                if st.button("💾 Save to Database", use_container_width=True):
                    try:
                        document_id = database.save_document(result)
                        st.success(f"Saved Successfully\n\nID : {document_id}")
                    except Exception as e:
                        st.error("Database Save Failed")
                        st.exception(e)
            else:
                st.warning("Database not connected.")

        st.divider()

        # ==========================================================
        # SUMMARY
        # ==========================================================

        st.markdown(
            f"""
<div class="neon-card green">
### ✅ Analysis Complete

**Document Type**
{document_type}
---
**Classification Confidence**
{confidence*100:.2f}%
---
✔ Document Classified

✔ OCR Completed

✔ Information Extracted

✔ Ready for Download / Database
</div>
""",
            unsafe_allow_html=True
        )

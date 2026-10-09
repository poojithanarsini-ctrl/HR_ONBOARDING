from modules.rag_pipeline import index_policy_text
import streamlit as st
if "user" not in st.session_state or st.session_state["user"] is None:
    st.error("Please log in to access the HR Admin page.")
    st.stop()

if st.session_state["user"]["role"] != "hr_admin":
    st.error("Access denied. HR Admin permissions are required.")
    st.stop()
from pathlib import Path
from pypdf import PdfReader
from docx import Document

st.title("🧑‍💼 HR Admin Panel")

st.write("Upload and manage approved HR policy documents.")

st.warning(
    "Only upload documents authorized for use "
    "in the HR knowledge base."
)

DATA_DIR = Path("data/policy_documents")
DATA_DIR.mkdir(parents=True, exist_ok=True)

uploaded_file = st.file_uploader(
    "Upload an HR policy document",
    type=["pdf", "docx"]
)

if uploaded_file is not None:
    if st.button("Save document"):
        safe_name = Path(uploaded_file.name).name
        destination = DATA_DIR / safe_name

        destination.write_bytes(uploaded_file.getvalue())

        try:
            if destination.suffix.lower() == ".pdf":
                reader = PdfReader(str(destination))
                text = "\n".join(
                    page.extract_text() or ""
                    for page in reader.pages
                )
            else:
                document = Document(str(destination))
                text = "\n".join(
                    paragraph.text
                    for paragraph in document.paragraphs
                )

            st.success(f"Saved: {safe_name}")

            if text.strip():
                st.subheader("Document preview")
                st.text_area(
                    "Extracted text",
                    text[:5000],
                    height=250
                )
            else:
                st.warning(
                    "No readable text was found. "
                    "The PDF may be scanned or image-based."
                )

        except Exception:
            st.error(
                "The file was saved, but its text could not "
                "be read. Check that the document is valid."
            )

st.subheader("Uploaded policy documents")

files = sorted(DATA_DIR.glob("*"))

if files:
    for file in files:
        st.write(f"📄 {file.name}")
else:
    st.info("No policy documents have been uploaded yet.")
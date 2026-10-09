from pathlib import Path
from modules.document_processor import extract_text

POLICY_DIR = Path("data/policy_documents")


def test_policy_documents_can_be_read():
    # Find available PDF and DOCX policy files
    files = list(POLICY_DIR.glob("*.docx"))
    files += list(POLICY_DIR.glob("*.pdf"))

    # Check that at least one policy exists
    assert files, "Upload a sample policy document first."

    # Extract text from the first policy
    text = extract_text(files[0])

    # Verify that text was extracted
    assert len(text.strip()) > 0

    # Check that the policy contains expected words
    assert (
        "attendance" in text.lower()
        or "leave" in text.lower()
    )
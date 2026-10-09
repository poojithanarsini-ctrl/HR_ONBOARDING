from pathlib import Path
import streamlit as st

from modules.chatbot import answer_policy_question
from modules.document_processor import extract_text

st.set_page_config(
    page_title="HR Policy Chatbot",
    page_icon="💬",
)

st.title("💬 HR Policy Chatbot")
st.write(
    "Ask questions about company policies, onboarding, "
    "attendance, and HR procedures."
)

st.info(
    "This chatbot provides information only. "
    "It cannot approve leave, authorize payroll, "
    "or approve policy exceptions."
)

PROJECT_DIR = Path(__file__).resolve().parents[1]
POLICY_DIR = PROJECT_DIR / "data" / "policy_documents"


@st.cache_data
def load_policy_text():
    documents = []
    POLICY_DIR.mkdir(parents=True, exist_ok=True)

    for file_path in POLICY_DIR.iterdir():
        if file_path.suffix.lower() in (".pdf", ".docx"):
            try:
                text = extract_text(file_path)
                if text.strip():
                    documents.append(
                        f"Document: {file_path.name}\n{text}"
                    )
            except Exception as exc:
                print(f"Could not read {file_path.name}: {exc}")

    return "\n\n".join(documents)


policy_text = load_policy_text()

if not policy_text:
    st.warning(
        "No readable PDF or DOCX policy was found. "
        "Place a policy document inside data/policy_documents."
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages only once
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# One chat input
question = st.chat_input(
    "Ask an HR policy question...",
    key="hr_policy_chat_input",
)

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Checking your HR policy..."):
            answer = answer_policy_question(
                question,
                policy_text,
            )
        st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

if st.button("Clear conversation"):
    st.session_state.messages = []
    st.rerun()
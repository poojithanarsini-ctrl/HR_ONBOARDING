
import streamlit as st

st.set_page_config(
    page_title="HR Onboarding Bot",
    page_icon="🤝",
    layout="wide"
)

st.title("🤝 HR Onboarding & Policy Explainer Bot")

st.write(
    "Welcome! Your AI-powered assistant helps you "
    "understand HR policies and onboarding procedures."
)

st.info(
    "Ask questions about company policies, "
    "onboarding tasks, and HR procedures."
)

st.subheader("What would you like to do?")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📚 Understand HR Policies")
    st.write("Get simple explanations of company policies.")

with col2:
    st.markdown("### ✅ Onboarding Checklist")
    st.write("Keep track of your onboarding activities.")

st.warning(
    "This assistant provides information only. "
    "It cannot approve leave, authorize payroll, "
    "or approve policy exceptions."
)
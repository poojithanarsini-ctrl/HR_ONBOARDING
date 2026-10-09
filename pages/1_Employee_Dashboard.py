
import streamlit as st

st.set_page_config(
    page_title="Employee Dashboard",
    page_icon="👋",
    layout="wide"
)

st.title("👋 Employee Dashboard")

st.write(
    "Welcome to your HR Onboarding & Policy Explainer Bot!"
)

st.info(
    "Use this dashboard to understand company policies "
    "and complete your onboarding activities."
)

# Dashboard summary
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Onboarding Tasks", "6")

with col2:
    st.metric("Policy Assistant", "Available")

with col3:
    st.metric("HR Support", "Available")

st.divider()

# Quick access
st.subheader("🚀 Quick Access")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📋 Onboarding Checklist")
    st.write(
        "Review your onboarding activities "
        "and track your progress."
    )

    if st.button("View Onboarding Tasks"):
        st.switch_page("pages/3_Onboarding_Checklist.py")

with col2:
    st.markdown("### 🤖 HR Policy Chatbot")
    st.write(
        "Ask questions about company policies, "
        "attendance, leave procedures, and HR processes."
    )

    if st.button("Ask the HR Assistant"):
        st.switch_page("pages/2_Policy_Chatbot.py")

st.divider()

st.subheader("📌 Important Reminder")

st.warning(
    "This assistant explains HR policies but cannot approve "
    "leave, authorize payroll, or approve policy exceptions. "
    "Contact HR for official decisions."
)

st.caption(
    "For unresolved questions, please contact your HR team."
)

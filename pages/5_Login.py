
import streamlit as st
from modules.auth import register_user, login_user, ensure_hr_admin

st.set_page_config(
    page_title="HR Onboarding - Login",
    page_icon="🔐",
)

# Set up the configured demo HR admin from Streamlit Secrets.
try:
    admin = st.secrets["hr_admin"]

    success, message = ensure_hr_admin(
        name=admin["name"],
        email=admin["email"],
        password=admin["password"],
    )

    if not success:
        st.warning(f"Demo admin setup: {message}")

except (KeyError, FileNotFoundError):
    st.warning(
        "Demo HR admin is not configured. "
        "Check your Streamlit Secrets settings."
    )

st.title("🔐 HR Onboarding Portal")
st.write("Sign in or create an employee account.")

if "user" not in st.session_state:
    st.session_state["user"] = None

if st.session_state["user"]:
    user = st.session_state["user"]

    st.success(f"Welcome, {user['name']}!")
    st.write(f"**Email:** {user['email']}")
    st.write(f"**Role:** {user['role'].replace('_', ' ').title()}")

    if st.button("Log out"):
        st.session_state["user"] = None
        st.rerun()

else:
    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        st.subheader("Login")

        with st.form("login_form"):
            email = st.text_input("Email address")
            password = st.text_input(
                "Password",
                type="password",
            )
            login_clicked = st.form_submit_button("Login")

        if login_clicked:
            if not email.strip() or not password:
                st.error("Please enter your email and password.")
            else:
                user = login_user(email, password)

                if user:
                    st.session_state["user"] = user
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid email or password.")

    with register_tab:
        st.subheader("Create an employee account")

        with st.form("register_form"):
            name = st.text_input("Full name")
            email = st.text_input("Work email address")
            password = st.text_input(
                "Create password",
                type="password",
            )
            confirm_password = st.text_input(
                "Confirm password",
                type="password",
            )

            register_clicked = st.form_submit_button(
                "Create account",
            )

        if register_clicked:
            if not name.strip() or not email.strip():
                st.error("Please fill in your name and email.")
            elif password != confirm_password:
                st.error("The passwords do not match.")
            else:
                success, message = register_user(
                    name=name,
                    email=email,
                    password=password,
                    role="employee",
                )

                if success:
                    st.success(
                        "Account created! You can now log in."
                    )
                else:
                    st.error(message)

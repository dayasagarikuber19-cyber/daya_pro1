import streamlit as st
import hashlib
from db_config import get_connection

# --- Utility: Hashing Password ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- Page Setup ---
st.set_page_config(page_title="Login/Register", layout="centered")
st.title("🔐 Client Query Management System")

# --- Shared Inputs ---
username = st.text_input("Username")
password = st.text_input("Password", type="password")
role = st.radio("Select Role", ["Client", "Support"])

# --- Register Function ---
def register_user():
    if not username or not password:
        st.error("Please enter both username and password.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        st.error("Username already exists.")
        conn.close()
        return

    hashed_pw = hash_password(password)
    cursor.execute(
        "INSERT INTO users (username, hashed_password, role) VALUES (%s, %s, %s)",
        (username, hashed_pw, role)
    )
    conn.commit()
    conn.close()
    st.success("Registration successful! Please log in.")

# --- Login Function ---
def login_user():
    if not username or not password:
        st.error("Please enter both username and password.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    hashed_pw = hash_password(password)
    cursor.execute(
        "SELECT role FROM users WHERE username = %s AND hashed_password = %s",
        (username, hashed_pw)
    )
    result = cursor.fetchone()
    conn.close()

    if result and result[0] == role:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.role = role
    else:
        st.error("Invalid credentials or role mismatch.")

# --- Buttons ---
col1, col2 = st.columns(2)
with col1:
    st.button("Register", on_click=register_user)
with col2:
    st.button("Login", on_click=login_user)

# --- Redirect After Login (Outside Callback) ---
if st.session_state.get("logged_in"):
    if st.session_state.role == "Client":
        st.switch_page("pages/1_Client.py")
    elif st.session_state.role == "Support":
        st.switch_page("pages/2_Support.py")

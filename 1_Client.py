import streamlit as st
from db_config import get_connection
from datetime import datetime

st.set_page_config(page_title="Client Dashboard")

if "username" not in st.session_state:
    st.warning("Please log in first.")
    st.stop()

st.title("Submit a Query")

mail_id = st.text_input("Email ID")
mobile_number = st.text_input("Mobile Number")
query_heading = st.text_input("Query Heading")
query_description = st.text_area("Query Description")
image_file = st.file_uploader("Upload Screenshot (optional)", type=["jpg", "png"])

if st.button("Submit"):
    image_data = image_file.read() if image_file else None
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO queries (mail_id, mobile_number, query_heading, query_description, image, status, query_created_time)
        VALUES (%s, %s, %s, %s, %s, 'Open', %s)
    """, (mail_id, mobile_number, query_heading, query_description, image_data, datetime.now()))
    conn.commit()
    conn.close()
    st.success("Query submitted successfully!")

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("Go to Support Page"):
        st.switch_page("2_Support")
with col2:
    if st.button("Logout"):
        st.session_state.clear()
        st.switch_page("Login")

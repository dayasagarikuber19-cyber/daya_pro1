import streamlit as st
from db_config import get_connection
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Support Dashboard")

if "username" not in st.session_state:
    st.warning("Please log in first.")
    st.stop()

st.title("Manage Queries")

status_filter = st.selectbox("Filter by Status", ["All", "Open", "Closed"])
conn = get_connection()
cursor = conn.cursor(dictionary=True)

query = "SELECT * FROM queries"
if status_filter != "All":
    query += f" WHERE status = '{status_filter}'"

cursor.execute(query)
rows = cursor.fetchall()
df = pd.DataFrame(rows)
st.dataframe(df)

query_ids = [row["query_id"] for row in rows if row["status"] == "Open"]
selected_id = st.selectbox("Select Query to Close", query_ids)

if st.button("Close Query"):
    cursor.execute("""
        UPDATE queries SET status='Closed', query_closed_time=%s WHERE query_id=%s
    """, (datetime.now(), selected_id))
    conn.commit()
    st.success(f"Query {selected_id} closed.")
conn.close()

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("Go to Client Page"):
       # st.switch_page("1_Client")
       st.switch_page("1_Client")
with col2:
    if st.button("Logout"):
        st.session_state.clear()
        st.switch_page("Login")

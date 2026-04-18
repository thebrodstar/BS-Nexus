import streamlit as st
from supabase import create_client, Client

URL = "https://cumhnomhukgnvqzgwega.supabase.co"
KEY = "sb_publishable_oEIkr3WPifCepDIFCKm7VA_sTeSUBJQ"
try: supabase: Client = create_client(URL, KEY)
except: pass

if "user" not in st.session_state or not st.session_state["user"]:
    st.warning("⚠️ Please log in on the main page first.")
    st.stop()

st.title("📬 Inbox & Notifications")
st.info("Messages, alerts, and certification warnings will show up here.")

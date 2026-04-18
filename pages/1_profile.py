import streamlit as st
from supabase import create_client, Client

# --- DATABASE RE-CONNECTION ---
URL = "https://cumhnomhukgnvqzgwega.supabase.co"
KEY = "sb_publishable_oEIkr3WPifCepDIFCKm7VA_sTeSUBJQ"
try:
    supabase: Client = create_client(URL, KEY)
except:
    pass

# --- SECURITY CHECK ---
# Kicks the user back to the login page if they try to bypass it
if "user" not in st.session_state or st.session_state["user"] is None:
    st.warning("⚠️ Please log in on the main page first.")
    st.stop()

# --- PROFILE DISPLAY ---
st.title("👤 My Profile")

p = st.session_state.get("profile")

if p:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Name:** {p.get('full_name', 'Not set')}")
        st.markdown(f"**Role:** {p.get('role', 'Not set')}")
        st.markdown(f"**Employee ID:** {p.get('employee_id', 'Not set')}")
    with col2:
        st.markdown(f"**Company:** {p.get('company', 'Not set')}")
        st.markdown(f"**Department:** {p.get('department', 'Not set')}")
        st.markdown(f"**Clearance:** {p.get('security_clearance', 'Not set')}")
else:
    st.info("No profile data found yet. We will add the edit form next!")

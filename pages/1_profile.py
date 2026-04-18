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
if "user" not in st.session_state or not st.session_state["user"]:
    st.warning("⚠️ Please log in on the main page first.")
    st.stop()

st.title("👤 My Profile")
st.markdown("Update your personnel and clearance information below.")

# Pull existing data if they have it
p = st.session_state.get("profile") or {}

# Dropdown options
roles = ["Fiber Tech", "Lineman", "Project Manager", "Admin", "Other"]
clearances = ["None", "Secret", "Top Secret"]

# --- THE DATA FORM ---
with st.form("profile_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name", value=p.get("full_name", ""))
        
        # Setup Role dropdown
        curr_role = p.get("role", "Fiber Tech")
        role_idx = roles.index(curr_role) if curr_role in roles else 0
        role = st.selectbox("Role", roles, index=role_idx)
        
        emp_id = st.text_input("Employee ID", value=p.get("employee_id", ""))
        
    with col2:
        company = st.text_input("Company", value=p.get("company", ""))
        dept = st.text_input("Department", value=p.get("department", ""))
        
        # Setup Clearance dropdown
        curr_clr = p.get("security_clearance", "None")
        clr_idx = clearances.index(curr_clr) if curr_clr in clearances else 0
        clearance = st.selectbox("Security Clearance", clearances, index=clr_idx)

    # The Save Button
    submitted = st.form_submit_button("Save Profile")

    # What happens when they click Save
    if submitted:
        user_id = st.session_state["user"].id
        profile_data = {
            "id": user_id,
            "full_name": name,
            "role": role,
            "employee_id": emp_id,
            "company": company,
            "department": dept,
            "security_clearance": clearance
        }
        
        try:
            # Upsert tells Supabase to Update if it exists, or Insert if it is brand new
            supabase.table("profiles").upsert(profile_data).execute()
            st.session_state["profile"] = profile_data
            st.success("✅ Profile saved securely!")
            st.rerun()
        except Exception as e:
            st.error(f"Error saving to database: {e}")

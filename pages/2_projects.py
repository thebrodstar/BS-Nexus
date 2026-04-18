import streamlit as st
from supabase import create_client, Client
import pandas as pd

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

st.title("📁 Projects & Networks")
st.markdown("Manage active fiber builds, splicing jobs, and network deployments.")

# --- CREATE NEW PROJECT FORM ---
with st.expander("➕ Create New Project", expanded=False):
    with st.form("new_project_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            p_name = st.text_input("Project / Job Name")
            client = st.text_input("Client / Contractor")
        with col2:
            net_type = st.selectbox("Network Type", ["FTTH (Fiber to the Home)", "Long Haul", "Cell Tower Backhaul", "Maintenance/Repair"])
            status = st.selectbox("Status", ["Planning", "Permitting", "Active Build", "Splicing/Testing", "Completed"])
        
        notes = st.text_area("Scope of Work / Notes")
        submitted = st.form_submit_button("Add Project")
        
        if submitted:
            if not p_name:
                st.error("⚠️ Project Name is required.")
            else:
                user_id = st.session_state["user"].id
                project_data = {
                    "project_name": p_name,
                    "client": client,
                    "network_type": net_type,
                    "status": status,
                    "notes": notes,
                    "created_by": user_id
                }
                
                try:
                    # Insert the new job into the database
                    supabase.table("projects").insert(project_data).execute()
                    st.success(f"✅ Project '{p_name}' added successfully!")
                    st.rerun() # Refresh the page to show the new project in the table
                except Exception as e:
                    st.error(f"Error saving project: {e}")

# --- VIEW ACTIVE PROJECTS ---
st.markdown("---")
st.subheader("Active Job Board")

try:
    # Fetch projects from Supabase
    response = supabase.table("projects").select("*").execute()
    
    if response.data:
        # Convert the data into a clean table using Pandas
        df = pd.DataFrame(response.data)
        # Rearrange and clean up columns for display
        display_df = df[["project_name", "client", "network_type", "status", "notes"]]
        # Display the table
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("No active projects found. Create one using the menu above!")
except Exception as e:
    st.error("⚠️ Database connection error. (Make sure you create the 'projects' table in Supabase!)")

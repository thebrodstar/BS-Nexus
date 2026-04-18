import streamlit as st
from supabase import create_client, Client

# --- DATABASE CONNECTION ---
URL = "https://cumhnomhukgnvqzgwega.supabase.co"
KEY = "sb_publishable_oEIkr3WPifCepDIFCKm7VA_sTeSUBJQ"
try: supabase: Client = create_client(URL, KEY)
except: pass

if "user" not in st.session_state or not st.session_state["user"]:
    st.warning("⚠️ Please log in on the main page.")
    st.stop()

st.title("📁 Projects & Networks")

# --- CREATE PROJECT (In an Expander) ---
with st.expander("➕ Add New Project"):
    with st.form("new_project"):
        p_name = st.text_input("Project Name")
        client = st.text_input("Client")
        net_type = st.selectbox("Type", ["FTTH", "Long Haul", "Maintenance"])
        status = st.selectbox("Status", ["Planning", "Active", "Splicing", "Done"])
        notes = st.text_area("Notes")
        if st.form_submit_button("Save New Project"):
            if p_name:
                supabase.table("projects").insert({
                    "project_name": p_name, "client": client, 
                    "network_type": net_type, "status": status, 
                    "notes": notes, "created_by": st.session_state["user"].id
                }).execute()
                st.success("Project Added!")
                st.rerun()

st.markdown("---")
st.subheader("Active Job Board")

# --- FETCH & EDIT PROJECTS ---
try:
    res = supabase.table("projects").select("*").execute()
    if res.data:
        for p in res.data:
            with st.container(border=True):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**{p['project_name']}** | {p['client']} ({p['status']})")
                    st.caption(f"{p['network_type']} - {p['notes']}")
                
                # The "Edit" trigger
                with col2:
                    if st.button("Edit", key=f"edit_{p['id']}"):
                        st.session_state[f"editing_{p['id']}"] = True

                # The Edit Form (Only shows if Edit was clicked)
                if st.session_state.get(f"editing_{p['id']}", False):
                    with st.form(f"form_{p['id']}"):
                        new_status = st.selectbox("Update Status", ["Planning", "Active", "Splicing", "Done"], 
                                                  index=["Planning", "Active", "Splicing", "Done"].index(p['status']))
                        new_notes = st.text_area("Update Notes", value=p['notes'])
                        
                        c1, c2 = st.columns(2)
                        if c1.form_submit_button("Save Changes"):
                            supabase.table("projects").update({"status": new_status, "notes": new_notes}).eq("id", p['id']).execute()
                            st.session_state[f"editing_{p['id']}"] = False
                            st.rerun()
                        if c2.form_submit_button("Cancel"):
                            st.session_state[f"editing_{p['id']}"] = False
                            st.rerun()
    else:
        st.info("No projects found.")
except Exception as e:
    st.error(f"Error: {e}")

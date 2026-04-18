import streamlit as st
from supabase import create_client, Client

# --- DATABASE CONNECTION ---
URL = "https://cumhnomhukgnvqzgwega.supabase.co"
KEY = "sb_publishable_oEIkr3WPifCepDIFCKm7VA_sTeSUBJQ"
try:
    supabase: Client = create_client(URL, KEY)
except:
    pass

if "user" not in st.session_state or not st.session_state["user"]:
    st.warning("⚠️ Please log in on the main page.")
    st.stop()

st.title("📁 Project & Asset Manager")

# --- ADD PROJECT SECTION ---
with st.expander("➕ New Project"):
    with st.form("new_p"):
        name = st.text_input("Project Name")
        client = st.text_input("Client")
        if st.form_submit_button("Create Project"):
            if name:
                try:
                    supabase.table("projects").insert({
                        "project_name": name, 
                        "client": client, 
                        "created_by": st.session_state["user"].id
                    }).execute()
                    st.success("Project Created!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

st.markdown("---")
st.subheader("Active Job Board")

# --- PROJECT LIST & ASSETS ---
try:
    res = supabase.table("projects").select("*").execute()
    for p in res.data:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            col1.subheader(f"🏗️ {p['project_name']}")
            col1.caption(f"Client: {p['client']}")
            
            # ASSET MANAGEMENT AREA
            with st.expander(f"View Assets for {p['project_name']}"):
                # Form to add a new asset
                with st.form(f"add_asset_{p['id']}"):
                    st.write("**Add Field Asset (FOSC, MH, Pole, etc.)**")
                    c1, c2, c3 = st.columns(3)
                    a_type = c1.selectbox("Type", ["MDF", "IDF", "Telepole", "JWI", "FOSC", "MH"], key=f"type_{p['id']}")
                    a_label = c2.text_input("Label/ID", placeholder="e.g. FOSC-A1", key=f"label_{p['id']}")
                    a_gps = c3.text_input("GPS (optional)", key=f"gps_{p['id']}")if st.form_submit_button("Add Asset"):
                        try:
                            supabase.table("assets").insert({
                                "project_id": p['id'],
                                "asset_type": a_type,
                                "label": a_label,
                                "gps_coords": a_gps
                            }).execute()
                            st.success(f"{a_type} Added!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error adding asset: {e}")
                
                # List existing assets in a clean table
                st.markdown("---")
                assets_res = supabase.table("assets").select("*").eq("project_id", p['id']).execute()
                if assets_res.data:
                    st.table(assets_res.data)
                else:
                    st.info("No assets logged yet.")

            if col2.button("🗑️ Delete Project", key=f"del_{p['id']}"):
                supabase.table("projects").delete().eq("id", p['id']).execute()
                st.rerun()
except Exception as e:
    st.error("Database sync in progress... try refreshing!")

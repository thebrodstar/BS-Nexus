import streamlit as st
from supabase import create_client, Client
import random
import string

# --- 1. CLOUD VAULT CONNECTION ---
URL = "https://cumhnomhukgnvqzgwega.supabase.co"
KEY = "sb_publishable_oEIkr3WPifCepDIFCKm7VA_sTeSUBJQ"

try:
    supabase: Client = create_client(URL, KEY)
except:
    st.warning("⚠️ Database not connected. Check your internet.")

# --- 2. THE "NEXUS" UI SETUP ---
st.set_page_config(page_title="B&S Nexus", layout="wide")

st.markdown("""
    <style>
    .stApp { 
        background: radial-gradient(circle at 10% 20%, rgb(255, 255, 255) 0%, rgb(228, 233, 237) 100%); 
        color: #202124; 
    }
    [data-testid="stSidebar"] { background-color: rgba(248, 249, 250, 0.85); border-right: 1px solid #DADCE0; backdrop-filter: blur(10px); }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #1A73E8; color: white; font-weight: 600; padding: 10px; border: none; transition: 0.3s; }
    .stButton>button:hover { background-color: #1557B0; transform: translateY(-2px); box-shadow: 0 4px 6px rgba(26,115,232,0.3); }
    h1, h2, h3 { color: #172B4D; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'user' not in st.session_state:
    st.session_state['user'] = None
if 'role' not in st.session_state:
    st.session_state['role'] = None
if 'active_project' not in st.session_state:
    st.session_state['active_project'] = None

def generate_key():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# --- 4. THE GATEWAY (LOGIN/REGISTER) ---
if not st.session_state['user']:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("Website logo.jpg", width=300)
        page = st.radio("Select:", ["Sign In", "Register"], horizontal=True)

        if page == "Sign In":
            lemail = st.text_input("Email")
            lpass = st.text_input("Password", type="password")
            if st.button("Access Portal"):
                try:
                    res = supabase.auth.sign_in_with_password({"email": lemail, "password": lpass})
                    st.session_state['user'] = res.user
                    prof = supabase.table("profiles").select("role").eq("id", res.user.id).execute()
                    if prof.data:
                        st.session_state['role'] = prof.data[0]['role']
                    st.rerun()
                except Exception as e:
                    st.error(f"Login Failed: {e}")

        if page == "Register":
            rrole = st.selectbox("I am a...", ["Manager", "Technician"])
            rname = st.text_input("Full Name")
            remail = st.text_input("Work Email")
            rpass = st.text_input("Create Password", type="password")
            if st.button("Register Account"):
                try:
                    res = supabase.auth.sign_up({"email": remail, "password": rpass})
                    supabase.table("profiles").insert({"id": res.user.id, "email": remail, "full_name": rname, "role": rrole}).execute()
                    st.success("Account created! Now select 'Sign In'.")
                except Exception as e:
                    st.error(f"Registration failed: {e}")
    st.stop()

# --- 5. LOGOUT BUTTON ---
if st.sidebar.button("Log Out"):
    st.session_state.clear()
    st.rerun()

# --- 6. MANAGER DASHBOARD ---
if st.session_state['role'] == "Manager":
    st.title("👔 Manager Control Center")
    with st.container(border=True):
        p_name = st.text_input("Project Name (e.g. Halifax Fiber Expansion)")
        if st.button("Generate Tech Access Key"):
            new_key = generate_key()
            supabase.table("projects").insert({
                "manager_id": st.session_state['user'].id,
                "project_name": p_name,
                "invite_key": new_key
            }).execute()
            st.success(f"Project Live! Share this key with your technician: **{new_key}**")

    st.subheader("Current Network Audit Log")
    try:
        data = supabase.table("network_assets").select("*").execute()
        if data.data:
            st.table(data.data)
        else:
            st.info("No assets logged yet.")
    except Exception as e:
        st.error(f"Could not load data: {e}")

# --- 7. TECHNICIAN DASHBOARD ---
else:
    st.title("🔧 Technician Field Portal")

    check = supabase.table("roster").select("project_id").eq("user_id", st.session_state['user'].id).execute()

    if not check.data:
        st.info("Please enter the key provided by your manager to begin.")
        join_key = st.text_input("6-Digit Project Key")
        if st.button("Join Project"):
            try:
                proj = supabase.table("projects").select("id").eq("invite_key", join_key).execute()
                if proj.data:
                    supabase.table("roster").insert({
                        "user_id": st.session_state['user'].id,
                        "project_id": proj.data[0]['id']
                    }).execute()
                    st.success("Project Linked!")
                    st.rerun()
                else:
                    st.error("Invalid Key. Check with your manager.")
            except Exception as e:
                st.error(f"Error joining project: {e}")
    else:
        with st.sidebar:
            st.header("📋 Fiber Entry")
            cat = st.selectbox("Type", ["MDF", "Pole", "FDH/JWI", "Node", "MST", "Vault"])
            aid = st.text_input("Asset ID")
            count = st.selectbox("Fiber Count", [12, 24, 48, 144, 288, 432, 864, 1728, 3456])
            if st.button("Commit to Vault"):
                try:
                    supabase.table("network_assets").insert({
                        "asset_id": aid,
                        "category": cat,
                        "count": count,
                        "user_id": st.session_state['user'].id
                    }).execute()
                    st.success(f"Locked: {aid}")
                except Exception as e:
                    st.error(f"Failed to save: {e}")

        st.write("### Active Field Project")
        st.write("You are connected to the B&S Nexus. All entries are timestamped and logged.")

        st.subheader("Your Logged Assets")
        try:
            assets = supabase.table("network_assets").select("*").eq("user_id", st.session_state['user'].id).execute()
            if assets.data:
                st.table(assets.data)
            else:
                st.info("No assets logged yet. Use the sidebar to add entries.")
        except Exception as e:
            st.error(f"Could not load assets: {e}")
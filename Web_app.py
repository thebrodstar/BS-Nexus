import streamlit as st
from supabase import create_client, Client

# --- DATABASE CONNECTION ---
URL = "https://cumhnomhukgnvqzgwega.supabase.co"
KEY = "sb_publishable_oEIkr3WPifCepDIFCKm7VA_sTeSUBJQ"

try:
    supabase: Client = create_client(URL, KEY)
except:
    st.warning("Database connection failed.")

st.set_page_config(page_title="B&D Nexus", layout="wide")

# --- PERSISTENT SESSION MANAGEMENT ---
if "user" not in st.session_state:
    st.session_state["user"] = None

# Attempt to recover session if it exists in the client
if st.session_state["user"] is None:
    try:
        session = supabase.auth.get_session()
        if session:
            st.session_state["user"] = session.user
    except:
        pass

for key, val in [("profile", None), ("auth_page", "Sign In")]:
    if key not in st.session_state:
        st.session_state[key] = val

# --- LOGIN & REGISTRATION PAGE ---
if not st.session_state["user"]:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        # --- SMART LOGO LOADER ---
        logo_found = False
        for ext in ["jpg", "png", "jpeg", "JPG", "PNG"]:
            try:
                if st.image(f"Website logo.{ext}", use_container_width=True):
                    logo_found = True
                    break
            except:
                continue
        
        if not logo_found:
            st.markdown("## 🛰️ B&D Nexus")

        if st.session_state["auth_page"] == "Sign In":
            st.markdown("### Sign In")
            lemail = st.text_input("Email Address")
            lpass = st.text_input("Password", type="password")
            
            if st.button("Sign In", use_container_width=True):
                try:
                    res = supabase.auth.sign_in_with_password(
                        {"email": lemail, "password": lpass}
                    )
                    st.session_state["user"] = res.user
                    # Get profile data
                    prof = supabase.table("profiles").select("*").eq(
                        "id", res.user.id
                    ).execute()
                    if prof.data:
                        st.session_state["profile"] = prof.data[0]
                    st.rerun()
                except Exception as e:
                    st.error(f"Login Failed: {e}")
            
            st.markdown("---")
            c1, c2 = st.columns(2)
            if c1.button("Create Account"):
                st.session_state["auth_page"] = "Create Account"
                st.rerun()
            if c2.button("Forgot Password?"):
                st.session_state["auth_page"] = "Forgot Password"
                st.rerun()
import streamlit as st
from supabase import create_client, Client

# --- DATABASE CONNECTION ---
URL = "https://cumhnomhukgnvqzgwega.supabase.co"
KEY = "sb_publishable_oEIkr3WPifCepDIFCKm7VA_sTeSUBJQ"

try:
    supabase: Client = create_client(URL, KEY)
except:
    st.warning("Database connection failed.")

st.set_page_config(page_title="B&D Nexus", layout="wide")

# --- PERSISTENT SESSION MANAGEMENT ---
if "user" not in st.session_state:
    st.session_state["user"] = None

# Attempt to recover session if it exists in the client
if st.session_state["user"] is None:
    try:
        session = supabase.auth.get_session()
        if session:
            st.session_state["user"] = session.user
    except:
        pass

for key, val in [("profile", None), ("auth_page", "Sign In")]:
    if key not in st.session_state:
        st.session_state[key] = val

# --- LOGIN & REGISTRATION PAGE ---
if not st.session_state["user"]:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        # --- SMART LOGO LOADER ---
        logo_found = False
        for ext in ["jpg", "png", "jpeg", "JPG", "PNG"]:
            try:
                if st.image(f"Website logo.{ext}", use_container_width=True):
                    logo_found = True
                    break
            except:
                continue
        
        if not logo_found:
            st.markdown("## 🛰️ B&D Nexus")

        if st.session_state["auth_page"] == "Sign In":
            st.markdown("### Sign In")
            lemail = st.text_input("Email Address")
            lpass = st.text_input("Password", type="password")
            
            if st.button("Sign In", use_container_width=True):
                try:
                    res = supabase.auth.sign_in_with_password(
                        {"email": lemail, "password": lpass}
                    )
                    st.session_state["user"] = res.user
                    # Get profile data
                    prof = supabase.table("profiles").select("*").eq(
                        "id", res.user.id
                    ).execute()
                    if prof.data:
                        st.session_state["profile"] = prof.data[0]
                    st.rerun()
                except Exception as e:
                    st.error(f"Login Failed: {e}")
            
            st.markdown("---")
            c1, c2 = st.columns(2)
            if c1.button("Create Account"):
                st.session_state["auth_page"] = "Create Account"
                st.rerun()
            if c2.button("Forgot Password?"):
                st.session_state["auth_page"] = "Forgot Password"
                st.rerun()# --- LOGGED IN VIEW ---
st.title("🛰️ B&D Nexus Dashboard")
st.success(f"Logged in as: {st.session_state['user'].email}")
st.info("Use the sidebar to manage Projects, Assets, and Safety Logs.")

# Sidebar Logout Button
if st.sidebar.button("Log Out"):
    supabase.auth.sign_out()
    st.session_state["user"] = None
    st.rerun()

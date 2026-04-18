import streamlit as st
from supabase import create_client, Client

# --- DATABASE CONNECTION ---
URL = "https://cumhnomhukgnvqzgwega.supabase.co"
KEY = "sb_publishable_oEIkr3WPifCepDIFCKm7VA_sTeSUBJQ"
try:
    supabase: Client = create_client(URL, KEY)
except:
    st.warning("Database not connected.")

st.set_page_config(page_title="B&A Nexus", layout="wide")

# --- SESSION STATE ---
for key, val in [("user", None), ("profile", None), ("auth_page", "Sign In")]:
    if key not in st.session_state:
        st.session_state[key] = val

# --- LOGIN & REGISTRATION PAGE ---
if not st.session_state["user"]:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        try:
            st.image("Website logo.jpg", use_column_width=True)
        except:
            pass
            
        if st.session_state["auth_page"] == "Sign In":
            st.markdown("## Sign In to B&A Nexus")
            lemail = st.text_input("Email Address")
            lpass = st.text_input("Password", type="password")
            
            if st.button("Sign In"):
                try:
                    res = supabase.auth.sign_in_with_password({"email": lemail, "password": lpass})
                    st.session_state["user"] = res.user
                    prof = supabase.table("profiles").select("*").eq("id", res.user.id).execute()
                    if prof.data:
                        st.session_state["profile"] = prof.data[0]
                    st.rerun()
                except Exception as e:
                    st.error(f"Login Failed: {e}")
            
            st.markdown("---")
            if st.button("Create an Account"):
                st.session_state["auth_page"] = "Create Account"
                st.rerun()

        elif st.session_state["auth_page"] == "Create Account":
            st.markdown("## Create Your Account")
            remail = st.text_input("Work Email Address")
            rpass = st.text_input("Create Password", type="password")
            
            if st.button("Register"):
                try:
                    res = supabase.auth.sign_up({"email": remail, "password": rpass})
                    st.success("Account created! Please sign in.")
                    st.session_state["auth_page"] = "Sign In"
                    st.rerun()
                except Exception as e:
                    st.error(f"Registration failed: {e}")
            
            st.markdown("---")
            if st.button("Back to Sign In"):
                st.session_state["auth_page"] = "Sign In"
                st.rerun()
    st.stop() # Stops unauthenticated users here

# --- LOGGED IN VIEW ---
st.title("Welcome to B&A Nexus!")
st.success("Authentication successful. Ready to build the next pages!")

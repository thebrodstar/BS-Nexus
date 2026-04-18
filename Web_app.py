import streamlit as st
from supabase import create_client, Client

# --- DATABASE CONNECTION ---
URL = "https://cumhnomhukgnvqzgwega.supabase.co"
KEY = "sb_publishable_oEIkr3WPifCepDIFCKm7VA_sTeSUBJQ"
try:
    supabase: Client = create_client(URL, KEY)
except:
    st.warning("Database not connected.")

st.set_page_config(page_title="B&D Nexus", layout="wide")

# --- SESSION STATE ---
for key, val in [("user", None), ("profile", None), ("auth_page", "Sign In")]:
    if key not in st.session_state:
        st.session_state[key] = val

# --- LOGIN & REGISTRATION PAGE ---
if not st.session_state["user"]:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        # --- SMART LOGO LOADER ---
        Logo_found = False
        for ext in ["jpg", "png", "jpeg", "JPG", "PNG"]:
            try:
                if st.image(f"Website logo.{ext}", use_container_width=True):
                    Logo_found = True
                    break
            except:
                continue
        
        if not Logo_found:
            st.markdown("### 🛰️ B&D Nexus")
            
        if st.session_state["auth_page"] == "Sign In":
            st.markdown("## Sign In to B&D Nexus")
            lemail = st.text_input("Email Address")
            lpass = st.text_input("Password", type="password")
            
            if st.button("Sign In"):
                try:
                    res = supabase.auth.sign_in_with_password({"email": lemail, "password": lpass})
                    st.session_state["user"] = res.user
                    prof = supabase.table("profiles").select("*").eq("id", res.user.id).execute()
                    if prof.data: st.session_state["profile"] = prof.data[0]
                    st.rerun()
                except Exception as e:
                    st.error(f"Login Failed: {e}")
            
            st.markdown("---")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Create an Account"):
                    st.session_state["auth_page"] = "Create Account"
                    st.rerun()
            with c2:
                if st.button("Forgot Password?"):
                    st.session_state["auth_page"] = "Forgot Password"
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

        elif st.session_state["auth_page"] == "Forgot Password":
            st.markdown("## Reset Password")
            femail = st.text_input("Enter your email address to receive a reset link.")
            
            if st.button("Send Reset Link"):
                try:
                    supabase.auth.reset_password_for_email(femail)
                    st.success("Reset link sent! Check your inbox.")
                except Exception as e:
                    st.error(f"Error: {e}")
            
            st.markdown("---")
            if st.button("Back to Sign In"):
                st.session_state["auth_page"] = "Sign In"
                st.rerun()

    st.stop()

# --- LOGGED IN VIEW ---
st.title("Welcome to B&D Nexus!")
st.success("Authentication successful. Select a page from the sidebar.")

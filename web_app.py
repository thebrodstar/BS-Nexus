import streamlit as st
from supabase import create_client, Client

# --- 1. CLOUD VAULT CONNECTION ---
URL = "https://cumhnomhukgnvqzgwega.supabase.co" 
KEY = "sb_publishable_oElkr3WPifCepDIF6c80-45e0-a9e7-1169fa5c329f"

try:
    supabase: Client = create_client(URL, KEY)
except:
    st.warning("⚠️ Database not connected. Check your internet.")

# --- 2. THE "NEXUS" UI SETUP ---
st.set_page_config(page_title="B&S Nexus", layout="wide")

st.markdown("""
    <style>
    /* Google/Future Gradient Background */
    .stApp { 
        background: radial-gradient(circle at 10% 20%, rgb(255, 255, 255) 0%, rgb(228, 233, 237) 100%); 
        color: #202124; 
        font-family: 'Segoe UI', Roboto, Helvetica, sans-serif; 
    }
    [data-testid="stSidebar"] { background-color: rgba(248, 249, 250, 0.85); border-right: 1px solid #DADCE0; backdrop-filter: blur(10px); }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #1A73E8; color: white; font-weight: 600; border: none; padding: 10px; transition: all 0.3s ease; }
    .stButton>button:hover { background-color: #1557B0; transform: translateY(-2px); box-shadow: 0 4px 6px rgba(26,115,232,0.3); }
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea { background-color: #FFFFFF; color: #202124; border: 1px solid #DADCE0; border-radius: 6px; box-shadow: inset 0 1px 2px rgba(0,0,0,0.05); }
    h1, h2, h3 { color: #172B4D; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. THE "CEO" LOCK ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.title("🛡️ B&S Nexus Security Gateway")
    pin = st.text_input("Enter 4-Digit Clearance PIN", type="password")
    if pin == "1234": 
        st.session_state['authenticated'] = True
        st.rerun()
    st.stop()

# --- 4. ASSET REGISTRATION ---
st.title("🌐 B&S Nexus | Infrastructure Portal")

with st.sidebar:
    st.header("📋 Field Entry")
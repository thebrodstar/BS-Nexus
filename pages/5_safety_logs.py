import streamlit as st
from supabase import create_client, Client
from datetime import date

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

st.title("🦺 Daily Safety & Hazard Log")
st.markdown("Log your daily tailgate meetings and site hazards before starting work.")

# --- THE SAFETY FORM ---
with st.form("safety_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        log_date = st.date_input("Date", value=date.today())
        location = st.text_input("Job Site / Location")
        weather = st.selectbox("Weather Conditions", ["Clear/Sunny", "Overcast", "Rain", "Snow/Ice", "High Wind"])
        
    with col2:
        crew = st.text_input("Crew Members Present (Comma separated)")
        ppe_checked = st.checkbox("All required PPE inspected and worn?")
        first_aid = st.checkbox("First Aid kit on site and accessible?")
        
    # Standard field hazards
    hazards = st.multiselect("Hazards Identified", 
        ["Traffic/Roadway", "Overhead Power Lines", "Confined Space", "Trenching/Excavation", "Wildlife/Insects", "Extreme Temps", "Slips/Trips/Falls"]
    )
    
    notes = st.text_area("Additional Safety Notes or Mitigation Steps")
    
    submitted = st.form_submit_button("Submit Log")
    
    if submitted:
        if not location or not crew:
            st.error("⚠️ Please fill in the Site Location and Crew Members.")
        else:
            user_id = st.session_state["user"].id
            log_data = {
                "user_id": user_id,
                "date": str(log_date),
                "location": location,
                "weather": weather,
                "crew": crew,
                "ppe_checked": ppe_checked,
                "first_aid_on_site": first_aid,
                "hazards": ", ".join(hazards),
                "notes": notes
            }
            
            try:
                # Insert the new log into the database
                supabase.table("safety_logs").insert(log_data).execute()
                st.success(f"✅ Safety log for {location} successfully submitted!")
            except Exception as e:
                st.error(f"Error saving log: {e}")

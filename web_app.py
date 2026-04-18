import streamlit as st
from supabase import create_client, Client
from datetime import datetime, timedelta

URL = "https://cumhnomhukgnvqzgwega.supabase.co"
KEY = "sb_publishable_oEIkr3WPifCepDIFCKm7VA_sTeSUBJQ"

try:
    supabase: Client = create_client(URL, KEY)
except:
    st.warning("Database not connected.")

st.set_page_config(page_title="B&A Nexus", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f0f2f5; color: #202124; }
    [data-testid="stSidebar"] { background-color: #172B4D; }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebar"] .stButton>button {
        width: 100%; background: none !important; border: none !important;
        color: white !important; font-size: 15px !important; font-weight: 500 !important;
        text-align: left !important; padding: 10px 16px !important;
        border-radius: 8px !important; margin-bottom: 4px !important;
    }
    [data-testid="stSidebar"] .stButton>button:hover { background-color: rgba(255,255,255,0.1) !important; }
    .main-btn button { width: 100% !important; border-radius: 25px !important; background-color: #1A73E8 !important; color: white !important; font-weight: 700 !important; font-size: 16px !important; padding: 12px !important; border: none !important; }
    .main-btn button:hover { background-color: #1557B0 !important; }
    .link-btn button { background: none !important; border: none !important; color: #1A73E8 !important; text-decoration: underline !important; font-size: 14px !important; padding: 0 !important; box-shadow: none !important; width: auto !important; }
    h1, h2, h3 { color: #172B4D; }
    div[data-testid="stTextInput"] input { background-color: white !important; border: 1.5px solid #DADCE0 !important; border-radius: 8px !important; padding: 12px !important; font-size: 16px !important; }
    div[data-testid="stTextInput"] label { font-weight: 600 !important; font-size: 15px !important; color: #172B4D !important; }
    </style>
    """, unsafe_allow_html=True)

for key, val in [("user", None), ("profile", None), ("active_project", None), ("project_role", None), ("auth_page", "Sign In"), ("nav", "My Projects"), ("viewing_tech_id", None)]:
    if key not in st.session_state:
        st.session_state[key] = val

def check_cert_expiry():
    p = st.session_state["profile"]
    if not p:
        return
    certs = [
        ("first_aid", "first_aid_expiry", "First Aid / CPR"),
        ("whmis", "whmis_expiry", "WHMIS"),
        ("osha", "osha_expiry", "OSHA / OHS"),
        ("fall_protection", "fall_protection_expiry", "Fall Protection"),
        ("confined_space", "confined_space_expiry", "Confined Space"),
        ("fiber_cert", "fiber_cert_expiry", "Fiber Optic Cert"),
    ]
    today = datetime.today()
    for cert_key, expiry_key, label in certs:
        if p.get(cert_key) and p.get(expiry_key):
            try:
                expiry = datetime.strptime(str(p[expiry_key]), "%Y-%m-%d")
                days_left = (expiry - today).days
                if days_left < 0:
                    msg = "EXPIRED: Your " + label + " certification expired on " + str(p[expiry_key])
                    existing = supabase.table("notifications").select("id").eq("user_id", st.session_state["user"].id).eq("message", msg).execute()
                    if not existing.data:
                        supabase.table("notifications").insert({"user_id": st.session_state["user"].id, "message": msg}).execute()
                        managers = supabase.table("project_members").select("user_id").eq("project_id", st.session_state["active_project"]["id"] if st.session_state["active_project"] else "").eq("role", "Manager").execute()
                        for mgr in managers.data:
                            supabase.table("notifications").insert({"user_id": mgr["user_id"], "message": p.get("full_name", "A tech") + " certification EXPIRED: " + label + " on " + str(p[expiry_key])}).execute()
                elif days_left <= 30:
                    msg = "EXPIRING SOON: Your " + label + " expires in " + str(days_left) + " days (" + str(p[expiry_key]) + ")"
                    existing = supabase.table("notifications").select("id").eq("user_id", st.session_state["user"].id).eq("message", msg).execute()
                    if not existing.data:
                        supabase.table("notifications").insert({"user_id": st.session_state["user"].id, "message": msg}).execute()
            except:
                pass

def cert_status_badge(has_cert, expiry_str):
    if not has_cert:
        return "🟠 Missing"
    if not expiry_str:
        return "✅ Yes"
    try:
        expiry = datetime.strptime(str(expiry_str), "%Y-%m-%d")
        days_left = (expiry - datetime.today()).days
        if days_left < 0:
            return "🔴 Expired"
        elif days_left <= 30:
            return "🟠 Expiring Soon"
        else:
            return "✅ Valid"
    except:
        return "✅ Yes"

def get_positions():
    try:
        pos = supabase.table("positions").select("title").execute()
        return [p["title"] for p in pos.data]
    except:
        return ["Manager", "Technician", "Supervisor", "Administrator"]

def profile_form(button_label, existing=None):
    e = existing or {}
    positions = get_positions()
    current_role = e.get("role", "Technician")
    role_index = positions.index(current_role) if current_role in positions else 0
    st.markdown("#### Position and Identity")
    rrole = st.selectbox("Position / Role", positions, index=role_index)
    new_position = st.text_input("Add Custom Position (optional)")
    if st.button("Add Position") and new_position:
        try:
            supabase.table("positions").insert({"title": new_position, "created_by": st.session_state["user"].id}).execute()
            st.success("Position added!")
            st.rerun()
        except:
            st.error("Could not add position.")
    employee_id = st.text_input("Employee ID", value=e.get("employee_id", ""))
    st.markdown("---")
    st.markdown("#### Personal Information")
    first_name = st.text_input("First Name", value=e.get("first_name", ""))
    last_name = st.text_input("Last Name", value=e.get("last_name", ""))
    phone = st.text_input("Phone Number", value=e.get("phone", ""))
    st.markdown("---")
    st.markdown("#### Emergency Contact")
    emergency_contact_name = st.text_input("Emergency Contact Full Name", value=e.get("emergency_contact_name", ""))
    emergency_contact_phone = st.text_input("Emergency Contact Phone Number", value=e.get("emergency_contact_phone", ""))
    emergency_contact_relation = st.text_input("Relationship", value=e.get("emergency_contact_relation", ""))
    st.markdown("---")
    st.markdown("#### Work Information")
    company = st.text_input("Company / Contractor Name", value=e.get("company", ""))
    department = st.text_input("Department", value=e.get("department", ""))
    work_location = st.text_input("Primary Work Location / City", value=e.get("work_location", ""))
    st.markdown("---")
    st.markdown("#### Security Clearance")
    clearance_options = ["None", "Reliability", "Secret", "Top Secret"]
    security_clearance = st.selectbox("Security Clearance Level", clearance_options, index=clearance_options.index(e.get("security_clearance", "None")) if e.get("security_clearance") in clearance_options else 0)
    clearance_expiry = st.text_input("Clearance Expiry Date (YYYY-MM-DD)", value=e.get("clearance_expiry", ""))
    st.markdown("---")
    st.markdown("#### Drivers License")
    license_options = ["None", "Class 5", "Class 3", "Class 1", "Other"]
    drivers_license = st.selectbox("License Class", license_options, index=license_options.index(e.get("drivers_license", "None")) if e.get("drivers_license") in license_options else 0)
    license_expiry = st.text_input("License Expiry Date (YYYY-MM-DD)", value=e.get("license_expiry", ""))
    air_brakes = st.checkbox("Air Brakes Endorsement", value=bool(e.get("air_brakes", False)))
    st.markdown("---")
    st.markdown("#### Safety Certifications")
    certs = {}
    cert_list = [("first_aid", "First Aid / CPR"), ("whmis", "WHMIS"), ("osha", "OSHA / OHS"), ("fall_protection", "Fall Protection"), ("confined_space", "Confined Space Entry")]
    for cert_key, cert_label in cert_list:
        has = st.radio(cert_label, ["Yes", "No"], index=0 if e.get(cert_key) else 1, horizontal=True, key="cert_" + cert_key)
        expiry = ""
        if has == "Yes":
            expiry = st.text_input(cert_label + " Expiry (YYYY-MM-DD)", value=e.get(cert_key + "_expiry", ""), key="expiry_" + cert_key)
            uploaded = st.file_uploader("Upload " + cert_label + " Certificate", type=["jpg", "jpeg", "png", "pdf"], key="upload_" + cert_key)
            if uploaded:
                st.success("Certificate uploaded for review!")
        certs[cert_key] = has == "Yes"
        certs[cert_key + "_expiry"] = expiry
    st.markdown("---")
    st.markdown("#### Technical Certifications")
    fiber_has = st.radio("Fiber Optic Certification", ["Yes", "No"], index=0 if e.get("fiber_cert") else 1, horizontal=True)
    fiber_cert = fiber_has == "Yes"
    fiber_cert_expiry = ""
    if fiber_cert:
        fiber_cert_expiry = st.text_input("Fiber Cert Expiry (YYYY-MM-DD)", value=e.get("fiber_cert_expiry", ""))
    other_certifications = st.text_input("Other Technical Certifications", value=e.get("other_certifications", ""))
    other_safety_courses = st.text_input("Other Safety Courses Completed", value=e.get("other_safety_courses", ""))

    if st.button(button_label):
        if not first_name or not last_name or not employee_id:
            st.error("Please fill in all required fields.")
            return None
        data = {
            "full_name": first_name + " " + last_name,
            "first_name": first_name,
            "last_name": last_name,
            "role": rrole,
            "employee_id": employee_id,
            "phone": phone,
            "emergency_contact_name": emergency_contact_name,
            "emergency_contact_phone": emergency_contact_phone,
            "emergency_contact_relation": emergency_contact_relation,
            "company": company,
            "department": department,
            "work_location": work_location,
            "security_clearance": security_clearance,
            "clearance_expiry": clearance_expiry,
            "drivers_license": drivers_license,
            "license_expiry": license_expiry,
            "air_brakes": air_brakes,
            "fiber_cert": fiber_cert,
            "fiber_cert_expiry": fiber_cert_expiry,
            "other_certifications": other_certifications,
            "other_safety_courses": other_safety_courses,
        }
        data.update(certs)
        return data
    return None

if not st.session_state["user"]:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.image("Website logo.jpg", use_column_width=True)
        if st.session_state["auth_page"] == "Sign In":
            st.markdown("## Sign In to B&A Nexus")
            lemail = st.text_input("Email Address")
            lpass = st.text_input("Password", type="password")
            st.markdown("<div class='main-btn'>", unsafe_allow_html=True)
            if st.button("Sign In", key="signin_btn"):
                try:
                    res = supabase.auth.sign_in_with_password({"email": lemail, "password": lpass})
                    st.session_state["user"] = res.user
                    prof = supabase.table("profiles").select("*").eq("id", res.user.id).execute()
                    if prof.data:
                        st.session_state["profile"] = prof.data[0]
                    st.rerun()
                except Exception as e:
                    st.error("Login Failed: " + str(e))
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            link1, link2 = st.columns(2)
            with link1:
                st.markdown("<div class='link-btn'>", unsafe_allow_html=True)
                if st.button("Forgot Password?", key="goto_forgot"):
                    st.session_state["auth_page"] = "Forgot Password"
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            with link2:
                st.markdown("<div class='link-btn'>", unsafe_allow_html=True)
                if st.button("Create an Account", key="goto_register"):
                    st.session_state["auth_page"] = "Create Account"
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

        elif st.session_state["auth_page"] == "Forgot Password":
            st.markdown("## Reset Your Password")
            reset_email = st.text_input("Work Email Address")
            st.markdown("<div class='main-btn'>", unsafe_allow_html=True)
            if st.button("Send Reset Link"):
                try:
                    supabase.auth.reset_password_email(reset_email)
                    st.success("Password reset email sent!")
                except Exception as e:
                    st.error("Error: " + str(e))
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<div class='link-btn'>", unsafe_allow_html=True)
            if st.button("Back to Sign In"):
                st.session_state["auth_page"] = "Sign In"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        elif st.session_state["auth_page"] == "Create Account":
            st.markdown("## Create Your Account")
            st.markdown("#### Account Security")
            remail = st.text_input("Work Email Address")
            rpass = st.text_input("Create Password", type="password")
            rpass2 = st.text_input("Confirm Password", type="password")
            agree = st.checkbox("I confirm all information is accurate and agree to the B&A Nexus terms of use.")
            data = profile_form("Register Account")
            if data:
                if not agree:
                    st.error("You must agree to the terms.")
                elif rpass != rpass2:
                    st.error("Passwords do not match.")
                elif not remail or not rpass:
                    st.error("Please fill in email and password.")
                else:
                    try:
                        res = supabase.auth.sign_up({"email": remail, "password": rpass})
                        data["id"] = res.user.id
                        data["email"] = remail
                        supabase.table("profiles").insert(data).execute()
                        st.success("Account created! Please sign in.")
                        st.session_state["auth_page"] = "Sign In"
                        st.rerun()
                    except Exception as e:
                        st.error("Registration failed: " + str(e))
            st.markdown("<div class='link-btn'>", unsafe_allow_html=True)
            if st.button("Back to Sign In"):
                st.session_state["auth_page"] = "Sign In"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

if not st.session_state["profile"]:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.image("Website logo.jpg", use_column_width=True)
        st.warning("Welcome! Please complete your profile to continue.")
        st.markdown("## Complete Your Profile")
        data = profile_form("Save Profile")
        if data:
            try:
                data["id"] = st.session_state["user"].id
                data["email"] = st.session_state["user"].email
                existing = supabase.table("profiles").select("id").eq("id", st.session_state["user"].id).execute()
                if existing.data:
                    supabase.table("profiles").update(data).eq("id", st.session_state["user"].id).execute()
                else:
                    supabase.table("profiles").insert(data).execute()
                prof = supabase.table("profiles").select("*").eq("id", st.session_state["user"].id).execute()
                if prof.data:
                    st.session_state["profile"] = prof.data[0]
                st.success("Profile saved!")
                st.rerun()
            except Exception as e:
                st.error("Failed to save profile: " + str(e))
    st.stop()

check_cert_expiry()

with st.sidebar:
    st.image("Website logo.jpg", use_column_width=True)
    p = st.session_state["profile"]
    if p:
        st.markdown("**" + p.get("full_name", "") + "**")
        st.markdown(p.get("role", ""))
        st.markdown(p.get("company", ""))
    st.markdown("---")
    notif_count = 0
    try:
        notifs = supabase.table("notifications").select("*").eq("user_id", st.session_state["user"].id).eq("is_read", False).execute()
        notif_count = len(notifs.data)
    except:
        pass
    if st.button("👤  My Profile"):
        st.session_state["nav"] = "My Profile"
        st.rerun()
    if st.button("🔔  Notifications" + (" (" + str(notif_count) + ")" if notif_count > 0 else "")):
        st.session_state["nav"] = "Notifications"
        st.rerun()
    if st.button("📬  Inbox"):
        st.session_state["nav"] = "Inbox"
        st.rerun()
    if st.button("📁  My Projects"):
        st.session_state["nav"] = "My Projects"
        st.rerun()
    if st.button("🌐  All Projects"):
        st.session_state["nav"] = "All Projects"
        st.rerun()
    if st.button("➕  Create a Network"):
        st.session_state["nav"] = "Create Network"
        st.rerun()
    if p and p.get("role") in ["Manager", "Supervisor", "Administrator", "CEO"]:
        if st.button("👥  Personnel"):
            st.session_state["nav"] = "Personnel"
            st.rerun()
    st.markdown("---")
    if st.button("🚪  Log Out"):
        st.session_state.clear()
        st.rerun()

nav = st.session_state["nav"]

if nav == "My Profile":
    st.title("My Profile")
    p = st.session_state["profile"]
    if p:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Name:** " + str(p.get("full_name", "")))
            st.markdown("**Role:** " + str(p.get("role", "")))
            st.markdown("**Employee ID:** " + str(p.get("employee_id", "")))
            st.markdown("**Email:** " + str(p.get("email", "")))
            st.markdown("**Phone:** " + str(p.get("phone", "")))
            st.markdown("**Company:** " + str(p.get("company", "")))
            st.markdown("**Department:** " + str(p.get("department", "")))
            st.markdown("**Location:** " + str(p.get("work_location", "")))
            st.markdown("**Security Clearance:** " + str(p.get("security_clearance", "")))
            st.markdown("**Drivers License:** " + str(p.get("drivers_license", "")) + " | Air Brakes: " + str(p.get("air_brakes", "")))
        with col2:
            st.markdown("**Certification Status:**")
            cert_list = [("first_aid", "first_aid_expiry", "First Aid / CPR"), ("whmis", "whmis_expiry", "WHMIS"), ("osha", "osha_expiry", "OSHA / OHS"), ("fall_protection", "fall_protection_expiry", "Fall Protection"), ("confined_space", "confined_space_expiry", "Confined Space"), ("fiber_cert", "fiber_cert_expiry", "Fiber Optic Cert")]
            for cert_key, expiry_key, label in cert_list:
                badge = cert_status_badge(p.get(cert_key), p.get(expiry_key))
                st.markdown("**" + label + ":** " + badge)
            st.markdown("**Emergency Contact:** " + str(p.get("emergency_contact_name", "")) + " - " + str(p.get("emergency_contact_phone", "")))
        st.markdown("---")
        st.markdown("### Edit My Profile")
        updated = profile_form("Save Changes", existing=p)
        if updated:
            try:
                supabase.table("profiles").update(updated).eq("id", st.session_state["user"].id).execute()
                prof = supabase.table("profil
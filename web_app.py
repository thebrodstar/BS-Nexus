import streamlit as st
from supabase import create_client, Client

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
        width: 100%;
        background: none !important;
        border: none !important;
        color: white !important;
        font-size: 15px !important;
        font-weight: 500 !important;
        text-align: left !important;
        padding: 10px 16px !important;
        border-radius: 8px !important;
        margin-bottom: 4px !important;
    }
    [data-testid="stSidebar"] .stButton>button:hover {
        background-color: rgba(255,255,255,0.1) !important;
    }
    .main-btn button {
        width: 100% !important;
        border-radius: 25px !important;
        background-color: #1A73E8 !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        padding: 12px !important;
        border: none !important;
    }
    .main-btn button:hover { background-color: #1557B0 !important; }
    .link-btn button {
        background: none !important;
        border: none !important;
        color: #1A73E8 !important;
        text-decoration: underline !important;
        font-size: 14px !important;
        padding: 0 !important;
        box-shadow: none !important;
        width: auto !important;
    }
    h1, h2, h3 { color: #172B4D; }
    div[data-testid="stTextInput"] input { background-color: white !important; border: 1.5px solid #DADCE0 !important; border-radius: 8px !important; padding: 12px !important; font-size: 16px !important; }
    div[data-testid="stTextInput"] label { font-weight: 600 !important; font-size: 15px !important; color: #172B4D !important; }
    </style>
    """, unsafe_allow_html=True)

if "user" not in st.session_state:
    st.session_state["user"] = None
if "profile" not in st.session_state:
    st.session_state["profile"] = None
if "active_project" not in st.session_state:
    st.session_state["active_project"] = None
if "project_role" not in st.session_state:
    st.session_state["project_role"] = None
if "auth_page" not in st.session_state:
    st.session_state["auth_page"] = "Sign In"
if "nav" not in st.session_state:
    st.session_state["nav"] = "My Projects"

def profile_form(button_label, existing=None):
    e = existing or {}
    st.markdown("#### Position and Identity")
    rrole = st.selectbox("Position / Role", ["Manager", "Technician", "Supervisor", "Administrator"], index=["Manager", "Technician", "Supervisor", "Administrator"].index(e.get("role", "Technician")) if e.get("role") in ["Manager", "Technician", "Supervisor", "Administrator"] else 1)
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
    first_aid = st.checkbox("First Aid / CPR", value=bool(e.get("first_aid", False)))
    first_aid_expiry = st.text_input("First Aid Expiry (YYYY-MM-DD)", value=e.get("first_aid_expiry", "")) if first_aid else ""
    whmis = st.checkbox("WHMIS", value=bool(e.get("whmis", False)))
    whmis_expiry = st.text_input("WHMIS Expiry (YYYY-MM-DD)", value=e.get("whmis_expiry", "")) if whmis else ""
    osha = st.checkbox("OSHA / OHS", value=bool(e.get("osha", False)))
    osha_expiry = st.text_input("OSHA Expiry (YYYY-MM-DD)", value=e.get("osha_expiry", "")) if osha else ""
    fall_protection = st.checkbox("Fall Protection", value=bool(e.get("fall_protection", False)))
    fall_protection_expiry = st.text_input("Fall Protection Expiry (YYYY-MM-DD)", value=e.get("fall_protection_expiry", "")) if fall_protection else ""
    confined_space = st.checkbox("Confined Space Entry", value=bool(e.get("confined_space", False)))
    confined_space_expiry = st.text_input("Confined Space Expiry (YYYY-MM-DD)", value=e.get("confined_space_expiry", "")) if confined_space else ""
    st.markdown("---")
    st.markdown("#### Technical Certifications")
    fiber_cert = st.checkbox("Fiber Optic Certification", value=bool(e.get("fiber_cert", False)))
    fiber_cert_expiry = st.text_input("Fiber Cert Expiry (YYYY-MM-DD)", value=e.get("fiber_cert_expiry", "")) if fiber_cert else ""
    other_certifications = st.text_input("Other Technical Certifications", value=e.get("other_certifications", ""))
    other_safety_courses = st.text_input("Other Safety Courses Completed", value=e.get("other_safety_courses", ""))

    if st.button(button_label):
        if not first_name or not last_name or not employee_id:
            st.error("Please fill in all required fields.")
            return None
        return {
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
            "first_aid": first_aid,
            "first_aid_expiry": first_aid_expiry,
            "whmis": whmis,
            "whmis_expiry": whmis_expiry,
            "osha": osha,
            "osha_expiry": osha_expiry,
            "fall_protection": fall_protection,
            "fall_protection_expiry": fall_protection_expiry,
            "confined_space": confined_space,
            "confined_space_expiry": confined_space_expiry,
            "fiber_cert": fiber_cert,
            "fiber_cert_expiry": fiber_cert_expiry,
            "other_certifications": other_certifications,
            "other_safety_courses": other_safety_courses,
        }
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
            st.write("Enter your work email and we will send you a reset link.")
            reset_email = st.text_input("Work Email Address")
            st.markdown("<div class='main-btn'>", unsafe_allow_html=True)
            if st.button("Send Reset Link"):
                try:
                    supabase.auth.reset_password_email(reset_email)
                    st.success("Password reset email sent! Check your inbox.")
                except Exception as e:
                    st.error("Error: " + str(e))
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<div class='link-btn'>", unsafe_allow_html=True)
            if st.button("Back to Sign In"):
                st.session_state["auth_page"] = "Sign In"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        elif st.session_state["auth_page"] == "Create Account":
            st.markdown("## Create Your Profile")
            st.markdown("#### Account Security")
            remail = st.text_input("Work Email Address")
            rpass = st.text_input("Create Password", type="password")
            rpass2 = st.text_input("Confirm Password", type="password")
            agree = st.checkbox("I confirm all information is accurate and agree to the B&A Nexus terms of use.")
            data = profile_form("Register Account")
            if data:
                if not agree:
                    st.error("You must agree to the terms before registering.")
                elif rpass != rpass2:
                    st.error("Passwords do not match.")
                elif not remail or not rpass:
                    st.error("Please fill in all required fields.")
                else:
                    try:
                        res = supabase.auth.sign_up({"email": remail, "password": rpass})
                        data["id"] = res.user.id
                        data["email"] = remail
                        supabase.table("profiles").insert(data).execute()
                        st.success("Account created! Click below to sign in.")
                        st.session_state["auth_page"] = "Sign In"
                        st.rerun()
                    except Exception as e:
                        st.error("Registration failed: " + str(e))
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<div class='link-btn'>", unsafe_allow_html=True)
            if st.button("Back to Sign In"):
                st.session_state["auth_page"] = "Sign In"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- CHECK IF PROFILE EXISTS - if not, prompt to complete ---
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

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("Website logo.jpg", use_column_width=True)
    if st.session_state["profile"]:
        st.markdown("**" + st.session_state["profile"].get("full_name", "") + "**")
        st.markdown(st.session_state["profile"].get("role", ""))
        st.markdown(st.session_state["profile"].get("company", ""))
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
        with col2:
            st.markdown("**Security Clearance:** " + str(p.get("security_clearance", "")))
            st.markdown("**Drivers License:** " + str(p.get("drivers_license", "")))
            st.markdown("**Air Brakes:** " + str(p.get("air_brakes", "")))
            st.markdown("---")
            st.markdown("**Safety Certifications:**")
            if p.get("first_aid"): st.markdown("- First Aid / CPR (Expiry: " + str(p.get("first_aid_expiry", "")) + ")")
            if p.get("whmis"): st.markdown("- WHMIS (Expiry: " + str(p.get("whmis_expiry", "")) + ")")
            if p.get("osha"): st.markdown("- OSHA / OHS (Expiry: " + str(p.get("osha_expiry", "")) + ")")
            if p.get("fall_protection"): st.markdown("- Fall Protection (Expiry: " + str(p.get("fall_protection_expiry", "")) + ")")
            if p.get("confined_space"): st.markdown("- Confined Space (Expiry: " + str(p.get("confined_space_expiry", "")) + ")")
            if p.get("fiber_cert"): st.markdown("- Fiber Optic Cert (Expiry: " + str(p.get("fiber_cert_expiry", "")) + ")")
            st.markdown("**Other Certs:** " + str(p.get("other_certifications", "")))
            st.markdown("**Emergency Contact:** " + str(p.get("emergency_contact_name", "")) + " - " + str(p.get("emergency_contact_phone", "")))
        st.markdown("---")
        st.markdown("### Edit My Profile")
        updated = profile_form("Save Changes", existing=p)
        if updated:
            try:
                supabase.table("profiles").update(updated).eq("id", st.session_state["user"].id).execute()
                prof = supabase.table("profiles").select("*").eq("id", st.session_state["user"].id).execute()
                if prof.data:
                    st.session_state["profile"] = prof.data[0]
                supabase.table("notifications").insert({"user_id": st.session_state["user"].id, "message": "Your profile was updated successfully."}).execute()
                st.success("Profile updated!")
                st.rerun()
            except Exception as e:
                st.error("Failed to update: " + str(e))

elif nav == "Notifications":
    st.title("Notifications")
    try:
        notifs = supabase.table("notifications").select("*").eq("user_id", st.session_state["user"].id).order("created_at", desc=True).execute()
        if not notifs.data:
            st.info("No notifications yet.")
        else:
            for n in notifs.data:
                if not n["is_read"]:
                    st.warning(n["message"] + "  -  " + str(n["created_at"])[:10])
                    supabase.table("notifications").update({"is_read": True}).eq("id", n["id"]).execute()
                else:
                    st.info(n["message"] + "  -  " + str(n["created_at"])[:10])
    except Exception as e:
        st.error("Could not load notifications: " + str(e))

elif nav == "Inbox":
    st.title("Inbox")
    st.write("Messages from your projects:")
    try:
        my_projects = supabase.table("project_members").select("project_id").eq("user_id", st.session_state["user"].id).execute()
        my_project_ids = [m["project_id"] for m in my_projects.data]
        if not my_project_ids:
            st.info("Join a project to see messages.")
        else:
            for pid in my_project_ids:
                proj_info = supabase.table("projects").select("project_name").eq("id", pid).execute()
                proj_name = proj_info.data[0]["project_name"] if proj_info.data else "Unknown Project"
                assets = supabase.table("network_assets").select("*").eq("project_id", pid).execute()
                for asset in assets.data:
                    comments = supabase.table("asset_comments").select("*").eq("asset_id", asset["id"]).execute()
                    if comments.data:
                        with st.expander(proj_name + " - " + str(asset["asset_id"])):
                            for c in comments.data:
                                st.markdown(str(c["message"]) + "  -  " + str(c["created_at"])[:10])
                            reply = st.text_input("Reply", key="inbox_reply_" + str(asset["id"]))
                            if st.button("Send", key="inbox_send_" + str(asset["id"])):
                                if reply:
                                    supabase.table("asset_comments").insert({
                                        "asset_id": asset["id"],
                                        "user_id": st.session_state["user"].id,
                                        "message": reply
                                    }).execute()
                                    st.rerun()
    except Exception as e:
        st.error("Could not load inbox: " + str(e))

elif nav == "My Projects":
    st.title("My Projects")
    try:
        all_projects = supabase.table("projects").select("*").execute()
        my_memberships = supabase.table("project_members").select("*").eq("user_id", st.session_state["user"].id).execute()
        my_project_ids = [m["project_id"] for m in my_memberships.data]
        if not my_memberships.data:
            st.info("You have not joined any projects yet. Go to All Projects to join one.")
        else:
            for proj in all_projects.data:
                if proj["id"] in my_project_ids:
                    member = next((m for m in my_memberships.data if m["project_id"] == proj["id"]), None)
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown("### " + proj["project_name"])
                        st.markdown("Role: **" + member["role"] + "**")
                    with col2:
                        if st.button("Open", key="open_" + proj["id"]):
                            st.session_state["active_project"] = proj
                            st.session_state["project_role"] = member["role"]
                            st.session_state["nav"] = "Project Dashboard"
                            st.rerun()
                    st.markdown("---")
    except Exception as e:
        st.error("Could not load projects: " + str(e))

elif nav == "All Projects":
    st.title("All Projects")
    try:
        all_projects = supabase.table("projects").select("*").execute()
        my_memberships = supabase.table("project_members").select("*").eq("user_id", st.session_state["user"].id).execute()
        my_project_ids = [m["project_id"] for m in my_memberships.data]
        if not all_projects.data:
            st.info("No projects exist yet. Create one using Create a Network.")
        else:
            for proj in all_projects.data:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown("**" + proj["project_name"] + "**")
                with col2:
                    join_role = st.selectbox("Role", ["Technician", "Manager"], key="role_" + proj["id"])
                with col3:
                    if proj["id"] not in my_project_ids:
                        if st.button("Join", key="join_" + proj["id"]):
                            supabase.table("project_members").insert({
                                "user_id": st.session_state["user"].id,
                                "project_id": proj["id"],
                                "role": join_role
                            }).execute()
                            st.success("Joined!")
                            st.rerun()
                    else:
                        st.markdown("Joined")
                st.markdown("---")
    except Exception as e:
        st.error("Could not load projects: " + str(e))

elif nav == "Create Network":
    st.title("Create a Network")
    st.write("Create a new project network for your team.")
    new_proj_name = st.text_input("Network / Project Name")
    new_proj_desc = st.text_area("Description (optional)")
    if st.button("Create Network"):
        if new_proj_name:
            try:
                new_proj = supabase.table("projects").insert({
                    "project_name": new_proj_name,
                    "created_by": st.session_state["user"].id
                }).execute()
                supabase.table("project_members").insert({
                    "user_id": st.session_state["user"].id,
                    "project_id": new_proj.data[0]["id"],
                    "role": "Manager"
                }).execute()
                st.success("Network created! You have been added as Manager.")
                st.session_state["nav"] = "My Projects"
                st.rerun()
            except Exception as e:
                st.error("Failed to create network: " + str(e))
        else:
            st.error("Please enter a network name.")

elif nav == "Project Dashboard":
    if not st.session_state["active_project"]:
        st.session_state["nav"] = "My Projects"
        st.rerun()
    proj = st.session_state["active_project"]
    role = st.session_state["project_role"]
    st.title(proj["project_name"])
    st.markdown("**Your Role:** " + role)
    if st.button("Back to My Projects"):
        st.session_state["nav"] = "My Projects"
        st.session_state["active_project"] = None
        st.session_state["project_role"] = None
        st.rerun()
    st.markdown("---")
    if role == "Manager":
        st.subheader("Pending Approvals")
        pending = supabase.table("network_assets").select("*").eq("project_id", proj["id"]).eq("status", "Pending").execute()
        if not pending.data:
            st.info("No pending items.")
        else:
            for asset in pending.data:
                label = str(asset["asset_id"]) + " - " + str(asset["category"]) + " - " + str(asset["count"]) + " fibers"
                with st.expander(label):
                    st.write("Submitted by: " + str(asset["user_id"]))
                    st.write("Date: " + str(asset["created_at"]))
                    comments = supabase.table("asset_comments").select("*").eq("asset_id", asset["id"]).execute()
                    if comments.data:
                        st.markdown("**Messages:**")
                        for c in comments.data:
                            st.markdown(str(c["message"]) + " - " + str(c["created_at"])[:10])
                    msg = st.text_input("Message to tech", key="msg_" + str(asset["id"]))
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("Approve", key="app_" + str(asset["id"])):
                            supabase.table("network_assets").update({"status": "Approved"}).eq("id", asset["id"]).execute()
                            supabase.table("notifications").insert({"user_id": asset["user_id"], "message": "Your entry " + str(asset["asset_id"]) + " was approved!"}).execute()
                            st.rerun()
                    with col2:
                        if st.button("Reject", key="rej_" + str(asset["id"])):
                            supabase.table("network_assets").update({"status": "Rejected"}).eq("id", asset["id"]).execute()
                            supabase.table("notifications").insert({"user_id": asset["user_id"], "message": "Your entry " + str(asset["asset_id"]) + " was rejected."}).execute()
                            st.rerun()
                    with col3:
                        if st.button("Send Message", key="send_" + str(asset["id"])):
                            if msg:
                                supabase.table("asset_comments").insert({"asset_id": asset["id"], "user_id": st.session_state["user"].id, "message": msg}).execute()
                                supabase.table("notifications").insert({"user_id": asset["user_id"], "message": "Manager commented on " + str(asset["asset_id"]) + ": " + msg}).execute()
                                st.rerun()
        st.markdown("---")
        st.subheader("Approved Assets")
        approved = supabase.table("network_assets").select("*").eq("project_id", proj["id"]).eq("status", "Approved").execute()
        if approved.data:
            st.table(approved.data)
        else:
            st.info("No approved assets yet.")

    if role == "Technician":
        st.subheader("Submit Fiber Entry")
        col1, col2, col3 = st.columns(3)
        with col1:
            cat = st.selectbox("Asset Type", ["MDF", "Pole", "FDH/JWI", "Node", "MST", "Vault"])
        with col2:
            aid = st.text_input("Asset ID")
        with col3:
            count = st.selectbox("Fiber Count", [12, 24, 48, 144, 288, 432, 864, 1728, 3456])
        if st.button("Submit for Approval"):
            try:
                supabase.table("network_assets").insert({
                    "user_id": st.session_state["user"].id,
                    "project_id": proj["id"],
                    "asset_id": aid,
                    "category": cat,
                    "count": count,
                    "status": "Pending"
                }).execute()
                managers = supabase.table("project_members").select("user_id").eq("project_id", proj["id"]).eq("role", "Manager").execute()
                for mgr in managers.data:
                    supabase.table("notifications").insert({"user_id": mgr["user_id"], "message": "New entry " + str(aid) + " submitted for approval."}).execute()
                st.success("Submitted: " + str(aid))
            except Exception as e:
                st.error("Failed: " + str(e))
        st.markdown("---")
        st.subheader("My Submitted Assets")
        my_assets = supabase.table("network_assets").select("*").eq("user_id", st.session_state["user"].id).eq("project_id", proj["id"]).execute()
        if my_assets.data:
            for asset in my_assets.data:
                if asset["status"] == "Pending":
                    status_label = "Pending"
                elif asset["status"] == "Approved":
                    status_label = "Approved"
                else:
                    status_label = "Rejected"
                label = str(asset["asset_id"]) + " - " + str(asset["category"]) + " - " + str(asset["count"]) + " fibers - " + status_label
                with st.expander(label):
                    comments = supabase.table("asset_comments").select("*").eq("asset_id", asset["id"]).execute()
                    if comments.data:
                        st.markdown("**Messages:**")
                        for c in comments.data:
                            st.markdown(str(c["message"]) + " - " + str(c["created_at"])[:10])
                    reply = st.text_input("Reply to manager", key="reply_" + str(asset["id"]))
                    if st.button("Send Reply", key="sendreply_" + str(asset["id"])):
                        if reply:
                            supabase.table("asset_comments").insert({"asset_id": asset["id"], "user_id": st.session_state["user"].id, "message": reply}).execute()
                            managers = supabase.table("project_members").select("user_id").eq("project_id", proj["id"]).eq("role", "Manager").execute()
                            for mgr in managers.data:
                                supabase.table("notifications").insert({"user_id": mgr["user_id"], "message": "Tech replied on " + str(asset["asset_id"]) + ": " + reply}).execute()
                            st.rerun()
        else:
            st.info("No assets submitted yet.")

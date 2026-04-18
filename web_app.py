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
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #DADCE0; }
    .stButton>button { width: 100%; border-radius: 25px; background-color: #1A73E8; color: white; font-weight: 700; font-size: 16px; padding: 12px; border: none; margin-top: 4px; }
    .stButton>button:hover { background-color: #1557B0; }
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

if not st.session_state["user"]:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.image("Website logo.jpg", use_column_width=True)

        if st.session_state["auth_page"] == "Sign In":
            st.markdown("## Sign In to B&A Nexus")
            lemail = st.text_input("Email Address")
            lpass = st.text_input("Password", type="password")
            btn1, btn2 = st.columns(2)
            with btn1:
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
            with btn2:
                if st.button("Create an Account", key="goto_register"):
                    st.session_state["auth_page"] = "Create Account"
                    st.rerun()
            st.markdown("---")
            if st.button("Forgot Password", key="goto_forgot"):
                st.session_state["auth_page"] = "Forgot Password"
                st.rerun()

        elif st.session_state["auth_page"] == "Forgot Password":
            st.markdown("## Reset Your Password")
            st.write("Enter your work email and we will send you a reset link.")
            reset_email = st.text_input("Work Email Address")
            if st.button("Send Reset Link"):
                try:
                    supabase.auth.reset_password_email(reset_email)
                    st.success("Password reset email sent! Check your inbox.")
                except Exception as e:
                    st.error("Error: " + str(e))
            if st.button("Back to Sign In"):
                st.session_state["auth_page"] = "Sign In"
                st.rerun()

        elif st.session_state["auth_page"] == "Create Account":
            st.markdown("## Create Your Profile")
            st.markdown("#### Position and Identity")
            rrole = st.selectbox("Position / Role", ["Manager", "Technician", "Supervisor", "Administrator"])
            employee_id = st.text_input("Employee ID")
            st.markdown("---")
            st.markdown("#### Personal Information")
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            phone = st.text_input("Phone Number")
            st.markdown("---")
            st.markdown("#### Emergency Contact")
            emergency_contact_name = st.text_input("Emergency Contact Full Name")
            emergency_contact_phone = st.text_input("Emergency Contact Phone Number")
            emergency_contact_relation = st.text_input("Relationship")
            st.markdown("---")
            st.markdown("#### Work Information")
            company = st.text_input("Company / Contractor Name")
            department = st.text_input("Department")
            work_location = st.text_input("Primary Work Location / City")
            st.markdown("---")
            st.markdown("#### Security Clearance")
            security_clearance = st.selectbox("Security Clearance Level", ["None", "Reliability", "Secret", "Top Secret"])
            clearance_expiry = st.text_input("Clearance Expiry Date (YYYY-MM-DD)")
            st.markdown("---")
            st.markdown("#### Drivers License")
            drivers_license = st.selectbox("License Class", ["None", "Class 5", "Class 3", "Class 1", "Other"])
            license_expiry = st.text_input("License Expiry Date (YYYY-MM-DD)")
            air_brakes = st.checkbox("Air Brakes Endorsement")
            st.markdown("---")
            st.markdown("#### Safety Certifications")
            first_aid = st.checkbox("First Aid / CPR")
            first_aid_expiry = st.text_input("First Aid Expiry (YYYY-MM-DD)") if first_aid else ""
            whmis = st.checkbox("WHMIS")
            whmis_expiry = st.text_input("WHMIS Expiry (YYYY-MM-DD)") if whmis else ""
            osha = st.checkbox("OSHA / OHS")
            osha_expiry = st.text_input("OSHA Expiry (YYYY-MM-DD)") if osha else ""
            fall_protection = st.checkbox("Fall Protection")
            fall_protection_expiry = st.text_input("Fall Protection Expiry (YYYY-MM-DD)") if fall_protection else ""
            confined_space = st.checkbox("Confined Space Entry")
            confined_space_expiry = st.text_input("Confined Space Expiry (YYYY-MM-DD)") if confined_space else ""
            st.markdown("---")
            st.markdown("#### Technical Certifications")
            fiber_cert = st.checkbox("Fiber Optic Certification")
            fiber_cert_expiry = st.text_input("Fiber Cert Expiry (YYYY-MM-DD)") if fiber_cert else ""
            other_certifications = st.text_input("Other Technical Certifications")
            other_safety_courses = st.text_input("Other Safety Courses Completed")
            st.markdown("---")
            st.markdown("#### Account Security")
            remail = st.text_input("Work Email Address")
            rpass = st.text_input("Create Password", type="password")
            rpass2 = st.text_input("Confirm Password", type="password")
            agree = st.checkbox("I confirm all information is accurate and agree to the B&A Nexus terms of use.")
            if st.button("Register Account"):
                if not agree:
                    st.error("You must agree to the terms before registering.")
                elif rpass != rpass2:
                    st.error("Passwords do not match.")
                elif not first_name or not last_name or not remail or not rpass or not employee_id:
                    st.error("Please fill in all required fields.")
                else:
                    try:
                        res = supabase.auth.sign_up({"email": remail, "password": rpass})
                        supabase.table("profiles").insert({
                            "id": res.user.id,
                            "email": remail,
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
                        }).execute()
                        st.success("Account created! Click below to sign in.")
                        st.session_state["auth_page"] = "Sign In"
                        st.rerun()
                    except Exception as e:
                        st.error("Registration failed: " + str(e))
            if st.button("Back to Sign In"):
                st.session_state["auth_page"] = "Sign In"
                st.rerun()
    st.stop()

with st.sidebar:
    if st.session_state["profile"]:
        st.markdown("**" + st.session_state["profile"]["full_name"] + "**")
        st.markdown(st.session_state["profile"].get("company", ""))
        st.markdown(st.session_state["profile"].get("work_location", ""))
        st.divider()
    notifs = supabase.table("notifications").select("*").eq("user_id", st.session_state["user"].id).eq("is_read", False).execute()
    if notifs.data:
        st.warning("You have " + str(len(notifs.data)) + " unread notifications!")
        for n in notifs.data:
            st.info(n["message"])
            supabase.table("notifications").update({"is_read": True}).eq("id", n["id"]).execute()
    st.divider()
    if st.button("Log Out"):
        st.session_state.clear()
        st.rerun()

st.title("B&A Nexus")

all_projects = supabase.table("projects").select("*").execute()
my_memberships = supabase.table("project_members").select("*").eq("user_id", st.session_state["user"].id).execute()
my_project_ids = [m["project_id"] for m in my_memberships.data]

project_page = st.selectbox("Project Menu", ["My Projects", "All Projects and Join", "Create New Project"])

if project_page == "My Projects":
    if not my_memberships.data:
        st.info("You have not joined any projects yet.")
    else:
        for proj in all_projects.data:
            if proj["id"] in my_project_ids:
                member = next((m for m in my_memberships.data if m["project_id"] == proj["id"]), None)
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown("**" + proj["project_name"] + "** - " + member["role"])
                with col2:
                    if st.button("Open", key="open_" + proj["id"]):
                        st.session_state["active_project"] = proj
                        st.session_state["project_role"] = member["role"]
                        st.rerun()

if project_page == "All Projects and Join":
    if not all_projects.data:
        st.info("No projects exist yet.")
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

if project_page == "Create New Project":
    st.markdown("### Create New Project")
    new_proj_name = st.text_input("Project Name")
    if st.button("Create Project"):
        if new_proj_name:
            new_proj = supabase.table("projects").insert({
                "project_name": new_proj_name,
                "created_by": st.session_state["user"].id
            }).execute()
            supabase.table("project_members").insert({
                "user_id": st.session_state["user"].id,
                "project_id": new_proj.data[0]["id"],
                "role": "Manager"
            }).execute()
            st.success("Project created!")
            st.rerun()

if st.session_state["active_project"]:
    proj = st.session_state["active_project"]
    role = st.session_state["project_role"]
    st.divider()
    st.markdown("## " + proj["project_name"] + " - " + role)

    if st.button("Close Project"):
        st.session_state["active_project"] = None
        st.session_state["project_role"] = None
        st.rerun()

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
                    msg = st.text_input("Send message to tech", key="msg_" + str(asset["id"]))
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

        st.subheader("Approved Assets")
        approved = supabase.table("network_assets").select("*").eq("project_id", proj["id"]).eq("status", "Approved").execute()
        if approved.data:
            st.table(approved.data)
        else:
            st.info("No approved assets yet.")

    if role == "Technician":
        with st.sidebar:
            st.header("Fiber Entry")
            cat = st.selectbox("Asset Type", ["MDF", "Pole", "FDH/JWI", "Node", "MST", "Vault"])
            aid = st.text_input("Asset ID")
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

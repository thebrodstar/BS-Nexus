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

# --- 2. UI SETUP ---
st.set_page_config(page_title="B&S Nexus", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at 10% 20%, rgb(255,255,255) 0%, rgb(228,233,237) 100%); color: #202124; }
    [data-testid="stSidebar"] { background-color: rgba(248,249,250,0.85); border-right: 1px solid #DADCE0; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #1A73E8; color: white; font-weight: 600; padding: 10px; border: none; transition: 0.3s; }
    .stButton>button:hover { background-color: #1557B0; transform: translateY(-2px); }
    h1, h2, h3 { color: #172B4D; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'user' not in st.session_state:
    st.session_state['user'] = None
if 'profile' not in st.session_state:
    st.session_state['profile'] = None
if 'active_project' not in st.session_state:
    st.session_state['active_project'] = None
if 'project_role' not in st.session_state:
    st.session_state['project_role'] = None

# --- 4. LOGIN / REGISTER ---
if not st.session_state['user']:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("Website logo.jpg", width=300)
        page = st.selectbox("", ["Sign In", "Register", "Forgot Password"])

        if page == "Sign In":
            lemail = st.text_input("Email")
            lpass = st.text_input("Password", type="password")
            if st.button("Access Portal"):
                try:
                    res = supabase.auth.sign_in_with_password({"email": lemail, "password": lpass})
                    st.session_state['user'] = res.user
                    prof = supabase.table("profiles").select("*").eq("id", res.user.id).execute()
                    if prof.data:
                        st.session_state['profile'] = prof.data[0]
                    st.rerun()
                except Exception as e:
                    st.error(f"Login Failed: {e}")

        if page == "Register":
            st.markdown("### Create Your Profile")
            st.markdown("**Position & Identity**")
            rrole = st.selectbox("Position", ["Manager", "Technician", "Supervisor", "Administrator"])
            employee_id = st.text_input("Employee ID")
            st.markdown("**Personal Information**")
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            phone = st.text_input("Phone Number")
            emergency_contact = st.text_input("Emergency Contact Name & Number")
            st.markdown("**Work Information**")
            company = st.text_input("Company / Contractor Name")
            department = st.text_input("Department")
            work_location = st.text_input("Primary Work Location / City")
            certifications = st.text_input("Certifications (e.g. OSHA, Fiber, etc.)")
            st.markdown("**Account Security**")
            remail = st.text_input("Work Email")
            rpass = st.text_input("Create Password", type="password")
            rpass2 = st.text_input("Confirm Password", type="password")
            agree = st.checkbox("I confirm all information is accurate and agree to the B&S Nexus terms of use.")
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
                            "full_name": f"{first_name} {last_name}",
                            "first_name": first_name,
                            "last_name": last_name,
                            "role": rrole,
                            "employee_id": employee_id,
                            "phone": phone,
                            "emergency_contact": emergency_contact,
                            "company": company,
                            "department": department,
                            "work_location": work_location,
                            "certifications": certifications,
                        }).execute()
                        st.success("Account created! Please select 'Sign In'.")
                    except Exception as e:
                        st.error(f"Registration failed: {e}")

        if page == "Forgot Password":
            st.markdown("### Reset Your Password")
            reset_email = st.text_input("Enter your work email")
            if st.button("Send Reset Link"):
                try:
                    supabase.auth.reset_password_email(reset_email)
                    st.success("Password reset email sent! Check your inbox.")
                except Exception as e:
                    st.error(f"Error: {e}")
    st.stop()

# --- 5. SIDEBAR ---
with st.sidebar:
    if st.session_state['profile']:
        st.markdown(f"👤 **{st.session_state['profile']['full_name']}**")
        st.markdown(f"🏢 {st.session_state['profile']['company']}")
        st.markdown(f"📍 {st.session_state['profile']['work_location']}")
        st.divider()

    # Notifications
    notifs = supabase.table("notifications").select("*").eq("user_id", st.session_state['user'].id).eq("is_read", False).execute()
    if notifs.data:
        st.warning(f"🔔 You have {len(notifs.data)} unread notifications!")
        for n in notifs.data:
            st.info(n['message'])
            supabase.table("notifications").update({"is_read": True}).eq("id", n['id']).execute()
    st.divider()

    if st.button("Log Out"):
        st.session_state.clear()
        st.rerun()

# --- 6. PROJECT SELECTION ---
st.title("🌐 B&S Nexus")

all_projects = supabase.table("projects").select("*").execute()
my_memberships = supabase.table("project_members").select("*").eq("user_id", st.session_state['user'].id).execute()
my_project_ids = [m['project_id'] for m in my_memberships.data]

tab1, tab2 = st.tabs(["My Projects", "All Projects"])

with tab1:
    if not my_memberships.data:
        st.info("You haven't joined any projects yet. Go to 'All Projects' to join one.")
    else:
        for proj in all_projects.data:
            if proj['id'] in my_project_ids:
                member = next((m for m in my_memberships.data if m['project_id'] == proj['id']), None)
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{proj['project_name']}** — *{member['role']}*")
                with col2:
                    if st.button("Open", key=f"open_{proj['id']}"):
                        st.session_state['active_project'] = proj
                        st.session_state['project_role'] = member['role']
                        st.rerun()

with tab2:
    if not all_projects.data:
        st.info("No projects exist yet.")
    else:
        for proj in all_projects.data:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"**{proj['project_name']}**")
            with col2:
                join_role = st.selectbox("Role", ["Technician", "Manager"], key=f"role_{proj['id']}")
            with col3:
                if proj['id'] not in my_project_ids:
                    if st.button("Join", key=f"join_{proj['id']}"):
                        supabase.table("project_members").insert({
                            "user_id": st.session_state['user'].id,
                            "project_id": proj['id'],
                            "role": join_role
                        }).execute()
                        st.success("Joined!")
                        st.rerun()
                else:
                    st.markdown("✅ Joined")

    st.divider()
    st.markdown("### Create New Project")
    new_proj_name = st.text_input("Project Name")
    if st.button("Create Project"):
        if new_proj_name:
            new_proj = supabase.table("projects").insert({
                "project_name": new_proj_name,
                "created_by": st.session_state['user'].id
            }).execute()
            supabase.table("project_members").insert({
                "user_id": st.session_state['user'].id,
                "project_id": new_proj.data[0]['id'],
                "role": "Manager"
            }).execute()
            st.success(f"Project '{new_proj_name}' created!")
            st.rerun()

# --- 7. ACTIVE PROJECT DASHBOARD ---
if st.session_state['active_project']:
    proj = st.session_state['active_project']
    role = st.session_state['project_role']
    st.divider()
    st.markdown(f"## 📁 {proj['project_name']} — {role}")

    if st.button("Close Project"):
        st.session_state['active_project'] = None
        st.session_state['project_role'] = None
        st.rerun()

    # --- MANAGER VIEW ---
    if role == "Manager":
        st.subheader("📋 Pending Approvals")
        pending = supabase.table("network_assets").select("*").eq("project_id", proj['id']).eq("status", "Pending").execute()
        if not pending.data:
            st.info("No pending items.")
        else:
            for asset in pending.data:
                with st.expander(f"🔶 {asset['asset_id']} — {asset['category']} — {asset['count']} fibers"):
                    st.write(f"Submitted by user: {asset['user_id']}")
                    st.write(f"Date: {asset['created_at']}")

                    comments = supabase.table("asset_comments").select("*").eq("asset_id", asset['id']).execute()
                    if comments.data:
                        st.markdown("**Messages:**")
                        for c in comments.data:
                            st.markdown(f"> {c['message']} — *{c['created_at'][:10]}*")

                    msg = st.text_input("Send message to tech", key=f"msg_{asset['id']}")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("✅ Approve", key=f"app_{asset['id']}"):
                            supabase.table("network_assets").update({"status": "Approved"}).eq("id", asset['id']).execute()
                            supabase.table("notifications").insert({"user_id": asset['user_id'], "message": f"✅ Your entry {asset['asset_id']} was approved!"}).execute()
                            st.rerun()
                    with col2:
                        if st.button("❌ Reject", key=f"rej_{asset['id']}"):
                            supabase.table("network_assets").update({"status": "Rejected"}).eq("id", asset['id']).execute()
                            supabase.table("notifications").insert({"user_id": asset['user_id'], "message": f"❌ Your entry {asset['asset_id']} was rejected."}).execute()
                            st.rerun()
                    with col3:
                        if st.button("💬 Send Message", key=f"send_{asset['id']}"):
                            if msg:
                                supabase.table("asset_comments").insert({"asset_id": asset['id'], "user_id": st.session_state['user'].id, "message": msg}).execute()
                                supabase.table("notifications").insert({"user_id": asset['user_id'], "message": f"💬 Manager commented on {asset['asset_id']}: {msg}"}).execute()
                                st.rerun()

        st.subheader("✅ Approved Assets")
        approved = supabase.table("network_assets").select("*").eq("project_id", proj['id']).eq("status", "Approved").execute()
        if approved.data:
            st.table(approved.data)
        else:
            st.info("No approved assets yet.")

    # --- TECHNICIAN VIEW ---
    if role == "Technician":
        with st.sidebar:
            st.header("📋 Fiber Entry")
            cat = st.selectbox("Type", ["MDF", "Pole", "FDH/JWI", "Node", "MST", "Vault"])
            aid = st.text_input("Asset ID")
            count = st.selectbox("Fiber Count", [12, 24, 48, 144, 288, 432, 864, 1728, 3456])
            if st.button("Submit for Approval"):
                try:
                    new_asset = supabase.table("network_assets").insert({
                        "user_id": st.session_state['user'].id,
                        "project_id": proj['id'],
                        "asset_id": aid,
                        "category": cat,
                        "count": count,
                        "status": "Pending"
                    }).execute()
                    managers = supabase.table("project_members").select("user_id").eq("project_id", proj['id']).eq("role", "Manager").execute()
                    for mgr in managers.data:
                        supabase.table("notifications").insert({"user_id": mgr['user_id'], "message": f"🔶 New entry {aid} submitted for approval."}).execute()
                    st.success(f"Submitted: {aid}")
                except Exception as e:
                    st.error(f"Failed: {e}")

        st.subheader("My Submitted Assets")
        my_assets = supabase.table("network_assets").select("*").eq("user_id", st.session_state['user'].id).eq("project_id", proj['id']).execute()
        if my_assets.data:
            for asset in my_assets.data:
                status_icon = "🔶" if asset['status'] == "Pending" else "✅" if asset['status'] == "Approved" else "❌"
                with st.expander(f"{status_icon} {asset['asset_id']} — {asset['category']} — {asset['count']} fibers — {asset['status']}"):
                    comments = supabase.table("asset_comments").select("*").eq("asset_id", asset['id']).execute()
                    if comments.data:
                        st.markdown("**Messages:**")
                        for c in comments.data:
                            st.markdown(f"> {c['message']} — *{c['created_at'][:10]}*")
                    reply = st.text_input("Reply to manager", key=f"reply_{asset['id']}")
                    if st.button("Send Reply", key=f"sendreply_{asset['id']}"):
                        if reply:
                            supabase.table("asset_comments").insert({"asset_id": asset['id'], "user_id": st.session_state['user'].id, "message": reply}).execute()
                            managers = supabase.table("project_members").select("user_id").eq("project_id", proj['id']).eq("role", "Manager").execute()
                            for mgr in managers.data:
                                supabase.table("notifications").insert({"user_id": mgr['user_id'], "message": f"💬 Tech replied on {asset['asset_id']}: {reply}"}).execute()
                            st.rerun()
        else:
            st.info("No assets submitted yet. Use the sidebar to add entries.")
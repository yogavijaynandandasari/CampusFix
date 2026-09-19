"""
app.py - CampusFix: Campus Maintenance Complaint & Tracking System
A high-performance, feature-rich Streamlit web application.
Faithfully recreates the CampusFix theme, live facility map, ticket tracking,
complaint registration, maintenance ledger, and real-time visual analytics.
"""

import os
import sys
from datetime import datetime
import pandas as pd
import streamlit as st

# Matplotlib figure support
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

# Ensure parent directory is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import database as db
import analysis

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="CampusFix — Campus Maintenance Control System",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Initialize database on startup
db.init_db()

# Custom CSS for Dark Navy High-End CampusFix UI
st.markdown(
    """
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* Base background styling */
    .stApp {
        background-color: #070B14;
        color: #F8FAFC;
    }

    /* Navbar / Header Banner */
    .campusfix-header {
        background: linear-gradient(180deg, #0B162C 0%, #080F1E 100%);
        border: 1px solid #1E2E4A;
        border-radius: 14px;
        padding: 18px 24px;
        margin-bottom: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }
    .brand-group {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .brand-logo-sq {
        background: linear-gradient(135deg, #0284C7, #0369A1);
        color: #FFFFFF;
        font-weight: 800;
        font-size: 20px;
        width: 44px;
        height: 44px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid #38BDF8;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.35);
    }
    .brand-title {
        font-size: 24px;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.5px;
        line-height: 1.1;
    }
    .brand-subtitle {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        color: #38BDF8;
    }
    .status-badge-online {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 14px;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.35);
        color: #34D399;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 8px #10B981;
    }

    /* Hero Section */
    .hero-container {
        background: radial-gradient(circle at 85% 20%, rgba(56, 189, 248, 0.08) 0%, transparent 50%),
                    linear-gradient(135deg, #0C1A30 0%, #060D1A 100%);
        border: 1px solid #1A2F50;
        border-radius: 16px;
        padding: 36px 32px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .hero-tag {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        background: rgba(56, 189, 248, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.2px;
        color: #38BDF8;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    .hero-title {
        font-size: 34px;
        font-weight: 800;
        line-height: 1.15;
        letter-spacing: -0.8px;
        color: #FFFFFF;
        margin-bottom: 12px;
    }
    .hero-title span.accent-orange {
        color: #F59E0B;
    }
    .hero-desc {
        color: #94A3B8;
        font-size: 15px;
        line-height: 1.6;
        max-width: 680px;
        margin-bottom: 18px;
    }

    /* KPI Metric Cards */
    .metric-card {
        background: linear-gradient(145deg, #0E1B31 0%, #091220 100%);
        border: 1px solid #1B2F4E;
        border-radius: 12px;
        padding: 16px 18px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        border-color: #38BDF8;
        transform: translateY(-2px);
    }
    .metric-val {
        font-size: 26px;
        font-weight: 800;
        color: #F8FAFC;
        line-height: 1.1;
        margin-bottom: 4px;
        font-family: 'JetBrains Mono', monospace;
    }
    .metric-lbl {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #94A3B8;
    }

    /* Facility / Campus Map Cards */
    .facility-card {
        background: #0D192C;
        border: 1px solid #1E3352;
        border-radius: 12px;
        padding: 16px;
        height: 100%;
    }
    .facility-title {
        font-size: 15px;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 4px;
    }
    .facility-meta {
        font-size: 12px;
        color: #94A3B8;
        margin-bottom: 8px;
    }

    /* Form Container */
    .register-card-wrapper {
        background: #FDFBF7;
        border-radius: 16px;
        padding: 28px 32px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        color: #0F172A;
    }
    .register-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 18px;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 12px;
    }
    .register-title {
        font-size: 22px;
        font-weight: 800;
        color: #0F172A;
        text-transform: uppercase;
        letter-spacing: -0.5px;
    }
    .badge-new-ticket {
        border: 1.5px dashed #EF4444;
        color: #DC2626;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Clean Streamlit elements adjustment */
    div.stButton > button {
        background-color: #0284C7;
        color: #FFFFFF;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        padding: 8px 18px;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        background-color: #0369A1;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.4);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# TOP NAVBAR
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="campusfix-header">
        <div class="brand-group">
            <div class="brand-logo-sq">CF</div>
            <div>
                <div class="brand-title">CampusFix</div>
                <div class="brand-subtitle">MAINTENANCE CONTROL SYSTEM</div>
            </div>
        </div>
        <div>
            <span class="status-badge-online">
                <span class="pulse-dot"></span>
                LIVE ACROSS 6 CAMPUS BUILDINGS
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# NAVIGATION TABS
# -----------------------------------------------------------------------------
nav_tabs = st.tabs(
    [
        "🚀 Dashboard",
        "📝 Register Complaint",
        "🎫 Ticket Console",
        "📊 Reports & Analysis",
        "🔧 Maintenance Ledger",
        "💾 System & Database",
    ]
)

# =============================================================================
# TAB 1: DASHBOARD
# =============================================================================
with nav_tabs[0]:
    metrics = analysis.calculate_metrics()

    # Hero Section matching image 3
    st.markdown(
        """
        <div class="hero-container">
            <div class="hero-tag">● Real-time Facility Operations</div>
            <div class="hero-title">
                EVERY SQUEAK, LEAK, AND <span class="accent-orange">FLICKER</span> —<br/>
                LOGGED, TRACKED, FIXED.
            </div>
            <div class="hero-desc">
                CampusFix turns scattered maintenance complaints into a single work-order board — 
                from the moment a student reports a broken fan to the day a technician closes the ticket.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 4 Quick Stat Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-val">{metrics['total_complaints']}</div>
                <div class="metric-lbl">TOTAL COMPLAINTS</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
            <div class="metric-card" style="border-left: 4px solid #EF4444;">
                <div class="metric-val" style="color: #F87171;">{metrics['pending']}</div>
                <div class="metric-lbl">PENDING REPAIRS</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""
            <div class="metric-card" style="border-left: 4px solid #38BDF8;">
                <div class="metric-val" style="color: #38BDF8;">{metrics['in_progress']}</div>
                <div class="metric-lbl">IN PROGRESS</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f"""
            <div class="metric-card" style="border-left: 4px solid #10B981;">
                <div class="metric-val" style="color: #34D399;">{metrics['resolved']}</div>
                <div class="metric-lbl">RESOLVED TICKETS</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Campus Buildings Facility Matrix
    st.subheader("📍 Campus Buildings & Facility Health")
    b_cols = st.columns(3)

    campus_buildings = [
        {"name": "Block A", "rooms": "Lecture Halls 101–315", "type": "Academic", "icon": "🏫", "desc": "Fans, Lighting & Switchboards"},
        {"name": "Block B", "rooms": "Rooms 101–212, Workshop", "type": "Departments", "icon": "🏛️", "desc": "Desks, Podiums & Classrooms"},
        {"name": "Block C", "rooms": "Laboratories 101–305", "type": "Science & Labs", "icon": "🔬", "desc": "Plumbing, Sink Drains & Windows"},
        {"name": "Computer Lab", "rooms": "AI Lab, Labs 1–3, Server Room", "type": "IT Infrastructure", "icon": "💻", "desc": "Workstations, LAN & Projectors"},
        {"name": "Library", "rooms": "Reading Halls 1–2, Digital Lib", "type": "Knowledge Hub", "icon": "📚", "desc": "Wi-Fi APs, Quiet Zones & Furniture"},
        {"name": "Hostel Block", "rooms": "Wings H1–H4, Dining Hall", "type": "Residential", "icon": "🛌", "desc": "AC/Cooling Units, Plumbing & Taps"},
    ]

    all_complaints = db.get_all_complaints()
    df_all = pd.DataFrame(all_complaints) if all_complaints else pd.DataFrame()

    for idx, bldg in enumerate(campus_buildings):
        col_idx = idx % 3
        with b_cols[col_idx]:
            bldg_count = 0
            pending_count = 0
            if not df_all.empty and "building" in df_all.columns:
                bldg_df = df_all[df_all["building"] == bldg["name"]]
                bldg_count = len(bldg_df)
                pending_count = len(bldg_df[bldg_df["status"] == "Pending"])

            health_status = (
                '<span style="color:#EF4444; font-weight:700;">⚠️ Needs Attention</span>'
                if pending_count > 3
                else '<span style="color:#10B981; font-weight:700;">✅ Stable</span>'
            )

            st.markdown(
                f"""
                <div class="facility-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div class="facility-title">{bldg['icon']} {bldg['name']}</div>
                        <div>{health_status}</div>
                    </div>
                    <div class="facility-meta">{bldg['rooms']} · {bldg['type']}</div>
                    <div style="font-size:12px; color:#94A3B8; margin-bottom:10px;">{bldg['desc']}</div>
                    <div style="display:flex; justify-content:space-between; font-size:12px; border-top:1px solid #1A2E4B; padding-top:8px;">
                        <span>Total Issues: <b>{bldg_count}</b></span>
                        <span style="color:#F87171;">Pending: <b>{pending_count}</b></span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    st.markdown("---")

    # Urgent Tickets Feed
    st.subheader("⚡ High-Priority Urgent Tickets Requiring Attention")
    if not df_all.empty:
        urgent_df = df_all[(df_all["priority"] == "High") & (df_all["status"] != "Resolved")].head(5)
        if not urgent_df.empty:
            display_cols = ["complaint_id", "student_name", "building", "room_no", "category", "problem", "status", "date"]
            st.dataframe(
                urgent_df[display_cols].rename(
                    columns={
                        "complaint_id": "Ticket ID",
                        "student_name": "Student",
                        "building": "Building",
                        "room_no": "Room",
                        "category": "Category",
                        "problem": "Problem Description",
                        "status": "Status",
                        "date": "Reported Date",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.success("No critical high-priority tickets are pending right now!")


# =============================================================================
# TAB 2: REGISTER COMPLAINT FORM (Matching reference screenshots 1 & 4)
# =============================================================================
with nav_tabs[1]:
    st.markdown("### 📝 Register a Complaint")
    st.caption("Fill in the details below — a ticket ID is generated automatically.")

    with st.container():
        # Styled Cream/Dark Form Card
        with st.form("register_complaint_form", clear_on_submit=True):
            r1c1, r1c2 = st.columns(2)
            with r1c1:
                student_name = st.text_input(
                    "STUDENT NAME *",
                    placeholder="e.g. Rahul Sharma",
                    help="Enter reporting student's full name",
                )
            with r1c2:
                department = st.selectbox(
                    "DEPARTMENT *",
                    [
                        "BCA",
                        "B.Tech CSE",
                        "B.Tech ECE",
                        "B.Tech ME",
                        "B.Tech IT",
                        "MCA",
                        "MBA",
                        "BBA",
                        "Civil Engineering",
                        "Hostel Block Administration",
                        "Other",
                    ],
                )

            r2c1, r2c2 = st.columns(2)
            with r2c1:
                building = st.selectbox(
                    "BUILDING *",
                    ["Block A", "Block B", "Block C", "Computer Lab", "Library", "Hostel Block", "Cafeteria", "Sports Complex"],
                )
            with r2c2:
                room_no = st.text_input(
                    "ROOM NO. *",
                    placeholder="e.g. 204 or Lab 2",
                    help="Specify room number, lab code, or corridor location",
                )

            r3c1, r3c2 = st.columns(2)
            with r3c1:
                category = st.selectbox(
                    "CATEGORY *",
                    [
                        "Electrical",
                        "Furniture",
                        "Plumbing",
                        "IT",
                        "Internet",
                        "Cleaning",
                        "AC/Cooling",
                        "Other",
                    ],
                )
            with r3c2:
                priority = st.selectbox(
                    "PRIORITY *",
                    ["Medium", "High", "Low"],
                    index=0,
                    help="Urgency level for maintenance dispatch",
                )

            problem = st.text_area(
                "PROBLEM DESCRIPTION *",
                placeholder="Describe what's wrong, e.g. 'Ceiling fan makes a loud noise and doesn't reach full speed.'",
                height=110,
            )

            col_btn, col_info = st.columns([1, 3])
            with col_btn:
                submitted = st.form_submit_button("Register complaint", use_container_width=True)
            with col_info:
                st.markdown(
                    "<span style='color:#94A3B8; font-size:13px;'>Date & ticket ID are assigned automatically on submit.</span>",
                    unsafe_allow_html=True,
                )

            if submitted:
                # Validation checks per project guidelines (Section 20)
                if not student_name.strip():
                    st.error("❌ Student Name cannot be blank.")
                elif not problem.strip():
                    st.error("❌ Problem Description cannot be blank.")
                elif not room_no.strip():
                    st.error("❌ Room No. cannot be blank.")
                else:
                    new_id = db.add_complaint(
                        student_name=student_name.strip(),
                        department=department,
                        building=building,
                        room_no=room_no.strip(),
                        category=category,
                        problem=problem.strip(),
                        priority=priority,
                        status="Pending",
                    )
                    st.success(f"🎉 Complaint Registered Successfully! Assigned Ticket ID: **{new_id}** (Status: **Pending**)")
                    st.balloons()


# =============================================================================
# TAB 3: TICKET CONSOLE (Search, Filter, Status Update, Maintenance Logging)
# =============================================================================
with nav_tabs[2]:
    st.markdown("### 🎫 Ticket Console & Complaint Tracking")
    st.caption("Search, filter, update complaint statuses, and attach maintenance repair records.")

    # Search & Filter Controls
    fc1, fc2, fc3, fc4 = st.columns([2, 1, 1, 1])
    with fc1:
        search_query = st.text_input(
            "🔍 Search Complaints",
            placeholder="Search by ID (e.g. CMP001), Student, Room, or Issue...",
        )
    with fc2:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "Pending", "In Progress", "Resolved"],
        )
    with fc3:
        building_filter = st.selectbox(
            "Filter by Building",
            ["All", "Block A", "Block B", "Block C", "Computer Lab", "Library", "Hostel Block"],
        )
    with fc4:
        category_filter = st.selectbox(
            "Filter by Category",
            ["All", "Electrical", "Furniture", "Plumbing", "IT", "Internet", "Cleaning", "AC/Cooling", "Other"],
        )

    # Fetch filtered data
    complaint_records = db.get_all_complaints(
        search_term=search_query if search_query.strip() else None,
        status_filter=status_filter,
        building_filter=building_filter,
        category_filter=category_filter,
    )

    if complaint_records:
        df_display = pd.DataFrame(complaint_records)
        st.write(f"Showing **{len(df_display)}** complaint tickets:")

        # Interactive Table
        cols_to_show = ["complaint_id", "student_name", "department", "building", "room_no", "category", "problem", "priority", "status", "date"]
        st.dataframe(
            df_display[cols_to_show].rename(
                columns={
                    "complaint_id": "Ticket ID",
                    "student_name": "Student",
                    "department": "Department",
                    "building": "Building",
                    "room_no": "Room",
                    "category": "Category",
                    "problem": "Problem",
                    "priority": "Priority",
                    "status": "Status",
                    "date": "Date",
                }
            ),
            use_container_width=True,
            height=320,
            hide_index=True,
        )
    else:
        st.warning("No complaints found matching your search and filter criteria.")

    st.markdown("---")

    # Ticket Action Center: Status Update & Maintenance Logging
    st.markdown("#### ⚡ Ticket Action Center")
    all_active_ids = [c["complaint_id"] for c in db.get_all_complaints()]

    if all_active_ids:
        selected_ticket_id = st.selectbox(
            "Select Complaint ID to inspect, update status, or add repair details:",
            all_active_ids,
        )

        ticket = db.get_complaint_by_id(selected_ticket_id)
        if ticket:
            t_col1, t_col2 = st.columns([1.2, 1.8])

            with t_col1:
                # Ticket Summary Card
                st.markdown(
                    f"""
                    <div style="background:#0F1C33; border:1px solid #1E3558; border-radius:12px; padding:18px;">
                        <div style="font-size:18px; font-weight:800; color:#38BDF8;">Ticket: {ticket['complaint_id']}</div>
                        <div style="font-size:13px; color:#94A3B8; margin-bottom:12px;">Reported on {ticket['date']}</div>
                        <div style="font-size:14px; margin-bottom:6px;"><b>Student:</b> {ticket['student_name']} ({ticket['department']})</div>
                        <div style="font-size:14px; margin-bottom:6px;"><b>Location:</b> {ticket['building']} — Room {ticket['room_no']}</div>
                        <div style="font-size:14px; margin-bottom:6px;"><b>Category:</b> {ticket['category']} | <b>Priority:</b> {ticket['priority']}</div>
                        <div style="font-size:14px; margin-bottom:10px;"><b>Problem:</b> {ticket['problem']}</div>
                        <div style="font-size:14px;"><b>Current Status:</b> <span style="background:#1E3A5F; padding:3px 8px; border-radius:4px; font-weight:700;">{ticket['status']}</span></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

                # Update Status Form
                with st.form("quick_status_form"):
                    st.markdown("##### 🔄 Update Status")
                    status_options = ["Pending", "In Progress", "Resolved"]
                    cur_index = status_options.index(ticket["status"]) if ticket["status"] in status_options else 0
                    new_status_val = st.selectbox("New Status", status_options, index=cur_index)
                    submit_status = st.form_submit_button("Save Status")

                    if submit_status:
                        db.update_complaint_status(ticket["complaint_id"], new_status_val)
                        st.success(f"Status updated to: {new_status_val}")
                        st.rerun()

            with t_col2:
                # Add Maintenance Details Form
                with st.form("add_maintenance_form"):
                    st.markdown("##### 🛠️ Add Maintenance / Repair Details")
                    st.caption("Log technician name, repair cost, and remarks for this complaint.")

                    m_c1, m_c2 = st.columns(2)
                    with m_c1:
                        tech_name = st.text_input("Technician / Staff Name *", placeholder="e.g. Amit Kumar")
                    with m_c2:
                        repair_date = st.date_input("Repair Date", datetime.now()).strftime("%Y-%m-%d")

                    m_c3, m_c4 = st.columns(2)
                    with m_c3:
                        repair_cost = st.number_input("Repair Cost (₹) *", min_value=0.0, step=50.0, value=250.0)
                    with m_c4:
                        auto_resolve = st.checkbox("Mark ticket as 'Resolved' automatically", value=True)

                    remarks = st.text_area(
                        "Repair Remarks *",
                        placeholder="e.g. Replaced capacitor, tightened loose wires and tested operation.",
                        height=75,
                    )

                    submit_maint = st.form_submit_button("Save Maintenance Record")

                    if submit_maint:
                        if not tech_name.strip():
                            st.error("Technician Name is required.")
                        elif not remarks.strip():
                            st.error("Repair remarks are required.")
                        else:
                            db.add_maintenance_record(
                                complaint_id=ticket["complaint_id"],
                                staff_name=tech_name.strip(),
                                repair_date=repair_date,
                                cost=repair_cost,
                                remarks=remarks.strip(),
                            )
                            if auto_resolve:
                                db.update_complaint_status(ticket["complaint_id"], "Resolved")
                            st.success(f"✅ Maintenance logged successfully for {ticket['complaint_id']}!")
                            st.rerun()

                # Display existing maintenance logs for this ticket
                m_logs = db.get_maintenance_for_complaint(ticket["complaint_id"])
                if m_logs:
                    st.markdown("##### 📋 Maintenance History for this Ticket")
                    for m in m_logs:
                        st.markdown(
                            f"""
                            <div style="background:#091220; border-left:3px solid #10B981; padding:10px 14px; margin-bottom:8px; border-radius:0 8px 8px 0;">
                                <div style="display:flex; justify-content:space-between;">
                                    <b>🔧 {m['staff_name']}</b>
                                    <span style="color:#10B981; font-weight:700;">₹{m['cost']:,.2f}</span>
                                </div>
                                <div style="font-size:12px; color:#94A3B8;">Repaired on {m['repair_date']}</div>
                                <div style="font-size:13px; margin-top:4px;">{m['remarks']}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )


# =============================================================================
# TAB 4: REPORTS & ANALYSIS (Matching reference screenshot 2)
# =============================================================================
with nav_tabs[3]:
    st.markdown("### 📊 REPORTS & ANALYSIS")
    st.caption("Everything Pandas would have crunched — rendered live.")

    metrics = analysis.calculate_metrics()
    df_complaints, df_maintenance = analysis.load_data()

    # CSV Export Button on top-right (matching screenshot 2)
    top_c1, top_c2 = st.columns([3, 1])
    with top_c2:
        if not df_complaints.empty:
            csv_data = df_complaints.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Export tickets to CSV",
                data=csv_data,
                file_name="complaints_report.csv",
                mime="text/csv",
                use_container_width=True,
            )

    # 8 KPI Metric Cards (2 Rows of 4 Cards)
    row1_c1, row1_c2, row1_c3, row1_c4 = st.columns(4)
    with row1_c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-val">{metrics['total_complaints']}</div>
                <div class="metric-lbl">TOTAL COMPLAINTS</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with row1_c2:
        st.markdown(
            f"""
            <div class="metric-card" style="border-top: 3px solid #EF4444;">
                <div class="metric-val" style="color: #F87171;">{metrics['pending']}</div>
                <div class="metric-lbl">PENDING</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with row1_c3:
        st.markdown(
            f"""
            <div class="metric-card" style="border-top: 3px solid #38BDF8;">
                <div class="metric-val" style="color: #38BDF8;">{metrics['in_progress']}</div>
                <div class="metric-lbl">IN PROGRESS</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with row1_c4:
        st.markdown(
            f"""
            <div class="metric-card" style="border-top: 3px solid #10B981;">
                <div class="metric-val" style="color: #34D399;">{metrics['resolved']}</div>
                <div class="metric-lbl">RESOLVED</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    row2_c1, row2_c2, row2_c3, row2_c4 = st.columns(4)
    with row2_c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-val" style="color:#38BDF8;">₹{metrics['total_cost']:,.0f}</div>
                <div class="metric-lbl">TOTAL MAINTENANCE COST</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with row2_c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-val" style="color:#A78BFA;">₹{metrics['avg_cost']:,.2f}</div>
                <div class="metric-lbl">AVERAGE REPAIR COST</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with row2_c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-val" style="font-size: 20px; color:#FBBF24;">{metrics['most_common_category']}</div>
                <div class="metric-lbl">MOST COMMON CATEGORY</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with row2_c4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-val" style="font-size: 20px; color:#67E8F9;">{metrics['most_reported_building']}</div>
                <div class="metric-lbl">MOST REPORTED BUILDING</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # Visualizations Row 1: Category Horizontal Bar Chart + Status Distribution Pie Chart
    chart_c1, chart_c2 = st.columns([1.1, 0.9])
    with chart_c1:
        fig_cat = analysis.generate_category_bar_chart(df_complaints)
        st.pyplot(fig_cat, use_container_width=True)
    with chart_c2:
        fig_pie = analysis.generate_status_pie_chart(df_complaints)
        st.pyplot(fig_pie, use_container_width=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # Visualizations Row 2: Building Bar Chart + Monthly Trend Line Chart
    chart_c3, chart_c4 = st.columns(2)
    with chart_c3:
        fig_bldg = analysis.generate_building_bar_chart(df_complaints)
        st.pyplot(fig_bldg, use_container_width=True)
    with chart_c4:
        fig_trend = analysis.generate_monthly_trend_chart(df_complaints)
        st.pyplot(fig_trend, use_container_width=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # Visualization Row 3: Maintenance Cost by Category
    st.markdown("#### 💰 Maintenance Expenditure Distribution by Category")
    fig_cost = analysis.generate_cost_by_category_chart(df_complaints, df_maintenance)
    st.pyplot(fig_cost, use_container_width=True)


# =============================================================================
# TAB 5: MAINTENANCE LEDGER
# =============================================================================
with nav_tabs[4]:
    st.markdown("### 🔧 Facility Maintenance & Repair Ledger")
    st.caption("Complete breakdown of campus repair jobs, technicians, parts cost, and work remarks.")

    m_all = db.get_all_maintenance_records()
    if m_all:
        df_m = pd.DataFrame(m_all)
        total_spent = df_m["cost"].sum() if "cost" in df_m.columns else 0

        # Summary KPIs for maintenance
        mc1, mc2, mc3 = st.columns(3)
        with mc1:
            st.metric("Total Completed Work Orders", len(df_m))
        with mc2:
            st.metric("Total Repair Expenditure", f"₹{total_spent:,.2f}")
        with mc3:
            avg_repair = df_m["cost"].mean() if len(df_m) > 0 else 0
            st.metric("Average Cost per Work Order", f"₹{avg_repair:,.2f}")

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        st.dataframe(
            df_m.rename(
                columns={
                    "id": "Record ID",
                    "complaint_id": "Ticket ID",
                    "staff_name": "Technician / Staff",
                    "repair_date": "Repair Date",
                    "cost": "Cost (₹)",
                    "remarks": "Action / Remarks",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No maintenance repair records found in the database yet.")


# =============================================================================
# TAB 6: SYSTEM & DATABASE SETTINGS
# =============================================================================
with nav_tabs[5]:
    st.markdown("### 💾 System Administration & Database Controls")
    st.caption("Inspect SQLite database health, schema definitions, and sample data seeding.")

    s_c1, s_c2 = st.columns(2)
    with s_c1:
        st.markdown("#### 🗄️ Database Information")
        st.write(f"- **Database Engine:** SQLite 3")
        st.write(f"- **Database File:** `{db.DB_PATH}`")
        st.write(f"- **Total Complaints Recorded:** {metrics['total_complaints']}")
        st.write(f"- **Total Maintenance Records:** {len(db.get_all_maintenance_records())}")

        if st.button("🔄 Refresh Database Statistics"):
            st.rerun()

    with s_c2:
        st.markdown("#### 📥 Full Data Export")
        st.caption("Download SQLite tables as CSV files for backup or project submissions.")

        df_c, df_m = analysis.load_data()
        if not df_c.empty:
            st.download_button(
                "Download Complaints Table (CSV)",
                df_c.to_csv(index=False).encode("utf-8"),
                "complaints_full.csv",
                "text/csv",
                key="dl_comp",
            )
        if not df_m.empty:
            st.download_button(
                "Download Maintenance Table (CSV)",
                df_m.to_csv(index=False).encode("utf-8"),
                "maintenance_full.csv",
                "text/csv",
                key="dl_maint",
            )

    st.markdown("---")
    st.markdown("#### 📑 Database Schema (Per Teacher's Guide Specifications)")
    st.code(
        """
-- Main table: complaints
CREATE TABLE complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    complaint_id TEXT UNIQUE NOT NULL,
    student_name TEXT NOT NULL,
    department TEXT NOT NULL,
    building TEXT NOT NULL,
    room_no TEXT NOT NULL,
    category TEXT NOT NULL,
    problem TEXT NOT NULL,
    priority TEXT NOT NULL,
    status TEXT NOT NULL,
    date TEXT NOT NULL
);

-- Second table: maintenance
CREATE TABLE maintenance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    complaint_id TEXT NOT NULL,
    staff_name TEXT NOT NULL,
    repair_date TEXT NOT NULL,
    cost REAL NOT NULL,
    remarks TEXT NOT NULL,
    FOREIGN KEY (complaint_id) REFERENCES complaints (complaint_id)
);
        """,
        language="sql",
    )

# Footer
st.markdown(
    """
    <div style="text-align: center; color: #64748B; font-size: 12px; margin-top: 40px; padding: 20px 0; border-top: 1px solid #1E293B;">
        CampusFix — Campus Maintenance Complaint & Tracking System | Major Project 2026–2027<br/>
        Built with Python, Streamlit, Tkinter, SQLite, Pandas & Matplotlib
    </div>
    """,
    unsafe_allow_html=True,
)

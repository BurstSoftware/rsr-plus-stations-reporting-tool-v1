import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Amazon RSR + Stations", layout="wide", page_icon="🚛")

st.title("🚛 Amazon RSR + Stations Dashboard")
st.markdown("**WMN7 / QMN7 • Real-time Shift Reporting & STAR Logs**")

# Initialize session state to store reports
if "reports" not in st.session_state:
    st.session_state.reports = []

# Sidebar Navigation
page = st.sidebar.selectbox(
    "Go to",
    ["📋 New General RSR Report", 
     "👥 Submit Manager STAR Report", 
     "👤 Manager Report History", 
     "📊 All Recent Reports"]
)

# ======================
# PAGE 1: General RSR Report
# ======================
if page == "📋 New General RSR Report":
    st.header("New General STAR Report")
    
    col1, col2 = st.columns(2)
    with col1:
        report_date = st.date_input("Date", datetime.now().date())
        report_time = st.time_input("Time", datetime.now().time())
    with col2:
        location = st.selectbox(
            "Location",
            ["WMN7 - Main Sort", "QMN7 - Delivery Station", "RTS - Returns",
             "Cafeteria", "Visitor Parking Lot", "Driver Parking Lot", "Traffic Control"]
        )
    
    st.subheader("STAR Report")
    situation = st.text_area("**Situation**", height=120, placeholder="Describe the current situation...")
    task = st.text_area("**Task**", height=80, placeholder="What needed to be done?")
    action = st.text_area("**Action**", height=120, placeholder="What actions did you take?")
    result = st.text_area("**Result**", height=80, placeholder="What was the outcome?")
    
    notes = st.text_area("Additional Notes / Photos / Follow-ups", height=100)
    
    if st.button("✅ Submit General RSR Report", type="primary", use_container_width=True):
        timestamp = f"{report_date} {report_time}"
        st.session_state.reports.append({
            "Timestamp": timestamp,
            "Manager": "General / Shift Lead",
            "Location": location,
            "Situation": situation,
            "Task": task,
            "Action": action,
            "Result": result,
            "Notes": notes
        })
        st.success(f"✅ General Report submitted successfully at {report_time} for **{location}**")

# ======================
# PAGE 2: Manager-Specific Submit
# ======================
elif page == "👥 Submit Manager STAR Report":
    st.header("Submit Manager STAR Report")
    
    managers = [
        "Dalton", "Emilio", "Jason", "Mike (District Manager)",
        "Mike (Process Assistant)", "Ashley (Process Assistant)",
        "Dan (Process Assistant)", "Elizet (Process Assistant)",
        "David (Process Assistant)", "Omar Musa (AM Back Half)",
        "Giselle (AM Front Half)", "Ken BH (UTR Multi)"
    ]
    
    selected_manager = st.selectbox("Select Manager", managers)
    
    st.subheader(f"⭐ STAR Report - {selected_manager}")
    
    col1, col2 = st.columns(2)
    with col1:
        m_date = st.date_input("Date", datetime.now().date(), key="m_date")
        m_time = st.time_input("Time", datetime.now().time(), key="m_time")
    with col2:
        m_location = st.selectbox("Location", 
            ["WMN7 - Main Sort", "QMN7 - Delivery Station", "RTS - Returns",
             "Cafeteria", "Visitor Parking Lot", "Driver Parking Lot", "Traffic Control"],
            key="m_loc")
    
    st.markdown("### STAR Breakdown")
    m_situation = st.text_area("**Situation**", height=110, placeholder="What happened?", key="sit")
    m_task = st.text_area("**Task**", height=80, placeholder="What was the objective?", key="task")
    m_action = st.text_area("**Action**", height=110, placeholder="What did you do?", key="action")
    m_result = st.text_area("**Result**", height=80, placeholder="What was the outcome?", key="result")
    
    m_notes = st.text_area("Additional Notes", height=100, key="notes")
    
    if st.button(f"Submit STAR Report for {selected_manager}", type="primary", use_container_width=True):
        timestamp = f"{m_date} {m_time}"
        st.session_state.reports.append({
            "Timestamp": timestamp,
            "Manager": selected_manager,
            "Location": m_location,
            "Situation": m_situation,
            "Task": m_task,
            "Action": m_action,
            "Result": m_result,
            "Notes": m_notes
        })
        st.success(f"✅ STAR Report submitted successfully for **{selected_manager}**")
        st.rerun()

# ======================
# PAGE 3: Manager Report History (NEW)
# ======================
elif page == "👤 Manager Report History":
    st.header("👤 Manager Report History")
    
    managers = [
        "Dalton", "Emilio", "Jason", "Mike (District Manager)",
        "Mike (Process Assistant)", "Ashley (Process Assistant)",
        "Dan (Process Assistant)", "Elizet (Process Assistant)",
        "David (Process Assistant)", "Omar Musa (AM Back Half)",
        "Giselle (AM Front Half)", "Ken BH (UTR Multi)", "General / Shift Lead"
    ]
    
    selected_manager = st.selectbox("Select Manager to View Reports", managers)
    
    # Filter reports for selected manager
    manager_reports = [r for r in st.session_state.reports if r["Manager"] == selected_manager]
    
    if manager_reports:
        st.subheader(f"Reports for **{selected_manager}** ({len(manager_reports)} total)")
        
        for idx, report in enumerate(reversed(manager_reports)):  # Show newest first
            with st.expander(f"📅 {report['Timestamp']} — {report['Location']}", expanded=(idx == 0)):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Situation**")
                    st.write(report["Situation"] or "—")
                    st.markdown("**Task**")
                    st.write(report["Task"] or "—")
                with col2:
                    st.markdown("**Action**")
                    st.write(report["Action"] or "—")
                    st.markdown("**Result**")
                    st.write(report["Result"] or "—")
                
                if report.get("Notes"):
                    st.markdown("**Additional Notes**")
                    st.write(report["Notes"])
    else:
        st.info(f"No reports found for **{selected_manager}** yet.")

# ======================
# PAGE 4: All Recent Reports
# ======================
else:
    st.header("📊 All Recent STAR Reports")
    
    if st.session_state.reports:
        df = pd.DataFrame(st.session_state.reports)
        st.dataframe(
            df[["Timestamp", "Manager", "Location", "Situation", "Result"]],
            use_container_width=True,
            hide_index=True
        )
        
        # Download button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download All Reports as CSV",
            data=csv,
            file_name=f"rsr_reports_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No reports submitted yet. Submit some reports to see them here.")

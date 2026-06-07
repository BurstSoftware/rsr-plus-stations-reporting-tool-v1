import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Amazon RSR + Stations", layout="wide", page_icon="🚛")
st.title("🚛 Amazon RSR + Stations Dashboard")
st.markdown("**WMN7 / QMN7 • Real-time Shift Reporting & STAR Logs**")

# Sidebar Navigation
page = st.sidebar.selectbox(
    "Go to",
    ["📋 New General RSR Report", "👥 Manager STAR Reports", "📊 Recent Reports"]
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
        st.success(f"✅ Report submitted successfully at {report_time} for **{location}**")

# ======================
# PAGE 2: Manager-Specific STAR Reports
# ======================
elif page == "👥 Manager STAR Reports":
    st.header("Manager STAR Reports")
    
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
        m_location = st.selectbox(
            "Location", 
            ["WMN7 - Main Sort", "QMN7 - Delivery Station", "RTS", "Cafeteria",
             "Visitor Parking Lot", "Driver Parking Lot", "Traffic Control"],
            key="m_loc"
        )
    
    st.markdown("### STAR Breakdown")
    m_situation = st.text_area("**Situation**", height=110, placeholder="What happened?", key="sit")
    m_task = st.text_area("**Task**", height=80, placeholder="What was the objective?", key="task")
    m_action = st.text_area("**Action**", height=110, placeholder="What did you do?", key="action")
    m_result = st.text_area("**Result**", height=80, placeholder="What was the outcome?", key="result")
    
    m_notes = st.text_area("Additional Notes", height=100, key="notes")
    
    if st.button(f"Submit STAR Report for {selected_manager}", type="primary", use_container_width=True):
        st.success(f"✅ STAR Report submitted successfully for **{selected_manager}** at {m_time}!")
        st.info("Report is now visible in Recent Reports.")

# ======================
# PAGE 3: Recent Reports (Mock + DataFrame)
# ======================
else:
    st.header("Recent STAR Reports")
    
    # Mock data
    data = {
        "Timestamp": ["2026-06-07 16:45", "2026-06-07 15:20", "2026-06-07 14:10", "2026-06-07 13:55"],
        "Manager": ["Dalton", "Giselle", "Omar Musa", "Ashley"],
        "Location": ["WMN7 - Main Sort", "QMN7", "Driver Parking Lot", "Traffic Control"],
        "Situation": ["Heavy congestion at gate", "RTS backlog", "Unauthorized parking", "Safety violation"],
        "Result": ["Flow restored in 18 min", "Backlog cleared", "Issue resolved", "Corrected on spot"]
    }
    
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.caption("All manager STAR reports will appear here in a real database setup.")

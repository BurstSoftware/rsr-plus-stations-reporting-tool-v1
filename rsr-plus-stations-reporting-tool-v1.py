import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Amazon RSR + Stations", layout="wide")
st.title("🚛 Amazon RSR + Stations Dashboard")
st.markdown("**WMN7 / QMN7 • Real-time Shift Reporting**")

tab1, tab2 = st.tabs(["📋 New RSR Report", "👥 Manager Pages"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Date", datetime.now().date())
        time = st.time_input("Time", datetime.now().time())
    with col2:
        location = st.selectbox("Location", 
            ["WMN7 - Main Sort", "QMN7 - Delivery Station", "RTS - Returns", 
             "Cafeteria", "Visitor Parking Lot", "Driver Parking Lot", "Traffic Control"])
    
    st.subheader("STAR Report")
    situation = st.text_area("Situation", height=100)
    task = st.text_area("Task", height=70)
    action = st.text_area("Action", height=100)
    result = st.text_area("Result", height=70)
    
    notes = st.text_area("Additional Notes / Follow-ups / Photos", height=120)
    
    if st.button("Submit RSR Report", type="primary", use_container_width=True):
        st.success("Report submitted successfully! Visible to all managers.")

with tab2:
    st.subheader("Manager Overview")
    managers = [
        "Dalton", "Emilio", "Jason", "Mike (District Manager)",
        "Mike (Process Assistant)", "Ashley (PA)", "Dan (PA)",
        "Elizet (PA)", "David (PA)", "Omar Musa (AM Back Half)",
        "Giselle (AM Front Half)", "Ken BH (UTR Multi)"
    ]
    
    cols = st.columns(4)
    for i, mgr in enumerate(managers):
        with cols[i % 4]:
            st.button(mgr, use_container_width=True)
    
    st.divider()
    st.subheader("Recent Reports")
    st.write("• WMN7 • 16:45 - Traffic resolved (Dalton)")
    st.write("• QMN7 • 15:20 - RTS backlog cleared (Giselle)")

import streamlit as st
from datetime import datetime
import pandas as pd
import json

st.set_page_config(page_title="Amazon RSR + Stations", layout="wide", page_icon="🚛")

st.title("🚛 Amazon RSR + Stations Dashboard")
st.markdown("**WMN7 / QMN7 • Real-time Shift Reporting & STAR Logs**")

# Initialize session state
if "reports" not in st.session_state:
    st.session_state.reports = []

# ======================
# SIDEBAR NAVIGATION
# ======================
page = st.sidebar.selectbox(
    "Go to",
    ["📋 New General RSR Report", 
     "👥 Submit Manager STAR Report", 
     "📤 Import JSON Reports", 
     "👤 Manager Report History", 
     "📊 All Recent Reports"]
)

# ======================
# PAGE 1: General Report
# ======================
if page == "📋 New General RSR Report":
    # ... (same as before)
    st.header("New General STAR Report")
    col1, col2 = st.columns(2)
    with col1:
        report_date = st.date_input("Date", datetime.now().date())
        report_time = st.time_input("Time", datetime.now().time())
    with col2:
        location = st.selectbox("Location", [
            "WMN7 - Main Sort", "QMN7 - Delivery Station", "RTS - Returns",
            "Cafeteria", "Visitor Parking Lot", "Driver Parking Lot", "Traffic Control"
        ])
    
    st.subheader("STAR Report")
    situation = st.text_area("**Situation**", height=120)
    task = st.text_area("**Task**", height=80)
    action = st.text_area("**Action**", height=120)
    result = st.text_area("**Result**", height=80)
    notes = st.text_area("Additional Notes", height=100)
    
    if st.button("✅ Submit General RSR Report", type="primary", use_container_width=True):
        timestamp = f"{report_date} {report_time}"
        st.session_state.reports.append({
            "Timestamp": timestamp, "Manager": "General / Shift Lead",
            "Location": location, "Situation": situation, "Task": task,
            "Action": action, "Result": result, "Notes": notes, "Source": "Manual"
        })
        st.success("Report submitted!")

# ======================
# PAGE 2: Manual Manager Report
# ======================
elif page == "👥 Submit Manager STAR Report":
    # ... (same as before - kept for completeness)
    st.header("Submit Manager STAR Report")
    managers = ["Dalton", "Emilio", "Jason", "Mike (District Manager)", "Mike (Process Assistant)",
                "Ashley (Process Assistant)", "Dan (Process Assistant)", "Elizet (Process Assistant)",
                "David (Process Assistant)", "Omar Musa (AM Back Half)", "Giselle (AM Front Half)",
                "Ken BH (UTR Multi)"]
    selected_manager = st.selectbox("Select Manager", managers)
    # ... rest of form same as previous version

# ======================
# NEW PAGE: Import JSON Reports
# ======================
elif page == "📤 Import JSON Reports":
    st.header("📤 Import Anonymous JSON Reports")
    st.info("Upload the .json files you received (Artur, Ashley, Mike S, etc.)")

    uploaded_files = st.file_uploader("Upload JSON Report Files", type=["json"], accept_multiple_files=True)

    if uploaded_files:
        for file in uploaded_files:
            try:
                data = json.load(file)
                body = data.get("body", {})
                text_body = body.get("text", "")

                # Extract fields
                manager_name = "Unknown"
                if "Complaint About:" in text_body:
                    manager_name = text_body.split("Complaint About:")[1].split("\n")[0].strip()

                situation = task = action = result = notes = ""
                if "Situation:" in text_body:
                    situation = text_body.split("Situation:")[1].split("Task:")[0].strip()
                if "Task:" in text_body:
                    task = text_body.split("Task:")[1].split("Action:")[0].strip()
                if "Action:" in text_body:
                    action = text_body.split("Action:")[1].split("Result:")[0].strip()
                if "Result:" in text_body:
                    result = text_body.split("Result:")[1].split("Additional Comments:")[0].strip()
                if "Additional Comments:" in text_body:
                    notes = text_body.split("Additional Comments:")[1].strip()

                timestamp = data.get("date", datetime.now().strftime("%Y-%m-%d %H:%M"))

                st.session_state.reports.append({
                    "Timestamp": timestamp,
                    "Manager": manager_name.strip(),
                    "Location": "Amazon RSR – North Mankato",
                    "Situation": situation,
                    "Task": task,
                    "Action": action,
                    "Result": result,
                    "Notes": notes,
                    "Source": "Imported JSON"
                })
                st.success(f"✅ Imported report for **{manager_name}**")
            except Exception as e:
                st.error(f"Failed to parse {file.name}: {e}")

# ======================
# PAGE: Manager Report History
# ======================
elif page == "👤 Manager Report History":
    st.header("👤 Manager Report History")
    
    all_managers = sorted(list(set([r["Manager"] for r in st.session_state.reports])))
    if not all_managers:
        all_managers = ["Artur", "Ashley", "Mike S", "Keven", "Mohammed", "Sayeed"] + \
                       ["Dalton", "Emilio", "Jason", "Mike (District Manager)"]
    
    selected_manager = st.selectbox("Select Manager to View Reports", all_managers)
    
    manager_reports = [r for r in st.session_state.reports if selected_manager.lower() in r["Manager"].lower()]
    
    if manager_reports:
        st.subheader(f"📋 Reports for **{selected_manager}** ({len(manager_reports)} total)")
        for idx, report in enumerate(reversed(manager_reports)):
            with st.expander(f"📅 {report['Timestamp']} — {report.get('Source', 'Manual')}", expanded=(idx == 0)):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Situation**"); st.write(report.get("Situation") or "—")
                    st.markdown("**Task**"); st.write(report.get("Task") or "—")
                with col2:
                    st.markdown("**Action**"); st.write(report.get("Action") or "—")
                    st.markdown("**Result**"); st.write(report.get("Result") or "—")
                if report.get("Notes"):
                    st.markdown("**Additional Notes**"); st.write(report["Notes"])
    else:
        st.info(f"No reports found for **{selected_manager}** yet.")

# ======================
# PAGE: All Reports
# ======================
else:
    st.header("📊 All Recent STAR Reports")
    if st.session_state.reports:
        df = pd.DataFrame(st.session_state.reports)
        st.dataframe(df[["Timestamp", "Manager", "Location", "Situation", "Result", "Source"]],
                     use_container_width=True, hide_index=True)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download All Reports as CSV", csv,
                           file_name=f"rsr_reports_{datetime.now().strftime('%Y%m%d')}.csv",
                           mime="text/csv")
    else:
        st.info("No reports yet. Import JSON files or submit new ones.")

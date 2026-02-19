import streamlit as st
import pandas as pd
import os
from src.auth import create_user_table, add_user, login_user
from src.face_capture import capture_faces
from src.face_recognize import recognize_faces
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Attendance System", layout="wide")

# Init DB
create_user_table()

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# ---------------- AMAZON UI ----------------
st.markdown("""
<style>
.stApp { background-color: #131921; color: white; }

header {visibility: hidden;}
section[data-testid="stSidebar"] {display: none;}

button {
    background-color: #FF9900 !important;
    color: black !important;
    border-radius: 6px;
    font-weight: bold;
    height: 48px;
    width: 128px;
}

button:hover {
    background-color: #e68a00 !important;
}

input {
    background-color: #232F3E !important;
    color: white !important;
    border: 1px solid #FF9900 !important;
}

h1, h2, h3 {
    color: #FF9900;
}

/* Navbar */
.navbar {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- NAVBAR ----------------
col1, col2 = st.columns([6,5])

with col1:
    st.markdown("## 🚀 AI Attendance System")

with col2:
    nav1, nav2, nav3, nav4, nav5 = st.columns(5)

    with nav1:
        if st.button("🏠 Dashboard"):
            st.session_state.page = "Dashboard"

    with nav2:
        if st.button("👤 Register"):
            st.session_state.page = "Register"

    with nav3:
        if st.button("📸 Attendance"):
            st.session_state.page = "Attendance"

    with nav4:
        if st.button("📊 Reports"):
            st.session_state.page = "Reports"

    with nav5:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.rerun()

# ---------------- AUTH ----------------
if not st.session_state.logged_in:

    st.markdown("## Login / Signup")

    tab1, tab2 = st.tabs(["Login", "Signup"])

    # LOGIN
    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            result = login_user(username, password)
            if result:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome {username}")
                st.rerun()
            else:
                st.error("Invalid credentials")

    # SIGNUP
    with tab2:
        new_user = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")

        if st.button("Signup"):
            add_user(new_user, new_password)
            st.success("Account created successfully")

# ---------------- MAIN APP ----------------
else:
    st.success(f"Welcome {st.session_state.username}")

    page = st.session_state.page

    # ---------------- DASHBOARD ----------------
    if page == "Dashboard":
        st.markdown("## Dashboard Overview")

        file_path = "attendance/attendance.csv"

        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            df = pd.read_csv(file_path)

            if df.empty:
                st.warning("No attendance data yet")
                st.stop()

            if "Date" in df.columns and "Time" in df.columns:
                df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
                df["Time"] = pd.to_datetime(df["Time"], format="%H:%M:%S", errors="coerce")

                df["DateTime"] = df["Date"] + (df["Time"] - df["Time"].dt.normalize())
                df = df.dropna(subset=["DateTime"])

                df["Hour"] = df["DateTime"].dt.hour
            else:
                st.error("CSV must contain Name, Date, Time")
                st.stop()

            # Metrics
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total Records", len(df))

            with col2:
                st.metric("Unique Users", df["Name"].nunique())

            with col3:
                last_entry = df.sort_values(by="DateTime", ascending=False).iloc[0]
                st.metric("Last Entry", str(last_entry["DateTime"]))

            # Hourly chart
            hourly = df.groupby("Hour").size().reset_index(name="Count")

            fig = px.bar(hourly, x="Hour", y="Count", text="Count")
            fig.update_traces(marker_color="#FF9900", textposition="outside")
            fig.update_layout(
                plot_bgcolor="#131921",
                paper_bgcolor="#131921",
                font=dict(color="white")
            )

            st.plotly_chart(fig, use_container_width=True)

            # Daily trend
            daily = df.groupby(df["Date"]).size().reset_index(name="Count")

            fig2 = px.line(daily, x="Date", y="Count", markers=True)
            fig2.update_layout(
                plot_bgcolor="#131921",
                paper_bgcolor="#131921",
                font=dict(color="white")
            )

            st.plotly_chart(fig2, use_container_width=True)

        else:
            st.info("No attendance records yet")

    # ---------------- REGISTER ----------------
    elif page == "Register":
        st.subheader("Register User")

        name = st.text_input("Enter Name")

        if st.button("Capture Faces"):
            st.info("Press 'q' to stop camera")
            capture_faces(name)
            st.success("Face registered successfully")

    # ---------------- ATTENDANCE ----------------
    elif page == "Attendance":
        st.subheader("Start Attendance")

        if st.button("Start Attendance"):
            st.info("Press 'q' to exit camera")
            recognize_faces()
            st.success("Attendance completed")

    # ---------------- REPORTS ----------------
    elif page == "Reports":
        st.subheader("Attendance Records")

        file_path = "attendance/attendance.csv"

        if os.path.exists(file_path):
            df = pd.read_csv(file_path)

            if df.empty:
                st.warning("No data available")
                st.stop()

            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
            df["Time"] = pd.to_datetime(df["Time"], format="%H:%M:%S", errors="coerce")

            df["DateTime"] = df["Date"] + (df["Time"] - df["Time"].dt.normalize())
            df = df.dropna(subset=["DateTime"])

            df = df.sort_values(by="DateTime", ascending=False)

            st.dataframe(df)

            if not df.empty:
                st.warning(f"Last Entry: {df.iloc[0]['DateTime']}")

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, "attendance.csv")

            if st.button("Refresh"):
                st.rerun()

        else:
            st.info("No attendance records yet")

# ---------------- FOOTER ----------------
st.markdown("""
---
👨‍💻 Project Developed by Kotari Chaitanya Krishna  
| AI & ML
""")

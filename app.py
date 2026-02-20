import streamlit as st
import pandas as pd
import os
from datetime import datetime
from src.auth import create_user_table, add_user, login_user
from src.face_capture import capture_faces
from src.face_recognize import recognize_faces

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Attendance System", layout="wide")

# Init DB
create_user_table()

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# ---------------- UI STYLE ----------------
st.markdown("""
<style>
.stApp { background-color: #131921; color: white; }

header {visibility: hidden;}
section[data-testid="stSidebar"] {display: none;}

button {
    background-color: #FF9900 !important;
    color: black !important;
    border-radius: 8px !important;
    font-weight: bold;
    height: 45px;
    width: 120px;
}

/* 👁️ ONLY password eye button */
div[data-testid="stTextInput"] button {
    width: 35px !important;
    height: 35px !important;
    padding: 0px !important;
}

button:hover {
    background-color: #e68a00 !important;
}

input {
    background-color: #232F3E !important;
    color: white !important;
    border: 1px solid #FF9900 !important;
    border-radius: 10px !important;
    padding: 10px !important;
}

h1, h2, h3 {
    color: #FF9900;
}
</style>
""", unsafe_allow_html=True)

# ---------------- NAVBAR ----------------
col1, col2 = st.columns([5,6])

with col1:
    st.markdown("## 🚀 AI Attendance System")

with col2:
    nav = st.columns(5)

    if nav[0].button("🏠 Dashboard"):
        st.session_state.page = "Dashboard"

    if nav[1].button("👤 Register"):
        st.session_state.page = "Register"

    if nav[2].button("📸 Attendance"):
        st.session_state.page = "Attendance"

    if nav[3].button("📊 Reports"):
        st.session_state.page = "Reports"

    if nav[4].button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

# 🕒 CLOCK
st.markdown(f"🕒 {datetime.now().strftime('%d %b %Y | %I:%M:%S %p')}")

# ---------------- AUTH ----------------
if not st.session_state.logged_in:

    st.markdown("## Login / Signup")

    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        col1, col2, col3 = st.columns([2,3,2])
        with col2:
            st.markdown("### 🔐 Login")

            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                if login_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(f"Welcome {username}")
                    st.rerun()
                else:
                    st.error("Invalid credentials")

    with tab2:
        col1, col2, col3 = st.columns([2,3,2])
        with col2:
            st.markdown("### 📝 Signup")

            new_user = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")

            if st.button("Signup"):
                add_user(new_user, new_password)
                st.success("Account created successfully")

# ---------------- MAIN APP ----------------
else:
    st.success(f"Welcome {st.session_state.username}")
    st.success("🟢 System Active")

    page = st.session_state.page

    # ---------------- DASHBOARD ----------------
    if page == "Dashboard":
        st.markdown("## 📊 Dashboard Overview")

        file_path = "attendance/attendance.csv"

        if os.path.exists(file_path):
            df = pd.read_csv(file_path)

            if not df.empty:
                df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date
                df["Time"] = pd.to_datetime(df["Time"], format="%H:%M:%S", errors="coerce").dt.time

                df["DateTime"] = pd.to_datetime(
                    df["Date"].astype(str) + " " + df["Time"].astype(str),
                    errors="coerce"
                )

                df = df.dropna()

                last = df.sort_values(by="DateTime", ascending=False).iloc[0]

                col1, col2, col3 = st.columns(3)

                col1.metric("Total Records", len(df))
                col2.metric("Users", df["Name"].nunique())
                col3.metric("Last Entry", last["DateTime"].strftime("%d %b %Y %I:%M %p"))

        else:
            st.info("No data")

    # ---------------- REGISTER ----------------
    elif page == "Register":
        st.subheader("📸 Register User")

        name = st.text_input("Enter Name")

        if st.button("Capture Faces"):
            capture_faces(name)
            st.success("Face Registered")

    # ---------------- ATTENDANCE ----------------
    elif page == "Attendance":
        st.subheader("🎥 Start Attendance")

        if st.button("Start Attendance"):
            recognize_faces()
            st.success("Attendance Completed")

    # ---------------- REPORTS ----------------
    elif page == "Reports":
        st.subheader("📋 Attendance Records")

        file_path = "attendance/attendance.csv"

        if os.path.exists(file_path):
            df = pd.read_csv(file_path)

            if df.empty:
                st.warning("No data")
                st.stop()

            # FIX DATE TIME
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date
            df["Time"] = pd.to_datetime(df["Time"], format="%H:%M:%S", errors="coerce").dt.time

            df["DateTime"] = pd.to_datetime(
                df["Date"].astype(str) + " " + df["Time"].astype(str),
                errors="coerce"
            )

            df = df.dropna()
            df = df.sort_values(by="DateTime", ascending=False)

            # 🔍 FILTERS
            st.markdown("### 🔍 Filters")
            col1, col2 = st.columns(2)

            with col1:
                search = st.text_input("Search Name")

            with col2:
                date_filter = st.date_input("Filter Date", value=None)

            filtered_df = df.copy()

            if search:
                filtered_df = filtered_df[
                    filtered_df["Name"].str.lower().str.contains(search.lower())
                ]

            if date_filter:
                filtered_df = filtered_df[
                    filtered_df["Date"] == date_filter
                ]

            st.markdown("### 📄 Data")
            st.dataframe(filtered_df, use_container_width=True)

            # 📊 SUMMARY
            summary = filtered_df.groupby("Name").agg(
                Total_Entries=("Name", "count"),
                Days_Present=("Date", "nunique")
            ).reset_index()

            total_days = filtered_df["Date"].nunique()

            summary["Attendance %"] = (summary["Days_Present"] / total_days) * 100
            summary["Status"] = summary["Attendance %"].apply(
                lambda x: "Good" if x >= 75 else "Low"
            )

            st.markdown("### 📊 Summary")
            st.dataframe(summary)

            # LAST ENTRY
            if not filtered_df.empty:
                last = filtered_df.iloc[0]["DateTime"]
                st.success(f"🕒 Last Entry: {last}")

            # DOWNLOAD
            csv = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, "attendance.csv")

        else:
            st.info("No records")

# ---------------- FOOTER ----------------
st.markdown("""
---
👨‍💻 Developed by Kotari Chaitanya Krishna  
AI & ML Project
""")

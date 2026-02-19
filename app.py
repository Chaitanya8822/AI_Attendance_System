import streamlit as st
import pandas as pd
import os
from src.auth import create_user_table, add_user, login_user
from src.face_capture import capture_faces
from src.face_recognize import recognize_faces
import plotly.express as px

# Init DB
create_user_table()

st.set_page_config(page_title="AI Attendance System", layout="wide")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0e1117;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🚀 AI Smart Attendance System")

# Add logout button in sidebar
if st.session_state.logged_in:
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# Login/Signup Logic
if not st.session_state.logged_in:
    menu = ["Login", "Signup"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Signup":
        st.subheader("📝 Create Account")

        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type="password")

        if st.button("Signup"):
            add_user(new_user, new_password)
            st.success("Account created successfully!")

    elif choice == "Login":
        st.subheader("🔐 Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            result = login_user(username, password)

            if result:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome {username} 🎉")
                st.rerun()
            else:
                st.error("Invalid credentials")

else:
    st.success(f"Welcome {st.session_state.username} 🎉")

    # Dashboard Navigation
    menu2 = ["Dashboard", "Register", "Attendance", "Reports"]
    choice2 = st.sidebar.selectbox("Navigation", menu2)

    # -------- DASHBOARD --------
    if choice2 == "Dashboard":
        st.subheader("📊 Dashboard Overview")

        file_path = "attendance/attendance.csv"

        if os.path.exists(file_path):
            df = pd.read_csv(file_path)

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Total Records", len(df))

            with col2:
                st.metric("Unique Users", df["Name"].nunique())

            # Chart
            df["Time"] = pd.to_datetime(df["Time"])
            df["Hour"] = df["Time"].dt.hour

            fig = px.histogram(df, x="Hour", title="Attendance by Hour")
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("No attendance data available")

    # -------- REGISTER --------
    elif choice2 == "Register":
        st.subheader("📸 Register New User")

        name = st.text_input("Enter Name")

        if st.button("Capture Faces"):
            capture_faces(name)
            st.success("Face data captured!")

    # -------- ATTENDANCE --------
    elif choice2 == "Attendance":
        st.subheader("🎥 Start Attendance")

        if st.button("Start Camera"):
            recognize_faces()

    # -------- REPORTS --------
    elif choice2 == "Reports":
        st.subheader("📋 Attendance Records")

        if os.path.exists("attendance/attendance.csv"):
            df = pd.read_csv("attendance/attendance.csv")
            st.dataframe(df)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, "attendance.csv")

        else:
            st.warning("No data found")

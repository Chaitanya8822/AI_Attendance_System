# AI Attendance System Main Application
import streamlit as st
import os
import pandas as pd

st.set_page_config(page_title="AI Attendance System", layout="centered")

st.title("🎯 AI Smart Attendance System")

menu = ["Home", "Register User", "Start Attendance", "View Attendance"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- HOME ----------------
if choice == "Home":
    st.subheader("Welcome 👋")
    st.write("AI-based attendance system using Face Recognition")

# ---------------- REGISTER ----------------
elif choice == "Register User":
    st.subheader("📸 Register New User")

    name = st.text_input("Enter Name")

    if st.button("Capture Faces"):
        if name:
            os.system(f"python src/face_capture.py")
            st.success(f"Face data captured for {name}")
        else:
            st.warning("Please enter a name")

# ---------------- ATTENDANCE ----------------
elif choice == "Start Attendance":
    st.subheader("🎥 Start Attendance")

    if st.button("Start Camera"):
        os.system("python src/face_recognize.py")

# ---------------- VIEW ----------------
elif choice == "View Attendance":
    st.subheader("📊 Attendance Records")

    file_path = "attendance/attendance.csv"

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        st.dataframe(df)
    else:
        st.warning("No attendance records found")

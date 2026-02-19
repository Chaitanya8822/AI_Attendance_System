import streamlit as st
from src.auth import create_user_table, add_user, login_user
import os
import pandas as pd

create_user_table()

st.title("🔐 AI Attendance System Login")

menu = ["Login", "Signup"]
choice = st.sidebar.selectbox("Menu", menu)

# -------- SIGNUP --------
if choice == "Signup":
    st.subheader("Create New Account")

    new_user = st.text_input("Username")
    new_password = st.text_input("Password", type="password")

    if st.button("Signup"):
        add_user(new_user, new_password)
        st.success("Account created successfully!")

# -------- LOGIN --------
elif choice == "Login":
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        result = login_user(username, password)

        if result:
            st.success(f"Welcome {username}")

            # After login → show main app
            menu2 = ["Home", "Register", "Attendance", "View"]

            choice2 = st.selectbox("Menu", menu2)

            if choice2 == "Home":
                st.write("Welcome to AI Attendance System")

            elif choice2 == "Register":
                name = st.text_input("Enter Name")
                if st.button("Capture"):
                    os.system("python src/face_capture.py")

            elif choice2 == "Attendance":
                if st.button("Start"):
                    os.system("python src/face_recognize.py")

            elif choice2 == "View":
                if os.path.exists("attendance/attendance.csv"):
                    df = pd.read_csv("attendance/attendance.csv")
                    st.dataframe(df)
                else:
                    st.warning("No data")

        else:
            st.error("Invalid credentials")

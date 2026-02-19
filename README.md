# 🚀 AI Smart Attendance System

An AI-powered face recognition attendance system built using Python, OpenCV, and Streamlit.  
This system detects faces in real-time, verifies liveness, and automatically marks attendance with date and time.

---

## 📌 Features

✅ Face Recognition using OpenCV (LBPH)  
✅ Liveness Detection (Anti-Spoofing)  
✅ Real-time Attendance Marking  
✅ Streamlit Web Dashboard  
✅ Secure Login & Signup System  
✅ Attendance Reports & Download  
✅ Hourly & Daily Analytics Charts  
✅ Amazon-style Professional UI  

---

## 🛠️ Tech Stack

- Python 🐍
- OpenCV 👁️
- Streamlit 🌐
- Pandas 📊
- NumPy 🔢
- Plotly 📈
- SQLite (for login system)

---

## 📂 Project Structure

AI_Attendance_System/
│
├── attendance/
│ └── attendance.csv
│
├── data/
│ └── (captured face images)
│
├── models/
│ ├── face_model.xml
│ └── labels.npy
│
├── src/
│ ├── auth.py
│ ├── face_capture.py
│ ├── face_train.py
│ ├── face_recognize.py
│ └── liveness.py
│
├── app.py
├── database.db
├── requirements.txt
└── README.md


---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/AI_Attendance_System.git
cd AI_Attendance_System
2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate
3️⃣ Install Requirements
pip install -r requirements.txt
▶️ How to Run
🔹 Step 1: Capture Faces
python src/face_capture.py
🔹 Step 2: Train Model
python src/face_train.py
🔹 Step 3: Start Attendance System
python src/face_recognize.py
Press Q to stop camera.

🔹 Step 4: Run Web App
streamlit run app.py
🔐 Login Details
You can create your own account using Signup in the app.

📊 Dashboard Features
📌 Total Attendance Records

👤 Unique Users

🕒 Last Entry Time

📈 Daily Trends

📊 Hourly Attendance Chart

📁 Attendance Format
Name,Date,Time
John,2026-02-19,10:30:21
⚠️ Notes
Ensure good lighting for better accuracy

Press Q to exit camera

Avoid duplicate face registrations

Liveness detection prevents fake images

🚀 Future Improvements
🌐 Deploy on cloud (Streamlit Cloud / AWS)

📱 Mobile responsive UI

📸 Store face snapshots

🔔 Email/SMS notifications

🧠 Deep Learning (FaceNet / ArcFace)

👨‍💻 Author

Kotari Chaitanya Krishna
💻 Python | AI | ML | Data Science
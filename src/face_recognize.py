# Face Recognition Module
# Handles recognizing faces and marking attendance

import cv2
import numpy as np
import os
from datetime import datetime
from src.liveness import detect_liveness

# 🔥 Prevent duplicate marking in same session
marked_names = set()


# ---------------- ATTENDANCE FUNCTION ----------------
marked_names = set()   # keep this at top of file

def mark_attendance(name):
    global marked_names

    os.makedirs("attendance", exist_ok=True)
    file_path = "attendance/attendance.csv"

    # Create file if not exists
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("Name,Date,Time\n")

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    # 🔒 SESSION CHECK (avoid loop duplicates)
    if name in marked_names:
        return

    # 🔍 DAILY CHECK (avoid duplicates across runs)
    with open(file_path, "r") as f:
        lines = f.readlines()

    for line in lines[1:]:  # skip header
        data = line.strip().split(",")

        if len(data) >= 2:
            recorded_name = data[0]
            recorded_date = data[1]

            if recorded_name == name and recorded_date == date_str:
                print(f"⚠️ {name} already marked today")
                marked_names.add(name)  # also block in session
                return

    # ✅ Mark attendance
    with open(file_path, "a") as f:
        f.write(f"{name},{date_str},{time_str}\n")

    marked_names.add(name)

    print(f"✅ Attendance marked for {name}")



# ---------------- FACE RECOGNITION ----------------
def recognize_faces():
    # Load trained model
    model = cv2.face.LBPHFaceRecognizer_create()
    model.read("models/face_model.xml")

    # Load label map
    label_map = np.load("models/labels.npy", allow_pickle=True).item()

    cam = cv2.VideoCapture(0)

    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    # Liveness check
    if not detect_liveness():
        print("❌ Liveness failed")
        return

    print("🎥 Starting attendance system...")

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (200, 200))

            label, confidence = model.predict(face)

            name = label_map.get(label, "Unknown")

            print(f"Detected: {name}, Confidence: {confidence}")




            # Recognition condition
            if confidence < 90:
                mark_attendance(name)

                text = f"{name} ({round(confidence, 2)})"
                color = (0, 255, 0)
            else:
                text = "Unknown"
                color = (0, 0, 255)

            # Draw rectangle + label
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        cv2.imshow("Attendance System", frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


# ---------------- RUN FILE ----------------
if __name__ == "__main__":
    recognize_faces()

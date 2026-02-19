# Face Recognition Module
# Handles recognizing faces and marking attendance
import cv2
import numpy as np
import os
from datetime import datetime
from liveness import detect_liveness

def mark_attendance(name):
    os.makedirs("attendance", exist_ok=True)
    file_path = "attendance/attendance.csv"

    # Create file if not exists
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("Name,Time\n")

    with open(file_path, "r+") as f:
        data = f.readlines()
        names = [line.split(",")[0] for line in data]

        if name not in names:
            now = datetime.now()
            time_str = now.strftime("%H:%M:%S")
            f.write(f"{name},{time_str}\n")
            print(f"✅ Attendance marked for {name}")

def recognize_faces():
    # Load model
    model = cv2.face.LBPHFaceRecognizer_create()
    model.read("models/face_model.xml")

    label_map = np.load("models/labels.npy", allow_pickle=True).item()

    cam = cv2.VideoCapture(0)

    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    if not detect_liveness():
        print("❌ Liveness failed")
        exit()

    print("🎥 Starting attendance system...")

    while True:
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (200, 200))

            label, confidence = model.predict(face)

            if confidence < 70:
                name = label_map[label]
                mark_attendance(name)
                text = f"{name} ({round(confidence, 2)})"
                color = (0, 255, 0)
            else:
                text = "Unknown"
                color = (0, 0, 255)

            cv2.rectangle(frame, (x,y), (x+w,y+h), color, 2)
            cv2.putText(frame, text, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        cv2.imshow("Attendance System", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize_faces()

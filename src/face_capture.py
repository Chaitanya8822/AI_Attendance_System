# Face Capture Module
# Handles capturing and processing face images for attendance tracking
import cv2
import os

def capture_faces(user_name):
    # Create user folder
    path = f"data/{user_name}"
    os.makedirs(path, exist_ok=True)

    cam = cv2.VideoCapture(0)

    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    count = 0

    print("📸 Capturing faces... Look at the camera")

    while True:
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            count += 1

            face = frame[y:y+h, x:x+w]
            file_name = f"{path}/{count}.jpg"
            cv2.imwrite(file_name, face)

            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)

        cv2.imshow("Face Capture", frame)

        # Stop after 50 images OR press 'q'
        if count >= 50 or cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

    print("✅ Face data collected successfully!")

if __name__ == "__main__":
    name = input("Enter user name: ")
    capture_faces(name)

# Face Training Module
# Handles training and model building for face recognition
import cv2
import os
import numpy as np

def train_model():
    data_path = "data"
    faces = []
    labels = []
    label_map = {}

    current_label = 0

    print("🧠 Training model...")

    for user in os.listdir(data_path):
        user_path = os.path.join(data_path, user)

        if not os.path.isdir(user_path):
            continue

        label_map[current_label] = user

        for image_name in os.listdir(user_path):
            image_path = os.path.join(user_path, image_name)

            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

            if img is None:
                continue

            # Resize all images to same size
            img = cv2.resize(img, (200, 200))

            faces.append(img)
            labels.append(current_label)

        current_label += 1

    labels = np.array(labels)

    # Train LBPH model
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(faces, labels)

    # Save model
    os.makedirs("models", exist_ok=True)
    model.save("models/face_model.xml")

    # Save label map
    np.save("models/labels.npy", label_map)

    print("✅ Model trained and saved!")

if __name__ == "__main__":
    train_model()

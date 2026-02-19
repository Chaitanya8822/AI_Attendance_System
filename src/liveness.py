# Liveness Detection Module
# Handles detecting if a face is actually a live person (anti-spoofing)
import cv2

def detect_liveness():
    cam = cv2.VideoCapture(0)

    ret, prev_frame = cam.read()
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    print("👁️ Move your face slightly to verify liveness...")

    motion_detected = False
    frame_count = 0

    while True:
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Compute difference
        diff = cv2.absdiff(prev_gray, gray)
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

        motion = cv2.countNonZero(thresh)

        if motion > 5000:
            motion_detected = True
            print("✅ Liveness confirmed!")
            break

        prev_gray = gray
        frame_count += 1

        cv2.imshow("Liveness Check", frame)

        if cv2.waitKey(1) & 0xFF == ord('q') or frame_count > 100:
            break

    cam.release()
    cv2.destroyAllWindows()

    return motion_detected

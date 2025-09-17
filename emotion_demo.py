import cv2
from deepface import DeepFace

# Use DirectShow backend for Windows webcams
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Webcam opened successfully. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    try:
        # Analyze the full frame for better face detection
        result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)

        # DeepFace.analyze may return a list if multiple faces are detected
        if isinstance(result, list):
            result = result[0]

        if isinstance(result, dict) and "dominant_emotion" in result:
            emotion = result["dominant_emotion"]
            confidence = result["emotion"][emotion]

            # Debug: print detected emotion in console
            print(f"Detected: {emotion} ({confidence:.2f}%)")

            # Display on frame
            cv2.putText(
                frame,
                f"{emotion} ({int(confidence)}%)",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )
    except Exception as e:
        print("Skipping frame:", e)

    # Resize frame for faster display
    display_frame = cv2.resize(frame, (640, 480))
    cv2.imshow("AI Emotion Detector", display_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print("Webcam closed. Program ended.")

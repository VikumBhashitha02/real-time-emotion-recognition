import cv2
from deepface import DeepFace

# Open webcam
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
        # Analyze all faces in the frame for emotion, age, and gender
        results = DeepFace.analyze(
            frame, actions=["emotion", "age", "gender"], enforce_detection=False
        )

        # DeepFace may return a list if multiple faces are found
        if isinstance(results, dict):
            results = [results]

        for idx, res in enumerate(results):
            # Bounding box info (may not exist if enforce_detection=False and no face found)
            region = res.get("region", {})
            x, y, w, h = (
                region.get("x", 0),
                region.get("y", 0),
                region.get("w", 0),
                region.get("h", 0),
            )

            # Draw a rectangle around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Extract predictions
            emotion = res.get("dominant_emotion", "Unknown")
            gender = res.get("dominant_gender", "Unknown")
            age = res.get("age", "N/A")

            # Text to display: Gender | Age | Emotion
            text = f"{gender}, {age} yrs, {emotion}"

            # Put the text above the rectangle
            cv2.putText(
                frame,
                text,
                (x, y - 10 if y - 10 > 20 else y + h + 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )

            # Debug console print
            print(f"Person {idx}: {gender}, {age} yrs, {emotion}")

    except Exception as e:
        print("Skipping frame:", e)

    # Resize frame for smoother display
    display_frame = cv2.resize(frame, (640, 480))
    cv2.imshow("AI Multi-Face Detector", display_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print("Webcam closed. Program ended.")

import cv2
import time
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D

# ================= CNN MODEL =================
model = Sequential()
model.add(Conv2D(32, (3,3), activation='relu', input_shape=(48,48,1)))
model.add(Conv2D(64, (3,3), activation='relu'))
model.add(MaxPooling2D((2,2)))
model.add(Conv2D(128, (3,3), activation='relu'))
model.add(MaxPooling2D((2,2)))
model.add(Conv2D(128, (3,3), activation='relu'))
model.add(MaxPooling2D((2,2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(7, activation='softmax'))

model.load_weights("model.h5")

emotion_dict = {
    0: "Angry",
    1: "Disgusted",
    2: "Fearful",
    3: "Happy",
    4: "Neutral",
    5: "Sad",
    6: "Surprised"
}

# 🎨 Emotion → Color (BGR)
emotion_colors = {
    "Happy": (0, 255, 0),        # Green
    "Sad": (255, 0, 0),          # Blue
    "Angry": (0, 0, 255),        # Red
    "Fearful": (128, 0, 128),    # Purple
    "Neutral": (255, 255, 255),  # White
    "Surprised": (0, 255, 255),  # Yellow
    "Disgusted": (42, 42, 165)   # Brown
}

# ================= FACE DETECTOR =================
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ================= CAMERA =================
cap = cv2.VideoCapture(0)
time.sleep(0.5)
cap.set(cv2.CAP_PROP_FPS, 30)

cv2.namedWindow("Emotion Camera", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Emotion Camera", 600, 450)

start_time = time.time()
final_emotion = "Neutral"
final_confidence = 0.0

# FLAGS
face_detected = False
multiple_faces = False

while time.time() - start_time < 6:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(60, 60)
    )

    if len(faces) > 0:
        face_detected = True
    if len(faces) > 1:
        multiple_faces = True

    # 🟢 MULTI-FACE + COLOR BOXES
    for (x, y, w, h) in faces:
        roi = gray[y:y+h, x:x+w]
        roi = cv2.resize(roi, (48,48))
        roi = roi / 255.0
        roi = roi.reshape(1,48,48,1)

        prediction = model.predict(roi, verbose=0)[0]
        idx = int(np.argmax(prediction))

        emotion = emotion_dict[idx]
        confidence = prediction[idx] * 100

        color = emotion_colors.get(emotion, (0,255,0))
        label = f"{emotion} ({confidence:.1f}%)"

        cv2.rectangle(frame, (x,y), (x+w,y+h), color, 2)
        cv2.putText(
            frame, label, (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.85, color, 2
        )

        final_emotion = emotion
        final_confidence = confidence

    cv2.imshow("Emotion Camera", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

# ================= SAVE RESULT =================
with open("emotion_result.txt", "w") as f:
    if not face_detected:
        f.write("NO_FACE,0")
    elif multiple_faces:
        f.write("MULTIPLE_FACES,0")
    else:
        f.write(f"{final_emotion},{final_confidence:.2f}")
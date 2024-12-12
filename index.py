import cv2
from fer import FER
import time

from utils import translate_emotion
from api import send_emotion_in_thread

emotion_detector = FER()

# Variables for debounce
last_emotion = None
last_emotion_time = 1
debounce_interval = 0.50

# file source (0 for webcam)
file = "C:/Users/Tip/Desktop/Giovani/outros/facial-emotion-detector/files/videos/neutro.mp4"

cap = cv2.VideoCapture(file)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    emotions = emotion_detector.detect_emotions(frame)
    
    for emotion in emotions:
        box = emotion['box']
        emotion_label = max(emotion['emotions'], key=emotion['emotions'].get)

        translated_emotion = translate_emotion(emotion_label)

        current_time = time.time()
        
        if emotion_label != last_emotion or (current_time - last_emotion_time) > debounce_interval:
            send_emotion_in_thread(emotion_label)
            last_emotion = emotion_label
            last_emotion_time = current_time
        
        cv2.rectangle(frame, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), (0, 255, 0), 2)
        cv2.putText(frame, translated_emotion, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow('Emotions', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
import cv2
import mediapipe as mp
import numpy as np
import time

print("🚀 STARTING GESTURE RECOGNITION...")

# MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

# FPS
fps = 0
fps_time = time.time()
frame_count = 0

# Window settings
cv2.namedWindow('GESTURE RECOGNITION', cv2.WINDOW_NORMAL)
cv2.resizeWindow('GESTURE RECOGNITION', 900, 700)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    
    # Interface background
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 80), (25, 25, 25), -1)
    cv2.rectangle(overlay, (0, h-60), (w, h), (25, 25, 25), -1)
    frame = cv2.addWeighted(overlay, 0.3, frame, 0.7, 0)
    
    # FPS calculation
    frame_count += 1
    if time.time() - fps_time >= 1:
        fps = frame_count
        frame_count = 0
        fps_time = time.time()
    
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    
    gesture_text = "WAITING"
    confidence = 0
    color = (100, 100, 100)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks
            mp_drawing.draw_landmarks(
                frame, 
                hand_landmarks, 
                mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0,255,0), thickness=2),
                mp_drawing.DrawingSpec(color=(0,0,255), thickness=2)
            )
            
            # Bounding box coordinates
            x_coords = [lm.x for lm in hand_landmarks.landmark]
            y_coords = [lm.y for lm in hand_landmarks.landmark]
            
            x1 = int(min(x_coords) * w) - 40
            x2 = int(max(x_coords) * w) + 40
            y1 = int(min(y_coords) * h) - 40
            y2 = int(max(y_coords) * h) + 40
            
            # COUNT FINGERS
            tips = [4, 8, 12, 16, 20]
            fingers = []
            
            # Thumb
            if hand_landmarks.landmark[tips[0]].x < hand_landmarks.landmark[tips[0]-1].x:
                fingers.append(1)
            else:
                fingers.append(0)
            
            # Other fingers
            for tip in tips[1:]:
                if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip-2].y:
                    fingers.append(1)
                else:
                    fingers.append(0)
            
            # SPECIAL CHECKS
            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]
            
            # OK gesture - thumb and index finger touch
            distance_ok = abs(thumb_tip.x - index_tip.x) + abs(thumb_tip.y - index_tip.y)
            
            # Thumb down
            thumb_down = (hand_landmarks.landmark[4].y > hand_landmarks.landmark[3].y and 
                        hand_landmarks.landmark[4].y > hand_landmarks.landmark[2].y)
            
            # Victory (classic V)
            victory_classic = (fingers[1] == 1 and fingers[2] == 1 and 
                             fingers[3] == 0 and fingers[4] == 0)
            
            # DETECT GESTURE
            if distance_ok < 0.08 and fingers[1] == 1:
                gesture_text = "👌 OK"
                confidence = 95
                color = (0, 255, 0)
            elif thumb_down and fingers[1] == 0 and fingers[2] == 0:
                gesture_text = "👎 THUMB DOWN"
                confidence = 90
                color = (0, 255, 0)
            elif fingers == [1,0,0,0,0]:
                gesture_text = "👍 THUMB UP"
                confidence = 95
                color = (0, 255, 0)
            elif victory_classic:
                gesture_text = "✌️ VICTORY"
                confidence = 95
                color = (0, 255, 0)
            elif sum(fingers) == 0:
                gesture_text = "👊 FIST"
                confidence = 98
                color = (0, 255, 0)
            elif sum(fingers) == 5:
                gesture_text = "🖐️ PALM"
                confidence = 98
                color = (0, 255, 0)
            else:
                gesture_text = f"🖐️ {sum(fingers)}"
                confidence = 60
                color = (255, 165, 0)
            
            # DRAW BOUNDING BOX
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
            
            # Background for text
            cv2.rectangle(frame, (x1, y1-40), (x2, y1), color, -1)
            
            # Gesture text
            cv2.putText(frame, gesture_text, (x1+10, y1-15), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Confidence
            cv2.putText(frame, f"{confidence}%", (x1+10, y1-70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # === TOP PANEL ===
    cv2.rectangle(frame, (0, 0), (w, 80), (0, 0, 0), -1)
    cv2.rectangle(frame, (0, 0), (w, 80), (0, 255, 0), 2)
    
    # Title
    cv2.putText(frame, "🤖 GESTURE RECOGNITION SYSTEM", (20, 35), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    # FPS
    cv2.putText(frame, f"FPS: {fps}", (w-120, 35), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    # Status
    status = "🟢 ACTIVE" if results.multi_hand_landmarks else "⚫ WAITING"
    cv2.putText(frame, status, (20, 65), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
    
    # === BOTTOM PANEL ===
    cv2.rectangle(frame, (0, h-60), (w, h), (0, 0, 0), -1)
    cv2.rectangle(frame, (0, h-60), (w, h), (0, 255, 0), 1)
    
    # Gesture list
    gestures_list = "👊 FIST  🖐️ PALM  👍 UP  👎 DOWN  👌 OK  ✌️ VICTORY"
    cv2.putText(frame, gestures_list, (20, h-25), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
    
    # Exit
    cv2.putText(frame, "ESC - exit", (w-120, h-25), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 1)
    
    cv2.imshow('GESTURE RECOGNITION', frame)
    
    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()

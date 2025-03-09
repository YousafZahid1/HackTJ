
import cv2
import mediapipe as mp
import pyautogui
import numpy as np
from collections import deque

def eye_tracking(sensitivity=2.0, smoothing_factor=5):
  import cv2
import mediapipe as mp
import pyautogui
import numpy as np
from collections import deque

def eye_tracking(sensitivity=2.0, smoothing_factor=5):
    cam = cv2.VideoCapture(0)
    face_mesh = mp.solutions.face_mesh.FaceMesh(
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    screen_w, screen_h = pyautogui.size()
    pyautogui.moveTo(screen_w // 2, screen_h // 2)
    
    # Smoothing buffer
    position_buffer = deque(maxlen=smoothing_factor)
    
    # Scroll parameters
    SCROLL_THRESHOLD_UP = -0.05
    SCROLL_THRESHOLD_DOWN = 0.05
    SCROLL_AMOUNT = 50
    
    # Dead zone to prevent jitter
    DEAD_ZONE = 0.02
    
    while cam.isOpened():
        success, frame = cam.read()
        if not success:
            break
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape
        
        if landmark_points:
            landmarks = landmark_points[0].landmark
            
            # Use more stable eye center points (left: 468, right: 473)
            left_eye_center = landmarks[468]  # Left eye pupil
            right_eye_center = landmarks[473] # Right eye pupil
            
            # Calculate average eye position
            eye_x = (left_eye_center.x + right_eye_center.x) / 2
            eye_y = (left_eye_center.y + right_eye_center.y) / 2
            
            # Normalize coordinates (0.5 is center)
            norm_x = eye_x - 0.5
            norm_y = eye_y - 0.5
            
            # Apply dead zone
            if abs(norm_x) < DEAD_ZONE:
                norm_x = 0
            if abs(norm_y) < DEAD_ZONE:
                norm_y = 0
            
            # Calculate screen position with sensitivity
            target_x = screen_w // 2 + norm_x * screen_w * sensitivity
            target_y = screen_h // 2 + norm_y * screen_h * sensitivity
            
            # Smooth the movement
            position_buffer.append((target_x, target_y))
            avg_x = np.mean([pos[0] for pos in position_buffer])
            avg_y = np.mean([pos[1] for pos in position_buffer])
            
            # Keep cursor within screen bounds
            avg_x = np.clip(avg_x, 0, screen_w)
            avg_y = np.clip(avg_y, 0, screen_h)
            
            pyautogui.moveTo(avg_x, avg_y)
            
            # Visualize eye centers
            for landmark in [left_eye_center, right_eye_center]:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 0))
            
            # Click detection using eye outer corners
            left_eye = [landmarks[145], landmarks[159]]
            right_eye = [landmarks[374], landmarks[386]]
            for landmark in left_eye + right_eye:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 255))
            
            left_eye_ratio = left_eye[0].y - left_eye[1].y
            right_eye_ratio = right_eye[0].y - right_eye[1].y
            if left_eye_ratio < 0.015 and right_eye_ratio > 0.015:
                pyautogui.click()
                pyautogui.sleep(1)
            
            # Scroll detection
            nose_y = landmarks[1].y
            avg_eye_y = (left_eye[0].y + left_eye[1].y + 
                        right_eye[0].y + right_eye[1].y) / 4
            eye_relative_pos = avg_eye_y - nose_y
            
            if eye_relative_pos < SCROLL_THRESHOLD_UP:
                pyautogui.scroll(SCROLL_AMOUNT)
            elif eye_relative_pos > SCROLL_THRESHOLD_DOWN:
                pyautogui.scroll(-SCROLL_AMOUNT)
                
        frame_queue.put(frame)
    cam.release()

# Make sure to define frame_queue somewhere in your main code
# Example usage:
# import queue
# frame_queue = queue.Queue()
# eye_tracking()

# Make sure to define frame_queue somewhere in your main code
# Example usage:
# import queue
# frame_queue = queue.Queue()
# eye_tracking()

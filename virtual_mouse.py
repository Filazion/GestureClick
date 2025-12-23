# import mediapipe as mp
# import cv2
# import pyautogui
# import numpy as np
# from mediapipe.tasks import python
# from mediapipe.tasks.python import vision
# from mediapipe.framework.formats import landmark_pb2

# # --- 1. CONFIGURATION ---

# # Model and Task Setup
# MODEL_PATH = './model/hand_landmarker.task' 
# if MODEL_PATH == './model/hand_landmarker.task':
#     print("WARNING: Ensure the 'hand_landmarker.task' file is in the same directory.")
    
# BaseOptions = mp.tasks.BaseOptions
# HandLandmarker = vision.HandLandmarker
# HandLandmarkerOptions = vision.HandLandmarkerOptions
# VisionRunningMode = vision.RunningMode
# mp_drawing = mp.solutions.drawing_utils
# mp_hands = mp.solutions.hands

# # PyAutoGUI Setup
# pyautogui.FAILSAFE = False # Disable the safety feature that stops the script when mouse hits a corner
# SCREEN_W, SCREEN_H = pyautogui.size()

# # Parameters for smoothing and sensitivity
# SMOOTHING_FACTOR = 0.4 # Lower value means more smoothing (less jitter)
# CLICK_THRESHOLD = 0.05 # Distance threshold for the pinch gesture (Normalized 0.0 to 1.0)
# FRAME_W, FRAME_H = 640, 480 # Webcam resolution

# # Variables for smoothing cursor movement
# prev_x, prev_y = SCREEN_W // 2, SCREEN_H // 2
# is_clicking = False # State flag to prevent multiple rapid clicks

# # Hand Landmarker Landmarks (Indices)
# INDEX_FINGER_TIP = 8
# THUMB_TIP = 4

# # --- 2. HELPER FUNCTIONS ---

# def calculate_distance(landmark1, landmark2):
#     """Calculates the Euclidean distance between two MediaPipe NormalizedLandmark objects."""
#     return np.sqrt((landmark1.x - landmark2.x)**2 + 
#                    (landmark1.y - landmark2.y)**2 + 
#                    (landmark1.z - landmark2.z)**2)

# def process_and_control_mouse(frame, hand_landmarks):
#     """
#     Analyzes hand landmarks and controls the mouse using PyAutoGUI.
    
#     Args:
#         frame: The current OpenCV video frame.
#         hand_landmarks: A list of 21 NormalizedLandmarks for the detected hand.
#     """
#     global prev_x, prev_y, is_clicking
    
#     # 2.1. Cursor Movement: Use the Index Finger Tip (Landmark 8)
#     index_tip = hand_landmarks[INDEX_FINGER_TIP]
    
#     # Scale normalized coordinates (0 to 1) to screen coordinates (0 to SCREEN_W/H)
#     # The frame is flipped, so we use 1 - x to ensure movement is intuitive (left on screen = left in camera)
#     target_x = (1 - index_tip.x) * SCREEN_W
#     target_y = index_tip.y * SCREEN_H

#     # Apply smoothing (Linear Interpolation / Lerp)
#     smooth_x = prev_x + (target_x - prev_x) * SMOOTHING_FACTOR
#     smooth_y = prev_y + (target_y - prev_y) * SMOOTHING_FACTOR
    
#     # Move the mouse
#     pyautogui.moveTo(smooth_x, smooth_y)
    
#     # Update previous position for the next frame's smoothing
#     prev_x, prev_y = smooth_x, smooth_y
    
#     # 2.2. Click Detection: Use the distance between Index Tip (8) and Thumb Tip (4)
#     thumb_tip = hand_landmarks[THUMB_TIP]
#     distance = calculate_distance(index_tip, thumb_tip)
    
#     # Draw a circle on the cursor point
#     cv2.circle(frame, (int((1 - index_tip.x) * FRAME_W), int(index_tip.y * FRAME_H)), 10, (255, 0, 0), cv2.FILLED)
    
#     gesture_text = f"Distance: {distance:.2f}"
    
#     if distance < CLICK_THRESHOLD:
#         gesture_text = "CLICK: PINCH!"
        
#         # Check if a click is NOT already in progress (state management)
#         if not is_clicking:
#             pyautogui.click()
#             is_clicking = True
            
#         cv2.circle(frame, (int((1 - index_tip.x) * FRAME_W), int(index_tip.y * FRAME_H)), 15, (0, 0, 255), cv2.FILLED)
#     else:
#         # Reset the clicking state when fingers move apart
#         is_clicking = False
        
#     return frame, gesture_text


# # --- 3. MAIN LOOP ---
# def main():
#     cap = cv2.VideoCapture(0)
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_W)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_H)
    
#     if not cap.isOpened():
#         print("Error: Could not open webcam.")
#         return

#     # Create the Hand Landmarker Options
#     options = HandLandmarkerOptions(
#         base_options=BaseOptions(model_asset_path=MODEL_PATH),
#         running_mode=VisionRunningMode.VIDEO, # Using VIDEO mode for synchronous processing
#         num_hands=1 # We only care about one hand for cursor control
#     )

#     # Initialize the Landmarker
#     with HandLandmarker.create_from_options(options) as landmarker:
        
#         # Get frame timestamp for VIDEO mode
#         frame_timestamp_ms = 0

#         while cap.isOpened():
#             success, frame = cap.read()
#             if not success:
#                 break
            
#             # Flip the frame horizontally for natural movement
#             frame = cv2.flip(frame, 1)
#             frame_timestamp_ms += 33 # Approximate frame time for 30 FPS
            
#             # Convert BGR to RGB
#             rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            
#             # Synchronously process the frame
#             landmarker_result = landmarker.detect_for_video(mp_image, frame_timestamp_ms)
            
#             # --- Draw and Control ---
#             gesture_info = "Waiting for hand..."
#             if landmarker_result.hand_landmarks:
#                 # Assuming we only process the first detected hand
#                 hand_landmarks = landmarker_result.hand_landmarks[0] 

#                 # Convert Tasks landmarks → Drawing-compatible format
#                 hand_landmark_list = landmark_pb2.NormalizedLandmarkList(
#                     landmark=hand_landmarks
#                 )
                
#                 # Control the mouse
#                 frame, gesture_info = process_and_control_mouse(frame, hand_landmarks)
                
#                 # Draw the landmarks on the video feed
#                 mp_drawing.draw_landmarks(
#                     frame,
#                     hand_landmark_list,
#                     #hand_landmarks,
#                     mp_hands.HAND_CONNECTIONS,
#                     mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=3),
#                     mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2),
#                 )

#             # Display gesture info on screen
#             cv2.putText(frame, gesture_info, (10, 30), 
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
            
#             # --- Display the final frame ---
#             cv2.imshow('Virtual Mouse Control (Press Q to Exit)', frame)
            
#             if cv2.waitKey(5) & 0xFF == ord('q'):
#                 break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == '__main__':
#     main()



import cv2
import numpy as np
import pyautogui
import mediapipe as mp
from mediapipe.tasks.python import vision

# ---------------- CONFIG ----------------

MODEL_PATH = "./model/hand_landmarker.task"

pyautogui.FAILSAFE = False
SCREEN_W, SCREEN_H = pyautogui.size()

FRAME_W, FRAME_H = 640, 480
SMOOTHING = 0.35

PINCH_LEFT = 0.045
PINCH_RIGHT = 0.045
FIST_THRESHOLD = 0.18
SCROLL_SENSITIVITY = 40

# Landmarks
THUMB_TIP = 4
INDEX_TIP = 8
MIDDLE_TIP = 12
RING_TIP = 16
PINKY_TIP = 20
WRIST = 0

# State
prev_x, prev_y = SCREEN_W // 2, SCREEN_H // 2
left_down = False
dragging = False

# ---------------- HELPERS ----------------

def dist(a, b):
    return np.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2)

def lerp(a, b, t):
    return a + (b - a) * t

def is_fist(lm):
    wrist = lm[WRIST]
    tips = [INDEX_TIP, MIDDLE_TIP, RING_TIP, PINKY_TIP]
    return all(dist(lm[t], wrist) < FIST_THRESHOLD for t in tips)

# ---------------- MAIN ----------------

def main():
    global prev_x, prev_y, left_down, dragging
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_W)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_H)

    options = vision.HandLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=vision.RunningMode.VIDEO,
        num_hands=1
    )

    with vision.HandLandmarker.create_from_options(options) as landmarker:
        timestamp = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

            timestamp += 33
            result = landmarker.detect_for_video(mp_img, timestamp)

            if result.hand_landmarks:
                lm = result.hand_landmarks[0]

                # ---------- CURSOR MOVE ----------
                ix, iy = (1 - lm[INDEX_TIP].x) * SCREEN_W, lm[INDEX_TIP].y * SCREEN_H
                sx = lerp(prev_x, ix, SMOOTHING)
                sy = lerp(prev_y, iy, SMOOTHING)
                pyautogui.moveTo(sx, sy)
                prev_x, prev_y = sx, sy

                # ---------- PINCHES ----------
                left_pinch = dist(lm[THUMB_TIP], lm[INDEX_TIP]) < PINCH_LEFT
                right_pinch = dist(lm[THUMB_TIP], lm[MIDDLE_TIP]) < PINCH_RIGHT

                # ---------- DRAG ----------
                if is_fist(lm):
                    if not dragging:
                        pyautogui.mouseDown()
                        dragging = True
                else:
                    if dragging:
                        pyautogui.mouseUp()
                        dragging = False

                # ---------- LEFT CLICK ----------
                if left_pinch and not left_down and not dragging:
                    pyautogui.click()
                    left_down = True
                if not left_pinch:
                    left_down = False

                # ---------- RIGHT CLICK ----------
                if right_pinch and not dragging:
                    pyautogui.rightClick()

                # ---------- SCROLL ----------
                index_up = lm[INDEX_TIP].y < lm[MIDDLE_TIP].y
                if index_up and not dragging:
                    scroll_amount = int((lm[MIDDLE_TIP].y - lm[INDEX_TIP].y) * SCROLL_SENSITIVITY)
                    pyautogui.scroll(scroll_amount)

            cv2.imshow("Virtual Mouse (Q to quit)", frame)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

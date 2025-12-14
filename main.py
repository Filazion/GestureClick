# # import mediapipe as mp
# # import cv2
# # import time
# # import numpy as np
# # from mediapipe.tasks import python
# # from mediapipe.tasks.python import vision

# # # --- 1. CONFIGURATION ---

# # # Path to the downloaded model
# # MODEL_PATH = './model/gesture_recognizer.task' 
# # # if MODEL_PATH == './model/gesture_recognizer.task':
# # #     print("WARNING: Ensure the 'gesture_recognizer.task' file is in the same directory.")
    
# # # MediaPipe Task API setup
# # BaseOptions = mp.tasks.BaseOptions
# # GestureRecognizer = vision.GestureRecognizer
# # GestureRecognizerOptions = vision.GestureRecognizerOptions
# # VisionRunningMode = vision.RunningMode

# # # Drawing utilities for visualization
# # mp_drawing = mp.solutions.drawing_utils
# # mp_hands = mp.solutions.hands

# # # A list to store results asynchronously
# # recognition_results = []
    
# # # --- 2. CALLBACK FUNCTION FOR ASYNCHRONOUS RESULTS ---
# # def print_result(result: vision.GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
# #     """
# #     This function is called by the Gesture Recognizer whenever a frame is processed.
# #     It stores the latest result for the main loop to draw.
# #     """
# #     global recognition_results
# #     recognition_results.clear()
# #     recognition_results.append(result)

# # # --- 3. DRAWING FUNCTION ---
# # def visualize_results(frame, results: vision.GestureRecognizerResult):
# #     """
# #     Draws the hand landmarks and the recognized gesture text on the OpenCV frame.
# #     """
    
# #     # Check if any hands were detected
# #     if not results.handedness:
# #         return frame, ""

# #     for hand_idx, hand_landmarks in enumerate(results.hand_landmarks):
        
# #         # 3.1. Draw the landmarks and connections
# #         # 
# #         mp_drawing.draw_landmarks(
# #             frame,
# #             hand_landmarks,
# #             mp_hands.HAND_CONNECTIONS,
# #             mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2), # Red dots
# #             mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2), # Green lines
# #         )
        
# #         # 3.2. Get the recognized gesture
# #         if results.gesture_names and hand_idx < len(results.gesture_names):
# #             gesture = results.gesture_names[hand_idx][0] # The name is the first element of the first category
# #         else:
# #             gesture = "N/A"

# #         # 3.3. Get wrist coordinates (approximate bottom center of the hand)
# #         # Assuming the wrist (landmark 0) is the base point
# #         x_min = min([landmark.x for landmark in hand_landmarks])
# #         y_max = max([landmark.y for landmark in hand_landmarks])
        
# #         frame_h, frame_w, _ = frame.shape
# #         x_pixel = int(x_min * frame_w)
# #         y_pixel = int(y_max * frame_h) + 30 # Place text slightly below the hand
        
# #         # 3.4. Display the gesture text
# #         text_to_display = f"Gesture: {gesture}"
# #         cv2.putText(
# #             frame, 
# #             text_to_display, 
# #             (x_pixel, y_pixel), 
# #             cv2.FONT_HERSHEY_SIMPLEX, 
# #             0.7, 
# #             (255, 255, 255), # White text
# #             2, 
# #             cv2.LINE_AA
# #         )
        
# #         return frame, gesture


# # # --- 4. MAIN LOOP ---
# # def main():
# #     cap = cv2.VideoCapture(0)
# #     if not cap.isOpened():
# #         print("Error: Could not open webcam.")
# #         return

# #     # Create the Gesture Recognizer Options
# #     options = GestureRecognizerOptions(
# #         base_options=BaseOptions(model_asset_path=MODEL_PATH),
# #         running_mode=VisionRunningMode.LIVE_STREAM,
# #         result_callback=print_result # Use the asynchronous callback
# #     )

# #     # Initialize the Recognizer
# #     with GestureRecognizer.create_from_options(options) as recognizer:
        
# #         start_time = time.time()
# #         frame_count = 0

# #         while cap.isOpened():
# #             success, frame = cap.read()
# #             if not success:
# #                 break
            
# #             # Flip the frame horizontally for a more natural view
# #             frame = cv2.flip(frame, 1)

# #             # Convert BGR to RGB (required by MediaPipe)
# #             rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
# #             # Convert NumPy array to MediaPipe Image
# #             # Note: The timestamp must be monotonically increasing for LIVE_STREAM mode
# #             timestamp_ms = int(cv2.getTickCount() / cv2.getTickFrequency() * 1000)
# #             mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            
# #             # Run recognition asynchronously
# #             recognizer.recognize_async(mp_image, timestamp_ms)
            
# #             # --- Draw results from the last callback ---
# #             if recognition_results:
# #                 frame, gesture = visualize_results(frame, recognition_results[0])

# #             # --- Calculate and Display FPS ---
# #             frame_count += 1
# #             if frame_count % 10 == 0:
# #                 end_time = time.time()
# #                 fps = frame_count / (end_time - start_time)
# #                 cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), 
# #                             cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)
            
# #             # --- Display the final frame ---
# #             cv2.imshow('Real-Time MediaPipe Hand Gesture Tracking (Press Q to Exit)', frame)
            
# #             if cv2.waitKey(5) & 0xFF == ord('q'):
# #                 break

# #     cap.release()
# #     cv2.destroyAllWindows()

# # if __name__ == '__main__':
# #     main()

# import mediapipe as mp
# import cv2
# import time
# import numpy as np
# from mediapipe.tasks import python
# from mediapipe.tasks.python import vision
# from mediapipe.framework.formats import landmark_pb2

# # --- 1. CONFIGURATION ---
# MODEL_PATH = './model/gesture_recognizer.task' 

# # MediaPipe Task API setup
# BaseOptions = mp.tasks.BaseOptions
# GestureRecognizer = vision.GestureRecognizer
# GestureRecognizerOptions = vision.GestureRecognizerOptions
# VisionRunningMode = vision.RunningMode

# # Drawing utilities for visualization
# mp_drawing = mp.solutions.drawing_utils
# mp_hands = mp.solutions.hands

# # A list to store results asynchronously
# recognition_results = []

# # --- 2. CALLBACK FUNCTION FOR ASYNCHRONOUS RESULTS ---
# def print_result(result: vision.GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
#     """
#     This function is called by the Gesture Recognizer whenever a frame is processed.
#     It stores the latest result for the main loop to draw.
#     """
#     global recognition_results
#     recognition_results.clear()
#     recognition_results.append(result)

# # --- 3. DRAWING FUNCTION ---
# def visualize_results(frame, results: vision.GestureRecognizerResult):
#     """
#     Draws the hand landmarks and the recognized gesture text on the OpenCV frame.
#     """
#     if not results.hand_landmarks:  # Check if hand_landmarks is empty
#         return frame, ""

#     for hand_idx, hand_landmarks in enumerate(results.hand_landmarks):
        
#         # Convert the landmarks list into a NormalizedLandmarkList
#         landmark_list = landmark_pb2.NormalizedLandmarkList(
#             landmark=[
#                 landmark_pb2.NormalizedLandmark(x=lm.x, y=lm.y, z=lm.z) for lm in hand_landmarks
#             ]
#         )
        
#         # 3.1. Draw the landmarks and connections
#         mp_drawing.draw_landmarks(
#             frame,
#             landmark_list,
#             mp_hands.HAND_CONNECTIONS,
#             mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2), # Red dots
#             mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2), # Green lines
#         )
        
#         # 3.2. Get the recognized gesture
#         if results.gesture_names and hand_idx < len(results.gesture_names):
#             gesture = results.gesture_names[hand_idx][0] # The name is the first element of the first category
#         else:
#             gesture = "N/A"

#         # 3.3. Get wrist coordinates (approximate bottom center of the hand)
#         x_min = min([landmark.x for landmark in hand_landmarks])
#         y_max = max([landmark.y for landmark in hand_landmarks])
        
#         frame_h, frame_w, _ = frame.shape
#         x_pixel = int(x_min * frame_w)
#         y_pixel = int(y_max * frame_h) + 30  # Place text slightly below the hand
        
#         # 3.4. Display the gesture text
#         text_to_display = f"Gesture: {gesture}"
#         cv2.putText(
#             frame, 
#             text_to_display, 
#             (x_pixel, y_pixel), 
#             cv2.FONT_HERSHEY_SIMPLEX, 
#             0.7, 
#             (255, 255, 255), # White text
#             2, 
#             cv2.LINE_AA
#         )
        
#         return frame, gesture


# # --- 4. MAIN LOOP ---
# def main():
#     cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         print("Error: Could not open webcam.")
#         return

#     # Create the Gesture Recognizer Options
#     options = GestureRecognizerOptions(
#         base_options=BaseOptions(model_asset_path=MODEL_PATH),
#         running_mode=VisionRunningMode.LIVE_STREAM,
#         result_callback=print_result  # Use the asynchronous callback
#     )

#     # Initialize the Recognizer
#     with GestureRecognizer.create_from_options(options) as recognizer:
        
#         start_time = time.time()
#         frame_count = 0

#         while cap.isOpened():
#             success, frame = cap.read()
#             if not success:
#                 break
            
#             # Flip the frame horizontally for a more natural view
#             frame = cv2.flip(frame, 1)

#             # Convert BGR to RGB (required by MediaPipe)
#             rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
#             # Convert NumPy array to MediaPipe Image
#             timestamp_ms = int(cv2.getTickCount() / cv2.getTickFrequency() * 1000)
#             mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            
#             # Run recognition asynchronously
#             recognizer.recognize_async(mp_image, timestamp_ms)
            
#             # --- Draw results from the last callback ---
#             if recognition_results:
#                 frame, gesture = visualize_results(frame, recognition_results[0])

#             # --- Calculate and Display FPS ---
#             frame_count += 1
#             if frame_count % 10 == 0:
#                 end_time = time.time()
#                 fps = frame_count / (end_time - start_time)
#                 cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), 
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)
            
#             # --- Display the final frame ---
#             cv2.imshow('Real-Time MediaPipe Hand Gesture Tracking (Press Q to Exit)', frame)
            
#             if cv2.waitKey(5) & 0xFF == ord('q'):
#                 break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == '__main__':
#     main()


import mediapipe as mp
import cv2
import time
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2

# --- 1. CONFIGURATION ---
MODEL_PATH = './model/gesture_recognizer.task' 

# MediaPipe Task API setup
BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = vision.GestureRecognizer
GestureRecognizerOptions = vision.GestureRecognizerOptions
VisionRunningMode = vision.RunningMode

# Drawing utilities for visualization
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# A list to store results asynchronously
recognition_results = []

# --- 2. CALLBACK FUNCTION FOR ASYNCHRONOUS RESULTS ---
def print_result(result: vision.GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    """
    This function is called by the Gesture Recognizer whenever a frame is processed.
    It stores the latest result for the main loop to draw.
    """
    global recognition_results
    recognition_results.clear()
    recognition_results.append(result)

# --- 3. DRAWING FUNCTION ---
def visualize_results(frame, results: vision.GestureRecognizerResult):
    """
    Draws the hand landmarks and the recognized gesture text on the OpenCV frame.
    """
    if not results.hand_landmarks:  # Check if hand_landmarks is empty
        return frame, ""

    for hand_idx, hand_landmarks in enumerate(results.hand_landmarks):
        
        # Convert the landmarks list into a NormalizedLandmarkList
        landmark_list = landmark_pb2.NormalizedLandmarkList(
            landmark=[
                landmark_pb2.NormalizedLandmark(x=lm.x, y=lm.y, z=lm.z) for lm in hand_landmarks
            ]
        )
        
        # 3.1. Draw the landmarks and connections
        mp_drawing.draw_landmarks(
            frame,
            landmark_list,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2), # Red dots
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2), # Green lines
        )
        
        # 3.2. Get the recognized gesture
        gesture = "N/A"
        if results.gestures:
            # Ensure we're getting the right gesture category for the current hand
            gesture = results.gestures[hand_idx][0].category_name if hand_idx < len(results.gestures) else "N/A"

        # 3.3. Get wrist coordinates (approximate bottom center of the hand)
        x_min = min([landmark.x for landmark in hand_landmarks])
        y_max = max([landmark.y for landmark in hand_landmarks])
        
        frame_h, frame_w, _ = frame.shape
        x_pixel = int(x_min * frame_w)
        y_pixel = int(y_max * frame_h) + 30  # Place text slightly below the hand
        
        # 3.4. Display the gesture text
        text_to_display = f"Gesture: {gesture}"
        cv2.putText(
            frame, 
            text_to_display, 
            (x_pixel, y_pixel), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.7, 
            (255, 255, 255), # White text
            2, 
            cv2.LINE_AA
        )
        
        return frame, gesture


# --- 4. MAIN LOOP ---
def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Create the Gesture Recognizer Options
    options = GestureRecognizerOptions(
        base_options=BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=print_result  # Use the asynchronous callback
    )

    # Initialize the Recognizer
    with GestureRecognizer.create_from_options(options) as recognizer:
        
        start_time = time.time()
        frame_count = 0

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break
            
            # Flip the frame horizontally for a more natural view
            frame = cv2.flip(frame, 1)

            # Convert BGR to RGB (required by MediaPipe)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert NumPy array to MediaPipe Image
            timestamp_ms = int(cv2.getTickCount() / cv2.getTickFrequency() * 1000)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            
            # Run recognition asynchronously
            recognizer.recognize_async(mp_image, timestamp_ms)
            
            # --- Draw results from the last callback ---
            if recognition_results:
                frame, gesture = visualize_results(frame, recognition_results[0])

            # --- Calculate and Display FPS ---
            frame_count += 1
            if frame_count % 10 == 0:
                end_time = time.time()
                fps = frame_count / (end_time - start_time)
                cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)
            
            # --- Display the final frame ---
            cv2.imshow('Real-Time MediaPipe Hand Gesture Tracking (Press Q to Exit)', frame)
            
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

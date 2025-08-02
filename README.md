# Gesture-recognition
 This project demonstrates a real-time hand gesture recognition system using only OpenCV and basic mathematical geometry. The application identifies the number of fingers shown in front of a webcam and maps each gesture to a specific command like "START", "STOP", or "NEXT", etc. It works without using any deep learning or third-party hand-tracking frameworks like Mediapipe.
 
# Features
Detects fingers shown in a live webcam feed.
Counts 0 to 5 fingers accurately using convexity defect analysis.
Maps finger count to predefined gestures (e.g., 0 → START, 5 → STOP).
Works in real-time with a skin color segmentation-based method.
Runs with OpenCV only, compatible with Python 3.13.

# Project Objective
To develop a lightweight, real-time gesture recognition tool using basic image processing techniques — ideal for systems where installation of large ML models or external dependencies is not feasible.

# How It Works
1. Video Capture and Region of Interest (ROI)
The webcam feed is accessed using OpenCV’s VideoCapture.

A fixed ROI (Region of Interest) is defined on the screen (a box from (100, 100) to (400, 400)), where the user is expected to show their hand.

2. Skin Color Detection
The ROI is converted to HSV color space.

A skin color mask is created using predefined HSV thresholds.

The mask is blurred slightly to reduce noise and smoothen the hand outline.

3. Contour Detection
Contours are extracted from the skin mask.

The largest contour, assumed to be the hand, is identified and processed.

If the area of this contour is greater than a certain threshold (5000), it is considered valid.

4. Finger Counting using Convexity Defects
The convex hull of the hand contour is computed.

Using the hull, convexity defects (dips between fingers) are found.

For each defect, the angle between the fingertips and the farthest point is calculated using the cosine rule.

If the angle is less than 90 degrees and the depth of the defect is significant, it's counted as a finger gap.

The number of fingers is estimated as defect_count + 1.

5. Gesture Mapping
The finger count is mapped to a predefined dictionary:
gesture_actions = {
    0: "START",
    1: "YES",
    2: "OK",
    3: "NEXT",
    4: "BACK",
    5: "STOP"
}
This label is displayed on the webcam feed using cv2.putText().

6. Exit Mechanism
The user can press the 'e' key to exit the program safely.

# Dependencies
Python 3.13+
OpenCV (install with pip install opencv-python)

# How to Run
 1. Install Python 3.13+ and OpenCV:
     pip install opencv-python
 2.Run the script:
     python gesture_recognition.py
 3.Show your hand inside the green rectangle and perform gestures (0 to 5 fingers).
 4.Press 'e' to exit the application.

# Sample Output
 0 Fingers → START
 2 Fingers → OK
 5 Fingers → STOP
<img width="826" height="722" alt="Screenshot 2025-08-02 194102" src="https://github.com/user-attachments/assets/e9caf9aa-585a-4ea1-b53b-4d9ef730beef" />
<img width="813" height="628" alt="Screenshot 2025-08-02 194134" src="https://github.com/user-attachments/assets/a5b6ccdc-5bd7-476c-919f-902b901e1898" />
<img width="806" height="619" alt="Screenshot 2025-08-02 194148" src="https://github.com/user-attachments/assets/93a0c6c5-d07b-46f3-b48f-8dcbbb82b6df" />




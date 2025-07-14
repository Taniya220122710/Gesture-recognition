import cv2
import numpy as np
import math

# finger counting based on convexity defects
#using opencv without mediapipe
gesture_actions = {
    0: "START",
    1: "YES",
    2: "OK",
    3: "NEXT",
    4: "BACK",
    5: "STOP"
}

def count_fingers(contour, drawing):
    hull = cv2.convexHull(contour, returnPoints=False)
    if hull is None or len(hull) < 3:
        return 0

    defects = cv2.convexityDefects(contour, hull)
    if defects is None:
        return 0

    count = 0
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(contour[s][0])
        end = tuple(contour[e][0])
        far = tuple(contour[f][0])

        x = math.dist(start, end)
        y = math.dist(start, far)
        z = math.dist(end, far)

        angle = math.acos((y**2 + z**2 - x**2) / (2*y*z + 1e-5)) * 180 / math.pi

        if angle < 90 and d > 10000:
            count += 1
            cv2.circle(drawing, far, 8, (0, 0, 255), -1)

    return count + 1 if count > 0 else 0

cap = cv2.VideoCapture(0)
print("Press 'e' to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    roi = frame[100:400, 100:400]
    cv2.rectangle(frame, (100, 100), (400, 400), (0, 255, 0), 2)

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    lower_skin = np.array([0, 20, 70])
    upper_skin = np.array([20, 255, 255])
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    mask = cv2.GaussianBlur(mask, (5, 5), 0)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    drawing = roi.copy()

    if contours:
        largest = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest) > 5000:
            cv2.drawContours(drawing, [largest], -1, (255, 255, 0), 2)
            fingers = count_fingers(largest, drawing)

            # Cap the count to max 5
            fingers = min(fingers, 5)
            message = gesture_actions.get(fingers, "UNKNOWN")

            output_text = f"{fingers} Finger{'s' if fingers != 1 else ''}: {message}"
            cv2.putText(frame, output_text, (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)

    frame[100:400, 100:400] = drawing
    cv2.imshow("Gesture Recognition - Python 3.13 (No Mediapipe)", frame)

    if cv2.waitKey(1) & 0xFF == ord('e'):
        break

cap.release()
cv2.destroyAllWindows()

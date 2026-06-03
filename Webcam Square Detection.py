import cv2
import numpy as np

cap = cv2.VideoCapture(0)

def get_snapshot():
    ok, frame = cap.read()

    if not ok or frame is None:
        print("Camera read failed.")
        return None
    
    frame = cv2.resize(frame, (640, 480))

    return frame

def detect(frame):
    count = 0
    
    lower = np.array([0, 50, 50])
    upper = np.array([179, 255, 255])

    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    mask = cv2.inRange(hsv, lower, upper)

    open_kernel = np.ones((3, 3), np.uint8)

    opened_mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        open_kernel,
        iterations = 1
    )

    contours, _ = cv2.findContours(
        opened_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area < 100:
            continue
    
        perimeter = cv2.arcLength(cnt, True)

        if perimeter == 0:
            continue

        approx = cv2.approxPolyDP(cnt, 0.04 * perimeter, True)

        if len(approx) != 4:
            continue

        if not cv2.isContourConvex(approx):
            continue

        rect = cv2.minAreaRect(cnt)
        (cx, cy), (w, h), angle = rect

        if w == 0 or h == 0:
            continue
    
        aspect_ratio = max(w, h) / min (w, h)

        if aspect_ratio > 1.25:
            continue

        box_area = w * h
        extent = area / box_area

        if extent < 0.45:
            continue

        box = cv2.boxPoints(rect)
        box = np.int32(box)

        count += 1

        cv2.drawContours(frame, [box], 0, (255, 255, 255), 3)
    cv2.putText(frame, "Square Count: "+str(count), (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    return frame

while True:
    frame = get_snapshot()
    if frame is None:
        break
    
    cv2.imshow("Webcam", detect(frame))

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
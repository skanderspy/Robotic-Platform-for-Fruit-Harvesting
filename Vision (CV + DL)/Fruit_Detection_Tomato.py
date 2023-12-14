from ultralytics import YOLO
import cv2
import math
import numpy as np

# Start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Model
model = YOLO("tomato.pt")

# Object classes
classNames = ['ripe tomato', 'unripe tomato']

# Camera calibration parameters (You need to adjust these based on your camera calibration)
focal_length = 1300  # Focal length of your camera in pixels
known_object_width = 7.5  # Width of the object you want to measure (in centimeters)

while True:
    success, img = cap.read()
    results = model(img, stream=True)

    _,white_frame= cap.read()
    white_frame = cv2.resize(white_frame,(640,480))
    white_hsv = cv2.cvtColor(white_frame, cv2.COLOR_BGR2HSV)
    
    results = model(white_frame, stream=True)

    # Coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # Bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            # Calculate the center of the bounding box (x, y)
            x_center = (x1 + x2) / 2
            y_center = (y1 + y2) / 2

            print(f"Tomato coordinates: ({x_center}, {y_center})")

            # Confidence
            confidence = math.ceil((box.conf[0] * 100)) / 100

            # Class name
            cls = int(box.cls[0])

            # Calculate object distance
            object_width_pixels = x2 - x1
            object_distance_cm = ((known_object_width * focal_length) / object_width_pixels) - 35

            # Masking
            lower_white = np.array([0,0,87])
            upper_white = np.array([179,52,255])

            white_mask = cv2.inRange(white_hsv, lower_white, upper_white)            
            white_res = cv2.bitwise_and(white_frame,white_frame, mask= white_mask)
            
            # Find the contours of base
            white_contours, white_hierarchy = cv2.findContours(white_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            
            for white_c in white_contours:
                
                white_area = cv2.contourArea(white_c)  ### Get area of the contour detected
                
                if white_area>50000:          ## Setting the threshold for base area                      
                    cv2.drawContours(white_frame, white_c, -1, (0, 255, 0), 5)  ## Draw contours of base 


            # Object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
            cv2.putText(img, f"Confidence: {confidence}", (x1, y1 - 30), font, 0.5, color, thickness)
            cv2.putText(img, f"Distance: {object_distance_cm:.2f} cm", (x1, y1 - 60), font, 0.5, color, thickness)
            cv2.putText(img, f"Tomato coordinates: ({x_center}, {y_center})", (x1, y1 - 90), font, 0.5, color, thickness)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

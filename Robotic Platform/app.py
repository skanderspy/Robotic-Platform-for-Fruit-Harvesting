from flask import Flask, request, render_template, Response
from ultralytics import YOLO
import cv2
import math
import RPi.GPIO as GPIO
import serial
import threading

app = Flask(__name__)

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

# Servo motor setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
pwm=GPIO.PWM(12, 50)
pwm.start(0)

# Serial communication setup
ser = serial.Serial('/dev/ttyACM0', 9600)

def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(12, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(12, False)
    pwm.ChangeDutyCycle(0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(run_detection(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/move', methods=['POST'])
def move():
    direction = request.form.get('direction')
    ser.write(direction.encode())
    return '', 204

@app.route('/stop', methods=['POST'])
def stop():
    ser.write('x'.encode())
    return '', 204

def run_detection():
    while True:
        success, img = cap.read()
        results = model(img, stream=True)

        # Coordinates
        for r in results:
            boxes = r.boxes

            for box in boxes:
                # Bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                # Confidence
                confidence = math.ceil((box.conf[0] * 100)) / 100

                # Class name
                cls = int(box.cls[0])

                # Calculate object distance
                object_width_pixels = x2 - x1
                object_distance_cm = (known_object_width * focal_length) / object_width_pixels

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

                if confidence > 0.96:
                    SetAngle(90) # Rotate servo motor to grab the tomato

        ret, jpeg = cv2.imencode('.jpg', img)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

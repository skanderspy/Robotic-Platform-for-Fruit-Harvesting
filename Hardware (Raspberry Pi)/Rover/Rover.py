from flask import Flask, render_template, request
import RPi.GPIO as GPIO

app = Flask(__name__)

# Define the motor GPIO pins
motor_pins = {'motor1': [2, 3], 'motor2': [4, 5], 'motor3': [6, 7], 'motor4': [8, 9]}

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Setup the motor GPIO pins
for pins in motor_pins.values():
    GPIO.setup(pins[0], GPIO.OUT)
    GPIO.setup(pins[1], GPIO.OUT)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    command = request.form['command']
    if command == 'w':
        # Move forward
        for pins in motor_pins.values():
            GPIO.output(pins[0], GPIO.HIGH)
            GPIO.output(pins[1], GPIO.LOW)
    elif command == 's':
        # Move backward
        for pins in motor_pins.values():
            GPIO.output(pins[0], GPIO.LOW)
            GPIO.output(pins[1], GPIO.HIGH)
    elif command == 'a':
        # Move left
        # Add your logic here
        pass
    elif command == 'd':
        # Move right
        # Add your logic here
        pass
    else:
        print("Unknown command")
    return '', 204

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=80, debug=True)
    finally:
        # Cleanup the GPIO on exit
        GPIO.cleanup()

from flask import Flask, request, jsonify
import RPi.GPIO as GPIO
import time

# Define the servo GPIO pins
servo_pins = {'arm': 2, 'shoulder': 3, 'elbow': 4, 'wrist': 5, 'gripper': 6}

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Setup the servo GPIO pins
for pin in servo_pins.values():
    GPIO.setup(pin, GPIO.OUT)

# Create a dictionary to store the PWM objects
servos = {joint: GPIO.PWM(pin, 50) for joint, pin in servo_pins.items()}

def set_angle(servo, angle):
    duty = angle / 18 + 2
    GPIO.output(servo_pins[servo], True)
    servo.ChangeDutyCycle(duty)
    time.sleep(1)
    servo.ChangeDutyCycle(0)
    GPIO.output(servo_pins[servo], False)

# Start PWM on all servos
for servo in servos.values():
    servo.start(0)

app = Flask(__name__)

@app.route('/commands', methods=['POST'])
def commands():
    command = request.json['command']
    if command == 'arm_up':
        # Move the arm up
        set_angle(servos['arm'], 90)
    elif command == 'arm_down':
        # Move the arm down
        set_angle(servos['arm'], 0)
    elif command == 'shoulder_up':
        # Move the shoulder up
        set_angle(servos['shoulder'], 90)
    elif command == 'shoulder_down':
        # Move the shoulder down
        set_angle(servos['shoulder'], 0)
    elif command == 'elbow_up':
        # Move the elbow up
        set_angle(servos['elbow'], 90)
    elif command == 'elbow_down':
        # Move the elbow down
        set_angle(servos['elbow'], 0)
    elif command == 'wrist_up':
        # Move the wrist up
        set_angle(servos['wrist'], 90)
    elif command == 'wrist_down':
        # Move the wrist down
        set_angle(servos['wrist'], 0)
    elif command == 'gripper_open':
        # Open the gripper
        set_angle(servos['gripper'], 90)
    elif command == 'gripper_close':
        # Close the gripper
        set_angle(servos['gripper'], 0)
    elif command == 'stop':
        # Stop all servos
        for servo in servos.values():
            servo.ChangeDutyCycle(0)
    else:
        return jsonify({'status': 'error', 'message': 'Unknown command'}), 400
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=80)
    finally:
        # Cleanup the GPIO on exit
        GPIO.cleanup()

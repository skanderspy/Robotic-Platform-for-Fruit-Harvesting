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

# Start PWM on all servos
for servo in servos.values():
    servo.start(0)

try:
    while True:
        command = input("Enter command: ")
        if command == 'up':
            # Move the arm up
            servos['arm'].ChangeDutyCycle(2)
            time.sleep(0.5)
            servos['arm'].ChangeDutyCycle(0)
        elif command == 'down':
            # Move the arm down
            servos['arm'].ChangeDutyCycle(12)
            time.sleep(0.5)
            servos['arm'].ChangeDutyCycle(0)
        # Add similar elif conditions for other commands and joints
        # ...
        elif command == 'exit':
            break
        else:
            print("Unknown command")

finally:
    # Cleanup the GPIO on exit
    GPIO.cleanup()

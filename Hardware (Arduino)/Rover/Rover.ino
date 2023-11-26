#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;

void setup() {
  Serial.begin(9600);
  servo1.attach(9);
  servo2.attach(10);
  servo3.attach(11);
  servo4.attach(12);
}

void loop() {
  if (Serial.available()) {
    char ch = Serial.read();

    switch(ch) {
      case 'w':
        // Move forward
        servo1.write(0);
        servo2.write(180);
        servo3.write(0);
        servo4.write(180);
        break;
      case 's':
        // Move backward
        servo1.write(180);
        servo2.write(0);
        servo3.write(180);
        servo4.write(0);
        break;
      case 'a':
        // Move left
        servo1.write(180);
        servo2.write(180);
        servo3.write(180);
        servo4.write(180);
        break;
      case 'd':
        // Move right
        servo1.write(0);
        servo2.write(0);
        servo3.write(0);
        servo4.write(0);
        break;
      default:
        // Stop
        servo1.detach();
        servo2.detach();
        servo3.detach();
        servo4.detach();
    }
  }
}


# import RPi.GPIO as GPIO



class MotorControl:
     def __init__(self) -> None:
        #   GPIO.setmode(GPIO.BCM)
          self.motor1_pins = (17, 18)  # Forward and backward pins
          self.motor2_pins = (22, 23)  # Left and right pins


     def initMotor(self):
          for pin in self.motor1_pins + self.motor2_pins:
               print(f"Motor pins: {pin}")
                # GPIO.setup(pin, GPIO.OUT)
                # GPIO.output(pin, GPIO.LOW)
    
     def move_left(self):
         print("move_left")
        # GPIO.output(self.motor2_pins[0], GPIO.HIGH)
        # GPIO.output(self.motor2_pins[1], GPIO.LOW)

     def move_right(self):
         print("move_right")
        # GPIO.output(self.motor2_pins[0], GPIO.LOW)
        # GPIO.output(self.motor2_pins[1], GPIO.HIGH)

     def move_forward(self):
        print("move_forward")
        # GPIO.output(self.motor1_pins[0], GPIO.HIGH)
        # GPIO.output(self.motor1_pins[1], GPIO.LOW)

     def move_backward(self):
        print("move_backward")
        # GPIO.output(self.motor1_pins[0], GPIO.LOW)
        # GPIO.output(self.motor1_pins[1], GPIO.HIGH)

     def stop_motors(self):
        for pin in self.motor1_pins + self.motor2_pins:
            print(f"Motor stop making pins low : {pin}")
            # GPIO.output(pin, GPIO.LOW)

from adafruit_servokit import ServoKit
import board
from busio import I2C
import adafruit_pca9685
import time
# import numpy as np

from color_logger import create_color_logger


class Control:
    def __init__(self):
        self.logger = create_color_logger(__name__)

        self.setup_adafruit_device()

        self.logger.info("Ready to go!")

    def setup_adafruit_device(self):
        self.logger.info(f"Founded board: {board.SCL}, {board.SDA}")
        i2c = I2C(board.SCL, board.SDA)
        pca = adafruit_pca9685.PCA9685(i2c)

        # Set the PWM frequency to 250 Hz (standard for ESCs)
        pca.frequency = 250

        self.myKit = ServoKit(channels=16)  # Initialize the ServoKit with 16 channels
        self.myKit.servo[4].actuation_range = 180  # Set actuation range for servo
        self.myKit.servo[4].set_pulse_width_range(400, 2000)  # Set pulse width range for servo

    def run(self):
        """
        Runs the control loop to receive data from the client socket, decode it, and control servo motors accordingly.
        Handles exceptions and sets servo motors to default position and throttle in case of connection loss.
        """

        angle_values = [0.0, 50.0, 100.0]
        speed_values = [-0.5, 0.0, 0.5]
        idx = 0

        try:
            # Set servo angle to default position
            self.myKit.servo[4].angle = 50
            # Set continuous servo throttle to default
            self.myKit.continuous_servo[8].throttle = 0.1

            while True:
                self.logger.info(".")

                # Read keyboard
                angle = angle_values[idx]
                speed = speed_values[idx]
                idx = (idx + 1) % 3

                if (angle < -0.5 or angle > 100.5):  # Check if angle is out of bounds
                    angle = 50  # Set angle to default position
                if (speed > 0.5 or speed < -0.5):  # Check if speed is out of bounds
                    speed = 0.1  # Set speed to default value

                self.myKit.servo[4].angle = angle
                self.myKit.continuous_servo[8].throttle = speed
                time.sleep(1)

        finally:
            self.logger.info("Stopped")
            self.myKit.servo[4].angle = 50  # Set servo angle to default position
            self.myKit.continuous_servo[8].throttle = 0.1  # Set continuous servo throttle to default


def main(args=None):
    auto = Control()
    auto.run()


if __name__ == "__main__":
    main()

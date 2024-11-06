from adafruit_servokit import ServoKit
import board
import busio
import adafruit_pca9685
import socket
import time
import argparse
import select

from color_logger import create_color_logger

class Control:
    def __init__(self, host_ip, port):
        self.host_ip = host_ip
        self.port = port
        self.logger = create_color_logger(__name__)

        self.connect_to_server()
        self.setup_adafruit_device()

        self.client_socket.send('ready'.encode())
        self.logger.info("Ready to go!")

    def connect_to_server(self):
        """
        Attempts to connect to the server continuously until successful or manually interrupted.
        Logs connection attempts and warnings.
        """
        while True:
            self.logger.info(f"Try to connect {self.host_ip} and {self.port}")

            try:
                # Create a socket object and attempt connection
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((self.host_ip, self.port))
                break

            except ConnectionRefusedError:
                self.logger.warning(f"Could not connect to server, on {self.host_ip} and {self.port}, try again.")

            time.sleep(1)

    def setup_adafruit_device(self):
        """
        Initializes the Adafruit device including the I2C bus and the PCA9685 PWM driver.
        Sets the PWM frequency to 250 Hz.
        Initializes servo motors and sets their parameters.
        """
        self.logger.info(f"Founded board: {board.SCL}, {board.SDA}")
        i2c = busio.I2C(board.SCL, board.SDA)
        pca = adafruit_pca9685.PCA9685(i2c)

        # Set the PWM frequency to 250 Hz (standard for ESCs)
        pca.frequency = 250

        self.myKit = ServoKit(channels=16)
        self.myKit.servo[4].actuation_range = 180
        self.myKit.servo[4].set_pulse_width_range(400, 2000)

    def run(self):
        """
        Runs the control loop to receive data from the client socket, decode it, and control servo motors accordingly.
        Handles exceptions and sets servo motors to default position and throttle in case of connection loss.
        """

        try:
            while True:
                data = None
                try:
                    data = self.client_socket.recv(1024)
                    print(data)
                except socket.error as socket_error:
                    self.logger.critical(f"Connection lost due to socket error: {socket_error.strerror}")
                    break

                if not data:
                    self.logger.info("No data received")
                    continue
                    # break

                decoded = data.decode('utf8').split()
                # Check for data value error
                # if (len(decoded[1].split('-')) > 1):
                #     self.logger.error("Data value error")
                # else:
                speed = float(decoded[0])
                angle = float(decoded[1])

                print(f"Received speed: {speed} angle: {angle}")

                if (angle < 0.0 or angle > 100.0):
                    angle = 50.0
                if (speed > 0.2 or speed < -0.2):
                    speed = 0.1

                self.myKit.servo[4].angle = angle
                self.myKit.continuous_servo[8].throttle = speed
        finally:
            # Set default values
            self.myKit.servo[4].angle = 50
            self.myKit.continuous_servo[8].throttle = 0.1


def main():
    parser = argparse.ArgumentParser(description="Initialize with config file")
    parser.add_argument("--host_ip", type=str, help="Remote computer IP", required=True)
    parser.add_argument("--host_port", type=int, required=True)
    args = parser.parse_args()

    host_ip = args.host_ip
    host_port = args.host_port

    auto= Control(host_ip=host_ip, port=host_port)
    auto.run()

if __name__ == "__main__":
    main()

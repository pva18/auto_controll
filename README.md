# auto_control
Setup Instructions:

1. Ensure the remote computer and the car are connected to the same network.
2. Start the auto_controll_server.py script and provide the port number as an argument.
3. Launch control.py on the car, providing the necessary arguments (IP address and port).

Once initialized, you can control the car using the W, A, S, and D commands.
The Adafruit library is currently compatible with Python 3.7 but is not supported on lower versions.

# camera

Run covert_to_vox/main.py.

Currently built for Python 3.6. Please note that pip installation is not functional for this library; manual building is required. Follow the instructions below: https://github.com/IntelRealSense/librealsense/tree/master/wrappers/python#building-from-source .

Common Issues: Occasionally, following an Ubuntu update or after installing certain packages via pip, Ubuntu may deactivate the USB port.

# socket_instance.py
from flask_socketio import SocketIO

socketio = SocketIO()

peripheral_instance = None
DEVICE_NAME = "ESP32"
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
received_messages = []

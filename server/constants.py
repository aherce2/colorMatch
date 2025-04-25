# socket_instance.py
from flask_socketio import SocketIO

DELTA_E_THRESHOLD = 1.75

# MST Reference Colors (L, a, b values)
MST_REF = {
    1: (94.211, 1.503, 5.422),
    2: (92.275, 2.061, 7.28),
    3: (93.091, 0.216, 14.205),
    4: (87.573, 0.459, 17.748),
    5: (77.902, 3.471, 23.136),
    6: (55.142, 7.783, 26.74),
    7: (42.47, 12.325, 20.53),
    8: (30.678, 11.667, 13.335),
    9: (21.069, 2.69, 5.964),
    10: (14.61, 1.482, 3.525)
}

socketio = SocketIO(max_http_buffer_size=100 * 1024 * 1024)

DEVICE_NAME = "ESP32"
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
received_messages = []

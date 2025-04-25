

from flask import Flask, jsonify
from flask_cors import CORS
import simplepyble
import logging
import time
import constants
from flask_socketio import SocketIO, emit
from constants import *
from getMatches import analyzeInput
import struct

def on_notification(data: bytes):
    if len(data) < 1:
        return
    
    message = data.decode().strip()
    if message.startswith("ACK:"):
        ack_command = message[4:]
        if ack_command == "start":
            constants.socketio.emit('scan_status', {
                'status': 'acknowledged',
                'message': 'ESP32 received start command'
            })
    else:
        header = data[0]
        payload = data[1:]
        
        if header == 0x01:  # LAB data
            try:
                # Unpack 3 floats (12 bytes) after header
                l, a, b = struct.unpack('<3f', payload)
                print(f"LAB received: [{l:.2f}, {a:.2f}, {b:.2f}]")
                analyzeInput([l,a,b])
            except struct.error:
                print("Invalid LAB payload")
        else:
            print(f"Unknown header: {hex(header)}")
        
# def send_message(message):
#     global peripheral_instance
#     try:
#         # Add connection checks
#         if not peripheral_instance:
#             logging.error("No BLE device reference")
#             return False
            
#         if not peripheral_instance or not peripheral_instance.is_connected():
#             logging.error("Device not connected")
#             return False
            
#         # Convert to byte array if needed
#         if isinstance(message, str):
#             data = message.encode()
#         else:
#             data = message
            
#         # peripheral_instance.write_request(
#         #     constants.SERVICE_UUID,
#         #     constants.CHARACTERISTIC_UUID,
#         #     data
#         # )
#         peripheral_instance.write_command(
#             constants.SERVICE_UUID,
#             constants.CHARACTERISTIC_UUID,
#             data
#         )

#         logging.info(f"Sent: {message}")
#         return True
#     except Exception as e:
#         logging.error(f"Send error: {e}")
#         return False

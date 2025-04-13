

from flask import Flask, jsonify
from flask_cors import CORS
import simplepyble
import logging
import time
import constants
from flask_socketio import SocketIO, emit
from constants import socketio
from getMatches import getUserData

import struct

def on_notification(data: bytes):
    if len(data) < 1:
        return

    header = data[0]
    payload = data[1:]
    
    if header == 0x01:  # LAB data
        try:
            # Unpack 3 floats (12 bytes) after header
            l, a, b = struct.unpack('<3f', payload)
            handle_lab(l, a, b)
        except struct.error:
            print("Invalid LAB payload")
    else:
        print(f"Unknown header: {hex(header)}")


def handle_lab(l: float, a: float, b: float):
    print(f"LAB received: [{l:.2f}, {a:.2f}, {b:.2f}]")
    target_lab = [l,a,b]
    getUserData(target_lab)

# def on_notification(data: bytes):

#     message = data.decode()
#     constants.received_messages.append(message)
    
#     # Broadcast new message to all clients
#     socketio.emit('new_message', {'message': message})


def send_message(peripheral, message):
    try:
        peripheral.write_request(constants.SERVICE_UUID, constants.CHARACTERISTIC_UUID, message.encode())
        logging.info(f"Sent: {message}")
    except Exception as e:
        logging.error(f"Error sending message: {e}")

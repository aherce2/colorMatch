

from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from constants import *
from getMatches import analyzeInput
from Helper_Functions.analyzeData import xyz_to_lab
import struct


def xyY_to_XYZ(x, y, Y):
    X = (Y / y) * x
    Z = (Y / y) * (1 - x - y)
    return X, Y, Z

def on_notification(data: bytes):
    if len(data) < 1:
        return

    try:
        # First check for ACK messages
        message = data.decode().strip()
        if message.startswith("ACK:"):
            ack_command = message[4:]
            if ack_command == "1":
                socketio.emit('scan_status', {
                    'status': 'scanning',
                    'message': 'Scanning...'
                })
            elif ack_command == "0":
                print("ACKNOWLEDGED: Scan Face")
                socketio.emit('scan_status', {
                    'status': 'scanning',
                    'message': 'Face Scanning...'
                })
            return
    except UnicodeDecodeError:
        pass  # Handle binary data below

    # Process binary data
    header = data[0]
    payload = data[1:]

    if header == 0x01 or header == 0x02:  # Single measurement or average
        if len(data) != 13:
            print(f"Invalid length {len(data)} for header {hex(header)}")
            return

        try:
            x, y, Y = struct.unpack('<fff', payload)
            print(f"Received {'average' if header == 0x02 else ''} xyY: [{x:.4f}, {y:.4f}, {Y:.4f}]")
            
            X, Y_val, Z = xyY_to_XYZ(x, y, Y)
            l, a, b = xyz_to_lab(X, Y_val, Z)
            
            socketio.emit('target_lab', {
                'target': [round(l, 2), round(a, 2), round(b, 2)]
            })
            analyzeInput([l, a, b])
            
        except (struct.error, ValueError) as e:
            print(f"Invalid payload for header {hex(header)}: {e}")

    elif header == 0x03:  # Full measurement set
        expected_length = 1 + 3*3*4  # Header + 3 measurements × 3 floats × 4 bytes
        if len(data) != expected_length:
            print(f"Invalid length {len(data)} for measurements, expected {expected_length}")
            return

        try:
            measurements = struct.unpack('<9f', payload)
            print("Received 3 measurements:")
            
            for i in range(3):
                offset = i * 3
                x, y, Y = measurements[offset:offset+3]
                print(f"xyY: [{x:.4f}, {y:.4f}, {Y:.4f}]")

                X, Y_val, Z = xyY_to_XYZ(x, y, Y)
                l, a, b = xyz_to_lab(X, Y_val, Z)

        except struct.error as e:
            print(f"Failed to unpack measurements: {e}")

    else:
        print(f"Unknown header: {hex(header)}")

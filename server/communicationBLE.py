

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
        # Handle binary data that can't be decoded to string
        pass

    # Process binary LAB data
    if len(data) == 13:
        header = data[0]
        payload = data[1:]
        if header == 0x01:  # LAB data
            try:
                # Verify payload length matches 3 floats (12 bytes)
                if len(payload) != 12:
                    raise ValueError("Invalid payload length")
                
                # x,y,Y = struct.unpack('<fff', payload)
                # Unpack little-endian floats (ESP32 uses little-endian)
                x, y, Y = struct.unpack('<fff', data[1:13])
            
                print(f"Recieved xyY values: [{x:.2f}, {y:.2f}, {Y:.2f}]")
                X,Y, Z = xyY_to_XYZ(x,y,Y)
                print(f"XYZ Values Converted: [{X:.2f}, {Y:.2f}, {Z:.2f}]")
                l,a,b = xyz_to_lab(X,Y,Z)
                # Unpack 3 floats (little-endian format)
                # l, a, b = struct.unpack('<fff', payload)
                print(f"Converted LAB Values: [{l:.2f}, {a:.2f}, {b:.2f}]")
                
                # Update frontend with raw LAB values
                socketio.emit('target_lab', {
                    'target': [round(l, 2), round(a, 2), round(b, 2)]
                })
                
                # Process analysis
                analyzeInput([l, a, b])
            except (struct.error, ValueError) as e:
                print(f"Invalid LAB payload: {e}")
                
        elif header == 0x02: 
            print("ESP Returned")        
            
        else:
            print(f"Unknown header: {hex(header)}")
    else:
        print(f"Received unexpected data: {data.hex()}")



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
                print(f"  Measurement {i+1}:")
                print(f"    x: {x:.4f}")
                print(f"    y: {y:.4f}")
                print(f"    Y: {Y:.4f}")
                
                # Uncomment to emit individual measurements to frontend
                # X, Y_val, Z = xyY_to_XYZ(x, y, Y)
                # l, a, b = xyz_to_lab(X, Y_val, Z)
                # socketio.emit('measurement_update', {
                #     'index': i+1,
                #     'xyY': [x, y, Y],
                #     'LAB': [l, a, b]
                # })

        except struct.error as e:
            print(f"Failed to unpack measurements: {e}")

    else:
        print(f"Unknown header: {hex(header)}")

# def on_notification(data: bytes):
#     if len(data) < 1:
#         return

#     try:
#         # First check for ACK messages
#         message = data.decode().strip()
#         if message.startswith("ACK:"):
#             ack_command = message[4:]
#             if ack_command == "1":

#                 socketio.emit('scan_status', {
#                     'status': 'scanning',
#                     'message': 'Scanning...'
#                 })
#             elif ack_command == "0":
#                 print("ACKNOWLEDGED: Scan Face")
#                 socketio.emit('scan_status', {
#                     'status': 'scanning',
#                     'message': 'Face Scanning...'
#                 })
#             return
#     except UnicodeDecodeError:
#         # Handle binary data that can't be decoded to string
#         pass

#     # Process binary LAB data
#     if len(data) == 13:
#         header = data[0]
#         payload = data[1:]
#         if header == 0x01:  # LAB data
#             try:
#                 # Verify payload length matches 3 floats (12 bytes)
#                 if len(payload) != 12:
#                     raise ValueError("Invalid payload length")
                
#                 # x,y,Y = struct.unpack('<fff', payload)
#                 # Unpack little-endian floats (ESP32 uses little-endian)
#                 x, y, Y = struct.unpack('<fff', data[1:13])
            
#                 print(f"Recieved xyY values: [{x:.2f}, {y:.2f}, {Y:.2f}]")
#                 X,Y, Z = xyY_to_XYZ(x,y,Y)
#                 print(f"XYZ Values Converted: [{X:.2f}, {Y:.2f}, {Z:.2f}]")
#                 l,a,b = xyz_to_lab(X,Y,Z)
#                 # Unpack 3 floats (little-endian format)
#                 # l, a, b = struct.unpack('<fff', payload)
#                 print(f"Converted LAB Values: [{l:.2f}, {a:.2f}, {b:.2f}]")
                
#                 # Update frontend with raw LAB values
#                 socketio.emit('target_lab', {
#                     'target': [round(l, 2), round(a, 2), round(b, 2)]
#                 })
                
#                 # Process analysis
#                 analyzeInput([l, a, b])
#             except (struct.error, ValueError) as e:
#                 print(f"Invalid LAB payload: {e}")
                
#         elif header == 0x02: 
#             try:
#                 # Verify payload length matches 3 floats (12 bytes)
#                 if len(payload) != 12:
#                     raise ValueError("Invalid payload length")
                
#                 # x,y,Y = struct.unpack('<fff', payload)
#                 # Unpack little-endian floats (ESP32 uses little-endian)
#                 x, y, Y = struct.unpack('<fff', data[1:13])

#                 print(f"Recieved Average xyY values: [{x:.2f}, {y:.2f}, {Y:.2f}]")
#                 X,Y, Z = xyY_to_XYZ(x,y,Y)
#                 print(f"XYZ Values Converted: [{X:.2f}, {Y:.2f}, {Z:.2f}]")
#                 l,a,b = xyz_to_lab(X,Y,Z)
#                 # Unpack 3 floats (little-endian format)
#                 # l, a, b = struct.unpack('<fff', payload)
#                 print(f"Converted LAB Values: [{l:.2f}, {a:.2f}, {b:.2f}]")
                
#                 # Update frontend with raw LAB values
#                 socketio.emit('target_lab', {
#                     'target': [round(l, 2), round(a, 2), round(b, 2)]
#                 })
                
#                 # Process analysis
#                 analyzeInput([l, a, b])
#             except (struct.error, ValueError) as e:
#                 print(f"Invalid LAB payload: {e}")      
        
#         else:
#             print(f"Unknown header: {hex(header)}")
#     if data[0] == 0x03:
#         try:
#             # Verify payload length matches 3 measurements × 3 floats (36 bytes)
#             if len(payload) != 3 * 3 * 4: 
#                 raise ValueError(f"Invalid payload length for measurements: {len(payload)} bytes")

#             # Unpack 9 floats (3 measurements × x,y,Y)
#             measurements = struct.unpack('<9f', payload)
            
#             # Group into 3-tuples and print
#             print(f"Received 3 measurements via header 0x03:")
#             for i in range(0, 9, 3):
#                 x, y, Y = measurements[i:i+3]
#                 print(f"  Measurement {i//3 + 1}:")
#                 print(f"    x: {x:.4f}")
#                 print(f"    y: {y:.4f}")
#                 print(f"    Y: {Y:.4f}")
                
#                 # X, Y_val, Z = xyY_to_XYZ(x, y, Y)
#                 # l, a, b = xyz_to_lab(X, Y_val, Z)
                
#                 # socketio.emit('measurement_update', {
#                 #     'measurement': i//3 + 1,
#                 #     'xyY': [round(x,4), round(y,4), round(Y,4)],
#                 #     'LAB': [round(l,2), round(a,2), round(b,2)]
#                 # })
            

#         except (struct.error, ValueError) as e:
#             print(f"Failed to parse measurement data: {str(e)}")
#     else:
#         print(f"Received unexpected data: {data.hex()}")

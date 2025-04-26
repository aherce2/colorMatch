

from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from constants import *
from getMatches import analyzeInput
import struct
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
    if len(data) >= 13:
        header = data[0]
        payload = data[1:]
        
        if header == 0x01:  # LAB data
            try:
                # Verify payload length matches 3 floats (12 bytes)
                if len(payload) != 12:
                    raise ValueError("Invalid payload length")
                    
                # Unpack 3 floats (little-endian format)
                l, a, b = struct.unpack('<fff', payload)
                print(f"LAB received: [{l:.2f}, {a:.2f}, {b:.2f}]")
                
                # Update frontend with raw LAB values
                socketio.emit('target_lab', {
                    'target': [round(l, 2), round(a, 2), round(b, 2)]
                })
                
                # Process analysis
                analyzeInput([l, a, b])
                
            except (struct.error, ValueError) as e:
                print(f"Invalid LAB payload: {e}")
        else:
            print(f"Unknown header: {hex(header)}")
    else:
        print(f"Received unexpected data: {data.hex()}")

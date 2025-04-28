from flask import Flask, jsonify, request
from flask_cors import CORS
from ble import disconnect_ble, connect_ble, send_message
from communicationBLE import on_notification
import constants
from constants import socketio
from uploadImage import process_image_enhanced
from skimage import color
from getMatches import analyzeInput
import os
from Helper_Functions.analyzeData import xyz_to_lab
import numpy as np

# Create An App Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# Initialize SocketIO with app
socketio.init_app(app, cors_allowed_origins="*")

# Enable Origins -> Accept all origins for now
cors = CORS(app, origins='*')


@socketio.on('ble_connect')
def handle_ble_connect():
    success = connect_ble()
    if success:
        socketio.emit('ble_status', {'status': 'connected', 'message': 'BLE device connected'})
    else:
        socketio.emit('ble_status', {'status': 'error', 'message': 'Connection failed'})

@socketio.on('ble_disconnect')
def handle_ble_disconnect():
    success = disconnect_ble()
    if success:
        socketio.emit('ble_status', {'status': 'disconnected', 'message': 'BLE device disconnected'})
    else:
        socketio.emit('ble_status', {'status': 'error', 'message': 'Disconnection failed'})

@socketio.on('get_oneshot')
def handle_oneshot(lab):
    analyzeInput(lab)

@socketio.on('analyze_input')
def handle_analysis(data, image_buffer):
    if data.get('color', False):

        rgb = data.get('rgb', [0, 0, 0])
        normalized_rgb = np.array([rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0])
        print(rgb, normalized_rgb)
        lab_values = color.rgb2lab([normalized_rgb])[0]
        # lab_values = xyz_to_lab(normalized_rgb)
        products = analyzeInput(lab_values)
        print(products)
    else:
        # Process image upload
        filename = data.get('filename', 'untitled')
        with open(f"uploads/{filename}", "wb") as f:
            f.write(image_buffer)

        avg_rgb, hex_color, _ = process_image_enhanced(image_buffer)
        print(avg_rgb)
        normalized_rgb = np.array([avg_rgb[0]/255.0, avg_rgb[1]/255.0, avg_rgb[2]/255.0])
        # print(normalized_rgb)
        lab_values = color.rgb2lab(normalized_rgb)     
        # print(lab_values)
        analyzeInput(lab_values)


@socketio.on('start_scan')
def handle_start_scan(data):
    command = data.get('command', '1')  # Default to '1' if not provided
    success = send_message(command)  # Send raw command to BLE
    
    if success:
        socketio.emit('scan_status', {
            'status': 'sent',
            'message': f'Command {command} sent successfully'
        })
    else:
        socketio.emit('scan_status', {
            'status': 'error',
            'message': f'Failed to send command {command}'
        })


if __name__ == "__main__":
    socketio.run(app, debug=True, port=8080)

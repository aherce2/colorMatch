from flask import Flask, jsonify, request
from flask_cors import CORS
from ble import disconnect_ble, connect_ble
from communicationBLE import on_notification
import constants
from constants import socketio
from uploadImage import process_image_enhanced
from skimage import color
from getMatches import analyzeInput
import os
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

@socketio.on('analyze_input')
def handle_analysis(data, image_buffer):
    if data.get('color', False):

        rgb = data.get('rgb', [0, 0, 0])
        normalized_rgb = np.array([rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0])
        print(rgb, normalized_rgb)
        lab_values = color.rgb2lab([normalized_rgb])[0]
        products = analyzeInput(lab_values)
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
        products = analyzeInput(lab_values)

if __name__ == "__main__":
    socketio.run(app, debug=True, port=8080)

from flask import Flask, jsonify, request
from flask_cors import CORS
from ble import disconnect_ble, connect_ble
from communicationBLE import on_notification
import constants
from constants import socketio

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


if __name__ == "__main__":
    # app.run(debug=True, port=8080)
    socketio.run(app, debug=True, port=8080)

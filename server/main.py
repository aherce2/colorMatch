from flask import Flask, jsonify, request
from flask_cors import CORS
from ble import disconnect_ble, connect_ble, send_ble_message
# Create An App Instance
app = Flask(__name__)

# Enable Origins -> Accept all origins for now
cors = CORS(app, origins='*')

@app.route("/api/ble/<status>", methods=['GET'])
def handle_ble(status):
    if status.lower() == 'true':
        if disconnect_ble():
            return jsonify(success=True, message="Disconnected from BLE Device")
        return jsonify(success=False, message="Disconnection failed")
    
    elif status.lower() == 'false':
        if connect_ble():
            return jsonify(success=True, message="Connected to BLE Device")
        return jsonify(success=False, message="Connection failed")
    
    return jsonify(success=False, message="Invalid status")

@app.route("/api/send_message", methods=['POST'])
def send_message():
    message = request.json.get('message')
    if send_ble_message(message):
        return jsonify(success=True)
    return jsonify(success=False)

@app.route("/api/receive_messages", methods=['GET'])
def get_messages():
    global received_messages
    messages = received_messages.copy()
    received_messages.clear()
    return jsonify(messages=messages)

if __name__ == "__main__":
    app.run(debug=True, port=8080)

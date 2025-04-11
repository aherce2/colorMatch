from flask import Flask, jsonify, request
from flask_cors import CORS
from ble import disconnect_ble, connect_ble
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

if __name__ == "__main__":
    app.run(debug=True, port=8080)

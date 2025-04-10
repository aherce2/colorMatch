from flask import Flask, jsonify
from flask_cors import CORS
from ble import get_ble
# Create An App Instance
app = Flask(__name__)

# Enable Origins -> Accept all origins for now
cors = CORS(app, origins='*')

# Modify to establish BLE and wait
@app.route("/api/ble/<status>", methods=['GET'])
def bluetooth_connection(status):

    # Device is connected -> Disconnect from Device
    if status.lower() == 'true':
        return jsonify({
            "success": True,
            "message": "Disconnected from BLE Device"
        })
    # Device is disconnected -> Connect to Device
    elif status.lower() == 'false':
        return jsonify({
            "success": True,
            "message": "Connected to BLE Device"
        })
    else:
        return jsonify({
            "success": False,
            "message": "Invalid status provided"
        }), 400



# Modify to establish BLE and wait
@app.route("/api/ble", methods=['POST'])
def bluetooth_connection():
    return get_ble()



if __name__ == "__main__":
    app.run(debug=True, port=8080)

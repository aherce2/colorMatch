from flask import Flask, jsonify
from flask_cors import CORS
from ble import get_ble
# Create An App Instance
app = Flask(__name__)

# Enable Orgins -> Accept all origins for now
cors = CORS(app, origins='*')

@app.route("/api/users", methods=['GET'])
def users():
    return jsonify(
        {
            "users": [
                'Ashley',
                'Angel'   
            ]
            
        }
    )


# Modify to establish BLE and wait
@app.route("/api/ble", methods=['POST'])
def bluetooth_connection():
    return get_ble()



if __name__ == "__main__":
    app.run(debug=True, port=8080)
'''
Connect to BLE Device
'''
from flask import Flask, jsonify
from flask_cors import CORS
import simplepyble
import logging
import time

app = Flask(__name__)
cors = CORS(app, origins='*')

# Global BLE variables
peripheral_instance = None
DEVICE_NAME = "ESP32"
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def select_adapter():
    adapters = simplepyble.Adapter.get_adapters()
    return adapters[0] if adapters else None

def find_device(adapter):
    adapter.scan_for(2000)
    for peripheral in adapter.scan_get_results():
        if peripheral.identifier() == DEVICE_NAME:
            return peripheral
    return None

def connect_ble():
    global peripheral_instance
    try:
        adapter = select_adapter()
        if not adapter:
            return False
        
        peripheral = find_device(adapter)
        if not peripheral:
            return False
        
        peripheral.connect()
        time.sleep(2)
        
        if peripheral.is_connected():
            peripheral_instance = peripheral
            return True
        return False
    
    except Exception as e:
        logging.error(f"Connection error: {str(e)}")
        return False

def disconnect_ble():
    global peripheral_instance
    if peripheral_instance and peripheral_instance.is_connected():
        try:
            peripheral_instance.disconnect()
            peripheral_instance = None
            return True
        except Exception as e:
            logging.error(f"Disconnection error: {str(e)}")
    return False

# @app.route("/api/ble/<status>", methods=['GET'])
# def handle_ble(status):
#     if status.lower() == 'true':
#         if disconnect_ble():
#             return jsonify(success=True, message="Disconnected from BLE Device")
#         return jsonify(success=False, message="Disconnection failed")
    
#     elif status.lower() == 'false':
#         if connect_ble():
#             return jsonify(success=True, message="Connected to BLE Device")
#         return jsonify(success=False, message="Connection failed")
    
#     return jsonify(success=False, message="Invalid status"), 400

# if __name__ == "__main__":
#     app.run(debug=True, port=8080)

'''
Connect to BLE Device
'''
from flask import Flask, jsonify
from flask_cors import CORS
import simplepyble
import logging
import time
from communicationBLE import on_notification, send_message

app = Flask(__name__)
cors = CORS(app, origins='*')

# Global BLE variables
peripheral_instance = None
DEVICE_NAME = "ESP32"
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

MESSAGE_CHAR_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
received_messages = []

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def select_adapter():
    adapters = simplepyble.Adapter.get_adapters()
    return adapters[0] if adapters else None

def find_device(adapter):
    adapter.scan_for(2000)
    for peripheral in adapter.scan_get_results():
        if peripheral.identifier() == DEVICE_NAME:
            logging.info(f"Found device: {DEVICE_NAME}")
            return peripheral
    return None

def connect_ble():
    global peripheral_instance
    try:
        adapters = simplepyble.Adapter.get_adapters()
        if not adapters:
            logging.error("No BLE adapters found")
            return False

        adapter = adapters[0]
        adapter.scan_for(5000)
        peripherals = adapter.scan_get_results()

        for peripheral in peripherals:
            if peripheral.identifier() == DEVICE_NAME:
                logging.info(f"Found device: {DEVICE_NAME}")
                peripheral_instance = peripheral
                break

        if not peripheral_instance:
            logging.error(f"Device '{DEVICE_NAME}' not found")
            return False

        peripheral_instance.connect()
        time.sleep(3)

        if peripheral_instance.is_connected():
            logging.info(f"Connected to {DEVICE_NAME}")
        else:
            logging.error("Failed to connect to the device")
        try:
            peripheral.notify(SERVICE_UUID, CHARACTERISTIC_UUID, on_notification)
            logging.info("Notifications enabled")
            return True
        except Exception as e:
            logging.error(f"Error enabling notifications: {e}")
            return False
    
    except Exception as e:
        logging.error(f"Error during BLE connection: {str(e)}")
        if peripheral_instance:
            peripheral_instance.disconnect()
            peripheral_instance = None
        return False
    
def disconnect_ble():
    global peripheral_instance
    if peripheral_instance and peripheral_instance.is_connected():
        try:            
            while True:
                try:
                    logging.info("Attempting to disconnect from BLE device...")
                    peripheral_instance.disconnect()
                    time.sleep(1)  # Allow time for disconnection to complete
                    
                    if not peripheral_instance.is_connected():
                        logging.info("Successfully disconnected from BLE device")
                        peripheral_instance = None
                        return True
                        
                    logging.warning("Disconnection not acknowledged. Retrying...")
                    time.sleep(3)
                        
                except Exception as e:
                    logging.error(f"Disconnection error: {str(e)}. Retrying in {3} seconds...")
                    time.sleep(3)
        except Exception as e:
            logging.error(f"Critical disconnection error: {str(e)}")
            return False
    else:
        logging.warning("No connected BLE device found to disconnect")
        return False

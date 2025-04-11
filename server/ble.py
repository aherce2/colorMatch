'''
Connect to BLE Device
'''
from flask_cors import CORS
import simplepyble
import logging
import time
from communicationBLE import on_notification, send_message
import constants


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def select_adapter():
    adapters = simplepyble.Adapter.get_adapters()
    return adapters[0] if adapters else None

def find_device(adapter):
    adapter.scan_for(2000)
    for peripheral in adapter.scan_get_results():
        if peripheral.identifier() == constants.DEVICE_NAME:
            logging.info(f"Found device: {constants.DEVICE_NAME}")
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
            if peripheral.identifier() == constants.DEVICE_NAME:
                logging.info(f"Found device: {constants.DEVICE_NAME}")
                peripheral_instance = peripheral
                break

        if not peripheral_instance:
            logging.error(f"Device '{constants.DEVICE_NAME}' not found")
            return False

        peripheral_instance.connect()
        time.sleep(3)

        if peripheral_instance.is_connected():
            logging.info(f"Connected to {constants.DEVICE_NAME}")
        else:
            logging.error("Failed to connect to the device")
        try:
            peripheral.notify(constants.SERVICE_UUID, constants.CHARACTERISTIC_UUID, on_notification)
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
                    time.sleep(5)  # Allow time for disconnection to complete
                    
                    if not peripheral_instance.is_connected():
                        logging.info("Successfully disconnected from BLE device")
                        peripheral_instance = None
                        return True
                        
                    logging.warning("Disconnection not acknowledged. Retrying...")
                    time.sleep(5)
                        
                except Exception as e:
                    logging.error(f"Disconnection error: {str(e)}. Retrying in {5} seconds...")
                    time.sleep(5)
        except Exception as e:
            logging.error(f"Critical disconnection error: {str(e)}")
            return False
    else:
        logging.warning("No connected BLE device found to disconnect")
        return False

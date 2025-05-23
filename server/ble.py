'''
Connect to BLE Device
'''
from flask_cors import CORS
import simplepyble
import logging
import time
from communicationBLE import on_notification
import constants

peripheral_instance = None

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
        # reeset instance before new connection
        peripheral_instance = None

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

        if peripheral_instance is None:
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
            logging.info("Unsubscribing from notifications...")
            peripheral_instance.unsubscribe(constants.SERVICE_UUID, constants.CHARACTERISTIC_UUID)
            time.sleep(2)  
        except Exception as e:
            logging.error(f"Error unsubscribing: {e}")

        retries = 3
        while retries > 0:
            try:
                logging.info(f"Disconnecting attempt {4-retries}/3...")
                peripheral_instance.disconnect()
                time.sleep(2)

                if not peripheral_instance.is_connected():
                    logging.info("Successfully disconnected")
                    peripheral_instance = None
                    return True

                retries -= 1
                time.sleep(2)
            except Exception as e:
                logging.error(f"Disconnection error: {e}")
                retries -= 1

        logging.error("Failed to disconnect after 3 attempts")
        return False
    else:
        logging.warning("No active connection")
        return False

        
def send_message(message):
    global peripheral_instance
    try:
        # Add connection checks
        if not peripheral_instance:
            logging.error("No BLE device reference")
            return False
            
        if not peripheral_instance or not peripheral_instance.is_connected():
            logging.error("Device not connected")
            return False
            
        # Convert to byte array if needed
        if isinstance(message, str):
            data = message.encode()
        else:
            data = message
            
        # peripheral_instance.write_request(
        #     constants.SERVICE_UUID,
        #     constants.CHARACTERISTIC_UUID,
        #     data
        # )
        peripheral_instance.write_command(
            constants.SERVICE_UUID,
            constants.CHARACTERISTIC_UUID,
            data
        )

        logging.info(f"Sent: {message}")
        return True
    except Exception as e:
        logging.error(f"Send error: {e}")
        return False

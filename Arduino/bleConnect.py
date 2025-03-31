import simplepyble
import logging
import time
import keyboard

DEVICE_NAME = "ESP32-BLE"
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def select_adapter(adapters):
    if len(adapters) == 0:
        logging.error("No adapters found")
        return None
    elif len(adapters) == 1:
        logging.info(f"Found 1 adapter: {adapters[0].identifier()} [{adapters[0].address()}]")
        return adapters[0]
    else:
        logging.info("Please select an adapter: ")
        for i, adapter in enumerate(adapters):
            logging.info(f"{i}: {adapter.identifier()} [{adapter.address()}]")
        choice = int(input("Enter choice: "))
        return adapters[choice]

def find_device(adapter):
    adapter.set_callback_on_scan_start(lambda: logging.info("Scan started."))
    adapter.set_callback_on_scan_stop(lambda: logging.info("Scan complete."))
    adapter.set_callback_on_scan_found(lambda peripheral: logging.info(f"Found {peripheral.identifier()} [{peripheral.address()}]"))
    adapter.scan_for(2000)
    peripherals = adapter.scan_get_results()
    for i, peripheral in enumerate(peripherals):
        if peripheral.identifier() == DEVICE_NAME:
            logging.info(f"Found {DEVICE_NAME} at address [{peripheral.address()}]")
            return peripherals[i]
    logging.error(f"Could not find device with name '{DEVICE_NAME}'")
    time.sleep(10)
    return None

def main():
    # Get a list of available Bluetooth adapters
    adapters = simplepyble.Adapter.get_adapters()
    adapter = select_adapter(adapters)  # Assuming this selects an adapter
    if not adapter:
        return

    logging.info(f"Selected adapter: {adapter.identifier()} [{adapter.address()}]")

    # Find the peripheral device (ESP32 or other BLE device)
    peripheral = find_device(adapter)  # Assuming this finds the device
    if not peripheral:
        return

    logging.info(f"Connecting to: {peripheral.identifier()} [{peripheral.address()}]")
    peripheral.connect()
    time.sleep(3)
    if peripheral.is_connected():
        logging.info("Successfully connected to the peripheral")
    else:
        logging.error("Failed to connect to the peripheral")
        return

    
    # Enter a loop to continuously check for received messages
    while True:
        if keyboard.is_pressed('q'):  # 'q' press detected
            logging.info("q pressed! Disconnecting...")
            peripheral.disconnect()  # Disconnect the peripheral
            break  # Exit the loop and program

        try:
            response = peripheral.read(SERVICE_UUID, CHARACTERISTIC_UUID)
            if response:
                logging.info(f"Received response: {response.decode()}")  # Output the received message
        except Exception as e:
            logging.error(f"Error reading response: {e}")

        time.sleep(0.1)


if __name__ == "__main__":
    main()

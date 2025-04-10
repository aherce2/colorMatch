'''
Connect to BLE Device
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage.color import lab2rgb, deltaE_ciede2000
import sqlite3
import os
import math
import simplepyble
import logging
import time
import keyboard
import struct

DEVICE_NAME = "ESP32-BLE"
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    

# BLE Connection
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

def parse_ble_lab(response):
    """Convert BLE response to LAB tuple with error handling"""
    try:
        lab_str = response.decode().strip()
        l, a, b = map(float, lab_str.split(','))
        return (l, a, b)

    except Exception as e:
        logging.error(f"BLE parse error: {str(e)}")
        return None

def get_ble():

    """Connect to BLE device"""
    adapter = select_adapter(simplepyble.Adapter.get_adapters())
    if not adapter:
        return None

    peripheral = find_device(adapter)
    if not peripheral:
        return None

    try:
        peripheral.connect()
        time.sleep(2)  # Reduced connection time
        
        if not peripheral.is_connected():
            logging.error("Connection failed")
            return None

        # Single read instead of continuous loop
        response = peripheral.read(SERVICE_UUID, CHARACTERISTIC_UUID)
        if response:
            return parse_ble_lab(response)
                
    except Exception as e:
        logging.error(f"BLE Error: {e}")
    finally:
        if peripheral.is_connected():
            peripheral.disconnect()
            
    return None
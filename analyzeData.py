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

def connect(filepath="database.db"):
    # connect to database 
    db_path = os.path.join(filepath)
    print("Database Path:", db_path)
    conn = sqlite3.connect(db_path)
    
    # cursor object 
    return conn.cursor(), conn
    
# Close Connection to Database
def close_connection(conn):
    return conn.close()
    
def convert_to_rgb(lab_color):
    lab_array = np.array([[lab_color]], dtype=np.float64)
    rgb_array = lab2rgb(lab_array).squeeze()
    return np.clip(rgb_array * 255, 0, 255).astype(int)

def f(t):
    if t > 0.008856:
        return t ** (1/3.0)
    else:
        return 7.787 * t + 16/116.0
    
def xyz_to_lab(X, Y, Z, Xn=95.047, Yn=100, Zn=108.88):
    fx = f(X / Xn)
    fy = f(Y / Yn)
    fz = f(Z / Zn)
    
    L = 116 * fy - 16
    a = 500 * (fx - fy)
    b = 200 * (fy - fz)
    
    return L, a, b

def calculate_color_differences(df, lab_values, target_lab):
    # Convert to NumPy arrays
    lab_values = df[['L', 'a', 'b']].values.astype(float) 
    target_array = np.array(target_lab).reshape(1, 3) 

    # Compute deltaE for all rows
    deltaE = deltaE_ciede2000(lab_values, target_array)
    
    df['deltaE'] = deltaE
    return df.sort_values(by='deltaE')


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

def get_ble_lab():
    """Connect to BLE device and return LAB values"""
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
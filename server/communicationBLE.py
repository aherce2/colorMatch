

from flask import Flask, jsonify
from flask_cors import CORS
import simplepyble
import logging
import time

DEVICE_NAME = "ESP32"
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

MESSAGE_CHAR_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

def on_notification(data: bytes):
    logging.info(f"Received notification: {data.decode()}")

def send_message(peripheral, message):
    try:
        peripheral.write_request(SERVICE_UUID, CHARACTERISTIC_UUID, message.encode())
        logging.info(f"Sent: {message}")
    except Exception as e:
        logging.error(f"Error sending message: {e}")
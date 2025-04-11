

from flask import Flask, jsonify
from flask_cors import CORS
import simplepyble
import logging
import time
import constants
from flask_socketio import SocketIO, emit
from constants import socketio


def on_notification(data: bytes):
    # try:
    #     message = data.decode()
    #     logging.info(f"Received notification: {message}")
    #     constants.received_messages.append(message)
        
    #     # Emit through shared socketio instance
    #     socketio.emit('new_message', {'message': message})
        
    #     return message
    # except Exception as e:
    #     logging.error(f"Notification error: {str(e)}")
    #     return None
    message = data.decode()
    constants.received_messages.append(message)
    
    # Broadcast new message to all clients
    socketio.emit('new_message', {'message': message})


def send_message(peripheral, message):
    try:
        peripheral.write_request(constants.SERVICE_UUID, constants.CHARACTERISTIC_UUID, message.encode())
        logging.info(f"Sent: {message}")
    except Exception as e:
        logging.error(f"Error sending message: {e}")
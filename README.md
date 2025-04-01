# colorMatch
Color Matcher Code for Arduino + SQLite3 Code Interaction

colorMatch

├── Arduino

│   ├── ESP-BLE/

│   ├── connectColorSensor

│   ├── connectI2C

│   ├── sendMessage

│   ├── bleConnect.py

├── README.md

├── Color Analysis

│   ├── \_\_pycache\_\_

│   ├── csv files

      │	│   ├── ECE 445 Product Data.xlsx

      │	│   ├── cielab.csv

      │	│   ├── shades.csv

│   ├── cielab\_data.npy

│   ├── classifyData.ipynb

│   ├── database.db

│   ├── demo.py

│   ├── getMatches.py

│   └── helperFunctions.py

└── database.db

---

## ESP-BLE

Basic ESP32-S3 BLE Connection. Works with bleConnect.py to send and receive messages

## connectColorSensor

Establish BLE connection and I2C connection with bleConnect.py to send sensor data 

## classifyData.ipynb

Script to classify shades into 1 of 10 Monk Categories based on calculated L\*a\*b\* values. Returns csv file with Monk Category and Lab values.

## getMatches.py

Script to find products matching input XYZ values. Calculates corresponding L\*a\*b\* values and returns products within Delta E threshold. 

## helperFunctions.py

Helper functions used in getMatches.py for cleanliness
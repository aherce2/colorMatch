#include "arduino_secrets.h"

/*

Code to set up ESP32 to read color data from SparkFun OPT4048 Color Sensor, convert to CIELAB color space 
and send data over Bluetooth Low Energy (BLE) to a connected device. 

XYZ -> LAB allows the color data to be more perceptually uniform 

*/

#include <Wire.h>
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include "SparkFun_OPT4048.h"

// I2C Configuration
#define I2C_ADDR 0x44 //default address for OPT4048
#define SDA_PIN 4 //Blue Wire Data Line
#define SCL_PIN 5 //Yellow Wire Clock Line

//object of OPT4048 Breakout to interact
SparkFun_OPT4048 colorSensor;

// BLE Configuration
#define DEVICE_NAME "ESP32-BLE" //name to identify BLE Device

//Unique Identifier for BLE Service for ESP 
#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
//Identifier for the data point to expose BLE Service (Read, Write, notify)
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"


//Global Constants


BLEServer* pServer; //pointer to BLE Server object, that manages BLE connection
BLECharacteristic* pCharacteristic; //Pointer to BLE that has Color Data

// Conversion Constants (D65 illuminant)
const float Xn = 95.047f;
const float Yn = 100.0f;
const float Zn = 108.883f;


/* Class handles events related to BLE Connection

  Use BLEServerCallbacks class to define actions when BLE client connects & disconnects from ESP32
  
  Important for managing the state of BLE server and take necessary actions


*/

class ServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
        Serial.println("BLE Connected");
    }

    void onDisconnect(BLEServer* pServer) {
        Serial.println("Device disconnected");
        // Restart BLE advertising on disconnect from BLE Device
        pServer->startAdvertising();
        Serial.println("BLE Advertising");
    }
};
/*

Function to convert XYZ Data Color Space to LAB Color Space

Xn, Yn, Zn: Reference values for D65 Illuminant (Standard Light)
Epsilon & Kappa: Constants for color conversion with color perception non-linearity

Inputs: X,Y,Z 
Outputs:L,a, b

*/
void convertXYZtoLAB(float X, float Y, float Z, float* L, float* a, float* b) {
    Serial.println("Mearued XYZ Values:" + String(X) + "," + String(Y) + "," + String(Z));
    const float epsilon = 0.008856f;
    const float kappa = 903.3f;
    
    float xr = X / Xn;
    float yr = Y / Yn;
    float zr = Z / Zn;
    
    float fx = (xr > epsilon) ? cbrt(xr) : (kappa * xr + 16.0f) / 116.0f;
    float fy = (yr > epsilon) ? cbrt(yr) : (kappa * yr + 16.0f) / 116.0f;
    float fz = (zr > epsilon) ? cbrt(zr) : (kappa * zr + 16.0f) / 116.0f;
    
    *L = 116.0f * fy - 16.0f;
    *a = 500.0f * (fx - fy);
    *b = 200.0f * (fy - fz);
}
void getXYZ(){
    float X = colorSensor.getADCCh0();
    float Y = colorSensor.getADCCh1();
    float Z = colorSensor.getADCCh2();
    float LUM = colorSensor.getADCCh3();
}
void setup() {
    //Initialize serial communication with baud rate of 115200
    Serial.begin(115200);
    delay(5000); //Wait 5 Seconds

    // Initialize I2C
    Wire.begin(SDA_PIN, SCL_PIN); //Initialize Specific GPIO Pins for I2C
    
    //Initialize color sensor and establish communication
    if (!colorSensor.begin(I2C_ADDR)) { 
        //infinite loop if connection fails
        Serial.println("Color sensor not found!");
        while(1);
    }
    //configure sensor setup for basic operation
    colorSensor.setBasicSetup();
    
    // Initialize BLE
    BLEDevice::init(DEVICE_NAME);
    //create BLE server to host the service and characteristics
    pServer = BLEDevice::createServer(); 
    //Set a callback for BLE connection events (onConnect & onDisconnect)
    pServer->setCallbacks(new ServerCallbacks());
    
    BLEService* pService = pServer->createService(SERVICE_UUID); //creates a new BLE Service with unique UUID
    pCharacteristic = pService->createCharacteristic(
        //create new characterisitcs within the service
        //Allows: Read, Write, Notify Updates
        CHARACTERISTIC_UUID,
        BLECharacteristic::PROPERTY_READ |
        BLECharacteristic::PROPERTY_WRITE |
        BLECharacteristic::PROPERTY_NOTIFY
    );
    //Set the permissions for the characteristics (read & write access)
    pCharacteristic->setAccessPermissions(ESP_GATT_PERM_READ | ESP_GATT_PERM_WRITE);



    /* Bluetooth Security for BLE to ensure device is encrypted and authenticated

      Security Settings:
      - Authentication Mode: How devices authenticate each other
      - IO Capabilities: How Devices interact with users for authentication (entering a pin, using encryption)
      - Encrpytion: Ensure data exchange between devices is not intercepted and read by unauthorized third parties
    
    */


    //Configure BLE Security Settings (No Pairing Required and no I/O capabilities)
    BLESecurity *pSecurity = new BLESecurity();
    pSecurity->setAuthenticationMode(ESP_LE_AUTH_NO_BOND); //how BLE device authenticates each other: No authentication or pairing required
    pSecurity->setCapability(ESP_IO_CAP_NONE); //No user interactions needed for authentication
    pSecurity->setInitEncryptionKey(ESP_BLE_ENC_KEY_MASK | ESP_BLE_ID_KEY_MASK); //Encryption Keys used to protect data exchange | identity keys to securely identify device
    
    //Start BLE Service
    pService->start();
    //Configure BLE advertising to allow other devices to discover BLE Server
    BLEAdvertising* pAdvertising = BLEDevice::getAdvertising();
    pAdvertising->addServiceUUID(SERVICE_UUID); //add service UUID to the advertising package for clients to discover
    pAdvertising->setScanResponse(true); // scan response behavior
    pAdvertising->setMinPreferred(0x06); //Min preferred connection interval for advertising device
    pAdvertising->setMinPreferred(0x12);

    BLEDevice::startAdvertising(); //start advertising the device for connection
    Serial.println("Device ready"); //print to serial monitor to indicate ESP32 is ready
}

void loop() {
    static uint32_t lastUpdate = 0; //tracks the last time sensor was updated
    
    if (millis() - lastUpdate >= 30000) { // Update 30 second
        lastUpdate = millis();
        Serial.println("Scanning Color");
        // Read sensor data (XYZ values)
        float X = colorSensor.getCIEx();
        float Y = colorSensor.getCIEy();
        // float Z = 1 - X - Y;
        float Z = 1.0f - X - Y;
        
        // Convert to LAB
        float L, a, b;

        // Serial.println("Mearued XYZ Values:" + String(X) + "," + String(Y) + "," + String(Z));

        convertXYZtoLAB(X, Y, Z, &L, &a, &b);
        //String to hold LAB values
        String labData = String(L) + "," + String(a) + "," + String(b);
        
        //if BLE Device is connected, send LAB data to client
        if (pServer->getConnectedCount() > 0) {
          pCharacteristic->setValue(labData.c_str()); //Sets value of the characteristics to LAB data
          pCharacteristic->notify();//Notify connected device that new data is available
          Serial.println("Sent: " + labData); //Logs sent LAB data to the serial monitor 
        }
    }
    //Delay 3 seconds to prevent constant updates 
    delay(600);
}



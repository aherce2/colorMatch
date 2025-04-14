#include "arduino_secrets.h"

#include<Wire.h>
#include "SparkFun_OPT4048.h"

SparkFun_OPT4048 colorSensor;

#define i2C_ADDR 0x44
#define SDA_PIN 4 //blue wire
#define SCL_PIN 5 //yellow wire

byte busStatus;

//I2C found at 0x44
void setup() {
  
  
  Serial.begin(115200);
  delay(10000);
  Wire.begin(SDA_PIN,SCL_PIN);

  Serial.println("ESP32-S3 is running!");
  Serial.println("I2C Scanner starting...");


  for (int i2cAddress = 0x00; i2cAddress < 0x80; i2cAddress++)
  {
    Wire.beginTransmission(i2cAddress);
    busStatus = Wire.endTransmission();
    if (busStatus == 0x00)
    {
      Serial.print("I2C Device found at address: 0x");
      Serial.println(i2cAddress, HEX);
    }
  }

  if (!colorSensor.begin(i2C_ADDR)) {
    Serial.println("OPT4048 not detected. Check wiring!");
    while (1);
  }
  
  colorSensor.setBasicSetup();
  Serial.println("OPT4048 initialized successfully!");
}

void loop() {
  Serial.print("CIEx: ");
  Serial.print(colorSensor.getCIEx());
  Serial.print(" CIEy: ");
  Serial.println(colorSensor.getCIEy());
  
  delay(1000);
}

// void setup()
// {
//   Serial.begin(115200);
//   delay(10000);
//   Wire.begin(SDA_PIN, SCL_PIN);
//   Serial.println("I2C Scanner starting...");


//   for (int i2cAddress = 0x00; i2cAddress < 0x80; i2cAddress++)
//   {
//     Wire.beginTransmission(i2cAddress);
//     busStatus = Wire.endTransmission();
//     if (busStatus == 0x00)
//     {
//       Serial.print("I2C Device found at address: 0x");
//       Serial.println(i2cAddress, HEX);
//     }

//     else
//     {
//       Serial.print("I2C Device not found at address: 0x");
//       Serial.println(i2cAddress, HEX);
//     }
//   }
// }

// void loop()
// {}


#include "DFRobot_PH.h"
#include <EEPROM.h>
#include <ArduinoJson.h>

#define PH_PIN A1
float voltage, phValue;
DFRobot_PH ph;

byte statusLed    = 13;

byte sensorInterrupt = 0;  // 0 = digital pin 2
byte sensorPin       = 2;

const int waterLevelPin = A4;  // Analog input 4
int waterValue = 0; // variable to store the water level sensor value
int waterPercentage = 0; // variable to store the water level percentage

const int thermistorPin = A0;  // Pin for thermistor

// The hall-effect flow sensor outputs approximately 4.5 pulses per second per
// litre/minute of flow.
float calibrationFactor = 11;

volatile byte pulseCount;  

float flowRate;
unsigned int flowMilliLitres;
unsigned long totalMilliLitres;

unsigned long oldTime;

unsigned long waterTimepoint;

void setup()
{
    Serial.begin(115200);  
    ph.begin();

    pinMode(statusLed, OUTPUT);
    digitalWrite(statusLed, HIGH);  // We have an active-low LED attached
  
    pinMode(sensorPin, INPUT);
    digitalWrite(sensorPin, HIGH);

    pinMode(waterLevelPin, INPUT); // Set water level pin as input
    pinMode(thermistorPin, INPUT); // Set thermistor pin as input

    pulseCount        = 0;
    flowRate          = 0.0;
    flowMilliLitres   = 0;
    totalMilliLitres  = 0;
    oldTime           = 0;
    waterTimepoint    = millis(); // Initialize waterTimepoint

    attachInterrupt(sensorInterrupt, pulseCounter, FALLING);
}

void loop()
{
    static unsigned long timepoint = millis();
    if(millis()-timepoint>1000U){                  //time interval: 1s
        timepoint = millis();
        voltage = analogRead(PH_PIN)/1024.0*5000;  // read the voltage
        phValue = ph.readPH(voltage,25);  // convert voltage to pH with temperature compensation

        float tempC = 20.0 + (random(-5, 6) / 10.0); // Generate a random temperature around 20°C

        // Create a JSON document
        StaticJsonDocument<200> doc;
        doc["pH"] = phValue;
        doc["temperature"] = tempC;
        doc["water_level"] = waterPercentage;
        doc["flow_rate"] = flowRate;
        doc["output_liquid_quantity"] = totalMilliLitres;

        // Serialize JSON to a string
        char jsonBuffer[200];
        serializeJson(doc, jsonBuffer);

        // Send JSON string over serial
        Serial.println(jsonBuffer);
    }
    ph.calibration(voltage,25);           // calibration process by Serail CMD

    if(millis()-waterTimepoint>5000U){  // print water level every 5 seconds
        waterValue = analogRead(waterLevelPin); // read the analog value from water level sensor
        waterPercentage = map(waterValue, 0, 1023, 0, 100);  // Convert sensor value to percentage
        waterTimepoint = millis(); // Update waterTimepoint here
    }

    if((millis() - oldTime) > 1000)    // Only process counters once per second
    { 
        detachInterrupt(sensorInterrupt);
        
        flowRate = ((1000.0 / (millis() - oldTime)) * pulseCount) / calibrationFactor;
        
        oldTime = millis();
        
        flowMilliLitres = (flowRate / 60) * 1000;
        
        totalMilliLitres += flowMilliLitres;
      
        pulseCount = 0;
        
        attachInterrupt(sensorInterrupt, pulseCounter, FALLING);
    }
}

void pulseCounter()
{
    pulseCount++;
}

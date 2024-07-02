#include "DFRobot_PH.h"
#include <EEPROM.h>

#define PH_PIN A1
float voltage, phValue;
DFRobot_PH ph;

byte statusLed    = 13;

byte sensorInterrupt = 0;  // 0 = digital pin 2
byte sensorPin       = 2;

// The hall-effect flow sensor outputs approximately 4.5 pulses per second per
// litre/minute of flow.
float calibrationFactor = 11;

volatile byte pulseCount;  

float flowRate;
unsigned int flowMilliLitres;
unsigned long totalMilliLitres;

unsigned long oldTime;

void setup()
{
    Serial.begin(115200);  
    ph.begin();

    pinMode(statusLed, OUTPUT);
    digitalWrite(statusLed, HIGH);  // We have an active-low LED attached
  
    pinMode(sensorPin, INPUT);
    digitalWrite(sensorPin, HIGH);

    pulseCount        = 0;
    flowRate          = 0.0;
    flowMilliLitres   = 0;
    totalMilliLitres  = 0;
    oldTime           = 0;

    attachInterrupt(sensorInterrupt, pulseCounter, FALLING);
}

void loop()
{
    static unsigned long timepoint = millis();
    if(millis()-timepoint>1000U){                  //time interval: 1s
        timepoint = millis();
        voltage = analogRead(PH_PIN)/1024.0*5000;  // read the voltage
        phValue = ph.readPH(voltage,25);  // convert voltage to pH with temperature compensation
        Serial.print("pH: ");
        Serial.print(phValue, 2);
        Serial.println();
    }
    ph.calibration(voltage,25);           // calibration process by Serail CMD

    if((millis() - oldTime) > 1000)    // Only process counters once per second
    { 
        detachInterrupt(sensorInterrupt);
        
        flowRate = ((1000.0 / (millis() - oldTime)) * pulseCount) / calibrationFactor;
        
        oldTime = millis();
        
        flowMilliLitres = (flowRate / 60) * 1000;
        
        totalMilliLitres += flowMilliLitres;
      
        Serial.print("Flow Rate: ");
        Serial.print(int(flowRate));
        Serial.print(" L/min\t");
        Serial.print("Output Liquid Quantity: ");
        Serial.print(totalMilliLitres);
        Serial.print(" mL (");
        Serial.print(totalMilliLitres/1000);
        Serial.println(" L)");
        
        pulseCount = 0;
        
        attachInterrupt(sensorInterrupt, pulseCounter, FALLING);
    }
}

void pulseCounter()
{
    pulseCount++;
}

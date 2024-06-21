void setup() {
  // put your setup code here, to run once:
  serial.begin(9600)
}

void loop() {
  // put your main code here, to run repeatedly:
  float flowSensor = 12.122
  float temperatuurSensor = 2.0
  float waterPeil = 3.5
  float pHWaarde = 66.7

  serial.println(flowSensor)
  serial.println(temperatuurSensor)
  serial.println(waterPeil)
  serial.println(pHWaarde)

  delay(1000)
}

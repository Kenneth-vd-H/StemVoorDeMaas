const int waterLevelPin = A4;  // Analog input 4

int value = 0; // variable to store the sensor value

void setup() {
  Serial.begin(9600);
}

void loop() {
  delay(10);                      // wait 10 milliseconds
  value = analogRead(waterLevelPin); // read the analog value from sensor

  // Convert sensor value to percentage (assuming 0-1023 range)
  int percentage = map(value, 0, 1023, 0, 100);  // Correct mapping

  Serial.print("Water Level: ");
  Serial.print(percentage);
  Serial.println("%");

  delay(1000);
}

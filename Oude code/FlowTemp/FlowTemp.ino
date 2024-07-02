const int thermistorPin = A0;  // Pin for thermistor

void setup() {
  Serial.begin(9600);
}

void loop() {
  float tempC = 20.0 + (random(-5, 6) / 10.0); // Generate a random temperature around 20°C
  Serial.print("Temperature: ");
  Serial.print(tempC);
  Serial.println(" °C");
  delay(1000);
}

#include <TimeLib.h>  // Include the Time library

const int irSensorPin = A0;  // IR sensor connected to analog pin A0
unsigned long previousMillis = 0;
const long interval = 1000;  // Read every second (1000 milliseconds)

void setup() {
  Serial.begin(9600);
  
  // Set the time manually (you can modify the time for your needs)
  setTime(12, 30, 0, 3, 2, 2025);  // Set time to 12:30:00 on February 3, 2025
}

void loop() {
  unsigned long currentMillis = millis();
  
  // Check if it's time to send data
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    
    int sensorValue = analogRead(irSensorPin);  // Read the analog value
    Serial.print("{\"timestamp\": \"");
    Serial.print(getTimeStamp());  // Get timestamp
    Serial.print("\", \"value\": ");
    Serial.print(sensorValue);  // Send the sensor value
    Serial.println("}");
  }
}

String getTimeStamp() {
  char timestamp[20];
  sprintf(timestamp, "%04d-%02d-%02d %02d:%02d:%02d",
          year(), month(), day(), hour(), minute(), second());
  return String(timestamp);
}

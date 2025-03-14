#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <Arduino.h> 

// Analog input pin connected to op-amp output
const int opAmpPin = A4;

// Variables to store baseline voltage and detection parameters
float baselineVoltage = 0.0;
const float threshold = 0.07; // Voltage threshold to detect medication removal 

void setup() {
  Serial.begin(9600);  // Start serial communication for debugging
  delay(2000);         // Allow sensor to stabilize
  
  // Record the initial baseline voltage when setup starts
  baselineVoltage = readVoltage();  // Read the actual initial voltage
 
}

void loop() {
  // Reads current voltage
  float outputVoltage = readVoltage();
  
  // Calculates voltage change from the target baseline (1.4V)
  float voltageChange = baselineVoltage - outputVoltage;

  // Medication Removal Detection
  if (voltageChange > threshold) {
    unsigned long currentTime = millis();

      Serial.println(" Medication taken!");
  }
    
  else {
    Serial.println(" Medication not taken.");
  }

  // Delay to prevent overcrowding of serial monitor
  delay(500);
}

float readVoltage() {
  int raw_value = analogRead(opAmpPin);
  return (raw_value * 5.0) / 1023.0; // Convert ADC value to voltage (0 to 5V)
}

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <Arduino.h>

// define parameters
#define MAX_COMP 15  // 14 compartments for medication, 1 compartment for callibration
#define BUFFER 100  // max length for incoming serial data
#define ANGLE 11  // rotation angle for each compartment

// define pins
// TODO: change pins to match hardware !!!
#define SOUND   9
#define SERVO   10

// create a new datastype to store all Entries in Medication Schedule
typedef struct {
    int compartment;
    char date[11];  // format: YYYY-MM-DD
    char time[6];   // format: HH:MM
    char name[50];  // medication name
    unsigned long reminderTime;  // time (in milliseconds) to take medication
} ScheduleEntry;

// create global variables
ScheduleEntry schedule[MAX_COMP];  // Array to store schedule entries
int entries = 0;
unsigned long startTime = 0;
int timeSet = 0;  // Boolean variable (0 = false, 1 = true)

// initalization 
void setup() {
    pinMode(SOUND, OUTPUT);
    myServo.attach(SERVO);
    
    Serial.begin(9600); 
}

void loop() {
    char input[BUFFER];  // stores incoming serial data from Python script

    // only runs if data is available in buffer
    if (Serial.available()) {
        int index = 0;

        // Read until newline or buffer full
        while (Serial.available() && index < BUFFER - 1) {
            char c = Serial.read();
            if (c == '\n') break;
            input[index++] = c;
        }
        input[index] = '\0';  // TODO: wut is dis ???

        // Variables to store parsed data
        int compartment;
        char date[11], time[6], name[50];

        // Parse received data (Format: "compartment,date,time,medication")
        if (sscanf(input, "%d,%10[^,],%5[^,],%49[^\n]", &compartment, date, time, name) == 4) {
            
            if (compartment == 0) {
                // Compartment 0 is for calibration
                int schH, schM;
                if (sscanf(time, "%d:%d", &schH, &schM) == 2) {
                    startTime = (schH * 3600000UL) + (schM * 60000UL);
                    timeSet = 1;
                    Serial.print("Time calibrated to: ");
                    Serial.println(time);
                }
            } else if (entries < MAX_COMP - 1) {
                // Store the schedule entry
                schedule[entries].compartment = compartment;
                strncpy(schedule[entries].date, date, 10);
                strncpy(schedule[entries].time, time, 5);
                strncpy(schedule[entries].name, name, 29);

                // Convert time to milliseconds for trigger time
                int schH, schM;
                if (sscanf(time, "%d:%d", &schH, &schM) == 2) {
                    schedule[entries].reminderTime = (schH * 3600000UL) + (schM * 60000UL);
                }

                Serial.print("Stored: ");
                Serial.print(compartment);
                Serial.print(", ");
                Serial.print(date);
                Serial.print(", ");
                Serial.print(time);
                Serial.print(", ");
                Serial.println(name);

                entries++;
            }
        }
    }

    // Check if it's time for any medication
    if (timeSet == 1) {
        unsigned long timePast = millis() - startTime;

        for (int i = 0; i < entries; i++) {
            if (timePast >= schedule[i].reminderTime) {
                Serial.print("nice message reminder :) ");
                digitalWrite(SOUND, HIGH);
                delay(10000);  // play sound for 10 seconds
                digitalWrite(SOUND, LOW);
                delay (20000); // wait for 20 seconds
                digitalWrite(SOUND, HIGH);
                delay(10000);  // play sound for 10 seconds
                digitalWrite(SOUND, LOW);
                delay (20000); // wait for 20 seconds

                int rotation = ANGLE * schedule[i].compartment; //compartments evenly spaced
                Serial.print("Rotate to compartment: ");
                Serial.println(scheduel[i].compartment);
                servo.write(rotation);
                delay(300000);  // TODO fix this delay
                servo.write(0);  // reset servo

            
            }
        }
    }
}


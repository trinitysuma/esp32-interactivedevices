// adopted from WebSerial Lab 1

#include <Arduino.h>

int threshold = 40;

// Track current touch state for each pad
bool touchState[6] = {false, false, false, false, false, false};
uint8_t touchPins[6] = {T2, T3, T4, T5, T7, T8};
const char* padNames[6] = {"yelena", "bucky", "redguardian", "ghost", "walker", "team"};

void setup() {
  Serial.begin(115200);
  delay(1000);
}

void loop() {
  for(int i=0; i<6; i++) { // check each pin
    uint16_t val = touchRead(touchPins[i]); // read value
    bool pressed = val < threshold;

    if(pressed) {
      // pad is held, send current pressure
      Serial.print(padNames[i]);
      Serial.print(":");
      Serial.println(val);
    } 
    else if(touchState[i]) {
      // pad was released
      Serial.print("STOP_");
      Serial.println(padNames[i]);
    }

    touchState[i] = pressed;
  }
  delay(20); // adjust for faster/slower updates
}
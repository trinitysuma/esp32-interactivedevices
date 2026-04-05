# esp32-interactivedevices
Module 3 of Creative Embedded Systems

This project uses PlatformIO to send and process serial signals to/from an ESP32.

## Materials
* ESP32
* Wired connection (e.g., to laptop)
* Copper tape
* Wire
* Soldering iron
* Choice of base (e.g., acrylic)

## Implementation
This code is adapted from COMS3930 WebSerial Lab 1, which used serial pin values to produce different audio effects.  This code, instead, plays local audio files, using the serial values to indicate pressure. `audio.py` uses the pygame library to process local files.  It also processes the serial messages, triggering the correct song(s) and volume(s).  It uses a threshold to identify a double-tap -- a setting change.  

This can currently only be implemented with a wired connection to a device with speakers!

Read more about the piece here: https://sites.google.com/view/trinitysuma/portfolio/creative-embedded-systems#h.yis0njmb5446

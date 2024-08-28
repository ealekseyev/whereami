/*
 *  This sketch demonstrates how to scan WiFi networks.
 *  The API is based on the Arduino WiFi Shield library, but has significant changes as newer WiFi functions are supported.
 *  E.g. the return value of `encryptionType()` different because more modern encryption is supported.
 */
#include "WiFi.h"

void setup() {
    Serial.begin(115200);

    // Set WiFi to station mode and disconnect from an AP if it was previously connected.
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();
    delay(100);
}

void loop() {
    // WiFi.scanNetworks will return the number of networks found.
    int n = WiFi.scanNetworks();
    if (n == 0) {
    } else {
      Serial.write(0); Serial.write(0);
        for (int i = 0; i < n; ++i) {
            uint8_t* b = WiFi.BSSID(i);
            for(int i = 0; i < 6; i++) {
              Serial.write(b[i]);
            }
            int x = WiFi.RSSI(i);
            if(x > 0) {
              x = 0;
            } else if(x < -100) {
              x = -100;
            }
            Serial.write(map(x, -100, 0, 0, 255));
        }
    }
    Serial.write(0); Serial.write(0);
    // Delete the scan result to free memory for code below.
    WiFi.scanDelete();

    // Wait a bit before scanning again.
    while(Serial.available() == 0);
    while(Serial.available() != 0) {
      Serial.read();
    }
}

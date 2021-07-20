#include <SoftwareSerial.h>
SoftwareSerial ESP8266(2, 3); //RX, TX


void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  // put your setup code here, to run once:
  Serial.begin(9600);
  ESP8266.begin(9600);
  delay(5000);
}

void loop() {
  // put your main code here, to run repeatedly:
  String income = "";
  bool readFromESP8266 = false;
  while (ESP8266.available()) {
    income = ESP8266.readString();
    readFromESP8266 = true;
  }

  if (readFromESP8266) {
    Serial.println("Get String : " + income);
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(1000);                       // wait for a second
    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
    delay(1000);  
  }
}

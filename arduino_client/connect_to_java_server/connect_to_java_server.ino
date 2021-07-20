#include <ESP8266WiFi.h>
 
//
const int tx = 1;
const int rx = 0;
const char* ssid = "TP-Link_B6CC";
const char* password = "18641851";
 
// Socket Server
const char* host = "192.168.11.116";
const int port = 1278;
 
int i = 0;
char initJSON[] = "{\"component\":\"arduino\"}";

WiFiClient client;
 
void setup() {
  pinMode(2, OUTPUT);
  pinMode(rx,INPUT_PULLUP); 
  pinMode(tx,INPUT_PULLUP); 
  Serial.begin(9600);
  Serial.print( "Start..." );
 
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  delay(500);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println(".");
  }

  client.connect(host, port);
  client.println(initJSON);
}
 
void loop() {
 
  if (!client.connected()) {
    
  }
  /*
  String Control = client.readStringUntil('\n');
  Serial.println(Control);
  */
  Serial.write("light led");
  digitalWrite(2, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);              // wait for a second
  digitalWrite(2, LOW);    // turn the LED off by making the voltage LOW
  delay(1000); 
  delay(2000);
}

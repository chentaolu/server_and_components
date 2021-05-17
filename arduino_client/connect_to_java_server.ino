#include <ESP8266WiFi.h>
 
//
const int tx = 1;
const int rx = 0;
const char* ssid = "dlink";
const char* password = "7b27b27b27b27";
 
// Socket Server
const char* host = "192.168.11.112";
const int port = 5678;
 
int i = 0;
 
WiFiClient client;
 
void setup() {
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
}
 
void loop() {
 
  if (!client.connected()) {
    client.connect(host, port);
    client.println("connected...");
  }
 
  String Control = client.readStringUntil('\n');
  Serial.println(Control);
  
  delay(1000);
}

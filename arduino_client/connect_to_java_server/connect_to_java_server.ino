#include <ESP8266WiFi.h>
 
//
const int tx = 1;
const int rx = 0;
const char* ssid = "ASUS";
const char* password = "dodo890130";
 
// Socket Server
const char* host = "192.168.1.102";
const int port = 5678;
 
int i = 0;
char initJSON[] = "{\"component\":\"arduino\"}";

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

  client.connect(host, port);
  client.println(initJSON);
}
 
void loop() {
 
  if (!client.connected()) {
    
  }
 
  String Control = client.readStringUntil('\n');
  Serial.println(Control);
  Serial.println("");
  delay(1000);
}

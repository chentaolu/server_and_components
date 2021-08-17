#include <ESP8266WiFi.h>
 
//
const int tx = 1;
const int rx = 0;
/*
const char* ssid = "TP-Link_B6CC";
const char* password = "18641851";
*/
const char* ssid = "ASUS";
const char* password = "dodo890130";
// Socket Server
const char* host = "192.168.1.102";
const int port = 1278;
 
int i = 0;
char initJSON[] = "{\"component\":\"centerArduino\"}";

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
  if(client.connect(host, port))
  Serial.println("SUCCESS CONNECT");
  else
  Serial.println("FAIL CONNECT");
  
  client.println(initJSON);
}
 
void loop() {
  String income ="";
  if (!client.connected()) {
    reconnect();
  }
  if(client.available())
  {
    income=client.readStringUntil('\n');
    Serial.println(income);
  }
  //Serial.println("XX");
  delay(1000);              // wait for a second
}

void reconnect()
{
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println(".");
    }
    if(client.connect(host, port))
    Serial.println("SUCCESS CONNECT");
    else
    Serial.println("FAIL CONNECT"); 
    client.println(initJSON);
}

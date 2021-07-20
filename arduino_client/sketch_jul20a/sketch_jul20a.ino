#include <ESP8266WiFi.h>
#include <ArduinoJson.h> 
#include <Unistep2.h>
//
const int tx = 1;
const int rx = 0;
const char* ssid = "ASUS";
const char* password = "dodo890130";
 
// Socket Server
const char* host = "192.168.1.102";
const int port = 5678;
 
int i = 0;
Unistep2 stepper2(2, 3, 4, 5, 4096, 630);// IN1, IN2, IN3, IN4, 總step數, 每步的延遲(in micros) 
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
  /*while (!client.connected()) {
    client.connect(host, port);
    println()
  }*/
  stepper2.move(3000); 
}
 
void loop() {
  Serial.println("gogo");
 //Serial.println("QQ");
  /*String Control = client.readStringUntil('\n');
  Serial.println(Control);*/
  // stepper2.move(3000);                        //跟COUNT 差17           
  if(stepper2.stepsToGo() != 0)
  {     
    stepper2.run();  
  }
  delay(100);
}

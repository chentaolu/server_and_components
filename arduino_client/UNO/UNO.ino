#include <SoftwareSerial.h>
#include <Unistep2.h>
SoftwareSerial ESP8266(14, 15); //RX, TX   (ESP8266 TX to 14 ,RX to 15)
#include <ArduinoJson.h>

// Arduino component setting    
Unistep2 Parallel(4, 5, 6, 7, 2048, 630);// IN1, IN2, IN3, IN4, 總step數, 每步的延遲(in micros)
Unistep2 Vertical(8, 11, 12, 13, 2048, 630);// 注意腳位
word FANPIN = 3;           
const int SPARYPIN = 10;    

int FanSpeed = 0;   //Speed Range 0~100
int WaterSpary = 0;  
int input_parallel_location = 0;
int input_vertical_location = 0;
int parallel_location=0;
int vertical_location=0;

void setup() {
  Serial.begin(9600);
  ESP8266.begin(9600);
  
  pinMode(FANPIN, OUTPUT); 
  pinMode(SPARYPIN, OUTPUT);
  
  pwm25kHzBegin();
  Initialization();
  delay(5000);                            
}

void loop() {
  String income ="";
  bool readFromESP8266 = false;
  if (ESP8266.available()) {                  //read string
    income = ESP8266.readString();
    readFromESP8266 = true;
  }
  if (readFromESP8266) {                        
    Serial.println(income);
    StringProcessing(income);
  }
  //StringProcessing(income);
  //Serial.println(input_parallel_location);
  MoveControl();
  FanControl();
  //Spary();
  Parallel.run();  
  Vertical.run();
}

void Initialization(){                        //移動2公分
  Parallel.move(2340);
  Vertical.move(2340);
  while(Parallel.stepsToGo() != 0 || Vertical.stepsToGo() != 0)
  {   
      Parallel.run();  
      Vertical.run();  
  }
}

void StringProcessing(String input)
{
  DynamicJsonDocument json_doc(1024) ;
  DeserializationError json_error;
  int str_length =  input.length()+1;
  char json_intput[str_length];
  int fspd;
  int par;
  int ver;
  int wspy;
  input.toCharArray(json_intput, str_length);
  json_error = deserializeJson(json_doc, json_intput);
  ver = json_doc["verticalMove"];
  wspy = json_doc["waterSpary"];
  par = json_doc["parallelMove"];
  fspd = json_doc["fanSpeed"];

  if(fspd != -1) FanSpeed = int((fspd-1)/1.25);
  if(par != -1)  input_parallel_location = par;
  if(ver != -1) input_vertical_location = ver;
  if(wspy != -1) WaterSpary = wspy;
  
}

void MoveControl()          //range 0~?
{
  Parallel.move(Parallel.stepsToGo() + (parallel_location - input_parallel_location)*117); 
  parallel_location = input_parallel_location;
  Vertical.move(Vertical.stepsToGo() + (vertical_location- input_vertical_location)*117); 
  vertical_location = input_vertical_location;

}

void FanControl(){                          
  Serial.println(FanSpeed);
  pwmDuty(FanSpeed);
}

void Spary(){
  
}
void pwm25kHzBegin() {
  TCCR2A = 0;                               // TC2 Control Register A
  TCCR2B = 0;                               // TC2 Control Register B
  TIMSK2 = 0;                               // TC2 Interrupt Mask Register
  TIFR2 = 0;                                // TC2 Interrupt Flag Register
  TCCR2A |= (1 << COM2B1) | (1 << WGM21) | (1 << WGM20);  // OC2B cleared/set on match when up/down counting, fast PWM
  TCCR2B |= (1 << WGM22) | (1 << CS21);     // prescaler 8
  OCR2A = 79;                               // TOP overflow value (Hz)   original 79
  OCR2B = 0;
}

void pwmDuty(byte ocrb) {
  OCR2B = ocrb;                             // PWM Width (duty)
}

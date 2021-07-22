#include <SoftwareSerial.h>
#include <Unistep2.h>
SoftwareSerial ESP8266(2, 3); //RX, TX

// Arduino component setting    
Unistep2 Parallel(4, 5, 6, 7, 2048, 630);// IN1, IN2, IN3, IN4, 總step數, 每步的延遲(in micros)
Unistep2 Vertical(8, 11, 12, 13, 2048, 630);// 注意腳位
const int FANPIN = 9;
const int SPARYPIN = 10;    //噴水 PIN

int FanSpeed = 0;   //Speed Range 0~255
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
    StringProcessing(income);
  }
    
  FanControl();
  MoveControl();
  Parallel.run();  
  Vertical.run();  
  //analogWrite(fan,fan_speed);
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

void StringProcessing(String input)    //字串處理    format:???
{
  int num;
  int fspd, wspy ;
  int par, ver ;
  for (int i = 0; i < input.length(); i++)
  {
    if (input.substring(i, i+7) == "fspeed:")                  //風速  fspeed:XXX
    {
      fspd = input.substring(i+7, i+10).toInt();
      FanSpeed = fspd; 
    }
    if (input.substring(i, i+9) == "parallel:")
    {
      par = input.substring(i+9, i+11).toInt();
      input_parallel_location = par;
    }
    if (input.substring(i, i+9) == "vertical:")
    {
      ver = input.substring(i+9, i+11).toInt();
      input_vertical_location = ver; 
    }
    if(input.substring(i, i+7) == "wspary:")            //噴水  wspary: 0 or 1             
    {
      wspy = input.substring(i+7, i+8).toInt();
      WaterSpary = wspy;
    }    
  }                              
}

void MoveControl()          //range 0~?
{
  Parallel.move(Parallel.stepsToGo() + (parallel_location - input_parallel_location)*117); 
  parallel_location = input_parallel_location;
  Vertical.move(Vertical.stepsToGo() + (vertical_location- input_vertical_location)*117); 
  vertical_location = input_vertical_location;
}

void FanControl(){
  analogWrite(FANPIN,FanSpeed);
}

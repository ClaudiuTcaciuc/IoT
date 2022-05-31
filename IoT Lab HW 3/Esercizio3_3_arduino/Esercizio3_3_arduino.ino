#include <Bridge.h>
#include <BridgeServer.h>
#include <BridgeClient.h>
#include <Process.h>

Process p;
const int INT_LED_PIN = 13;
const int B = 4275;
const int long R0 = 100000;
const int Vcc = 1023;
const float T0 = 298.15;

float convertTension (float sensorVal) {
  float R = ((Vcc / sensorVal) - 1.0) * R0;
  float T = 1 / (log(R / R0) / B + 1 / T0) - 273.15;
  return T;
}

void setup() {
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Serial initialized!");

  pinMode(INT_LED_PIN, OUTPUT);
  digitalWrite(INT_LED_PIN, LOW);
  Bridge.begin();
  digitalWrite(INT_LED_PIN, HIGH);
  Serial.println("Bridge initialized!");

  p.begin("python3");
  p.addParameter("/root/Esercitazione3_3.py");
  p.runAsynchronously();
}

void loop() {
  float sensorVal = analogRead(A1);
  float tempValue = convertTension (sensorVal);
  String msg = "T:"+String(tempValue);
  p.println(msg);
  
  Serial.print("Send command: ");
  Serial.println(msg);

  while(p.available() > 0){
    char c = p.read();
    p.read();
    int num = p.read()-'0';
    if(c == 'L'){
      Serial.print("Led set to: ");
      Serial.println(num);
      digitalWrite(INT_LED_PIN, num);
    }
    else if (c == 'E'){
      Serial.print("Error number: ");
      Serial.println(num);
    }
  }
  delay(10000);
}

#include <Bridge.h>
#include <BridgeServer.h>
#include <BridgeClient.h>

BridgeServer server;
const int B = 4275;
const int long R0 = 100000;
const int Vcc = 1023;
const float T0 = 298.15;

float convertTension (float sensorVal) {
  float R = ((Vcc / sensorVal) - 1.0) * R0;
  float T = 1 / (log(R / R0) / B + 1 / T0) - 273.15;
  return T;
}

void printResponse(BridgeClient client, int code, String body) {
  client.println("Status: " + String(code));
  if (code == 200) {
    client.println(F("Content-type: application/json; charset=utf-8"));
    client.println();
    client.println(body);
  }
  if (code == 400) {
    client.println(F("BAD REQUEST"));
    client.println();
  }
}

void process(BridgeClient client) {
  String command = client.readStringUntil('/');
  Serial.print("Command: ");
  command.trim();
  Serial.println(command);

  if (command == "led")
    setLight(client);
  else if (command == "temperature")
    readTemp(client);
  else
    printResponse(client, 400, senMlEncode(F(""), 0, F("")));
}
String senMlEncode (String command, float value, String a) {
  String s1 = "{";
  String s2 = "\"bn\"";
  String s3 = ":";
  String s4 = "\"Yun\"";
  String s5 = ",";
  String s6 = "\"e\"";
  String s7 = ":[{";
  String s8 = "\"n\"";
  String s9 = "\""+ command+"\"";
  String s10 = "\"t\"";
  String s11 = String(millis());
  String s12 = "\"v\"";
  String s13 = String(value);
  String s14 = "\"u\"";
  String s15 = "\""+a+"\"";
  String s16 = "}]}";
  return s1+s2+s3+s4+s5+s6+s7+s8+s3+s9+s5+s10+s3+s11+s5+s12+s3+s13+s5+s14+s3+s15+s16;
}


void setLight(BridgeClient client) {
  int value = client.parseInt();
  digitalWrite(13, value);
  printResponse(client, 200, senMlEncode(F("led"), value, F("")));
}

void readTemp(BridgeClient client) {
  float sensorVal = analogRead(A1);
  float value = convertTension (sensorVal);
  Serial.print("Temperature value: ");
  Serial.println(value);
  printResponse(client, 200, senMlEncode(F("temperature"), value, F("Cel")));
}

void setup() {
  pinMode(13, OUTPUT); //RLED_PIN = 13
  pinMode(A1, INPUT); //TEMP_PIN = A1
  Bridge.begin();

  server.listenOnLocalhost();
  server.begin();
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Lab HW es 3.1 Starting");
}

void loop() {
  BridgeClient client = server.accept();
  if (client) {
    process(client);
    client.stop();
  }
  delay(50);
}

const int TEMP_PIN = A1;
const int B = 4275;
const int long R0 = 100000;
const int Vcc = 1023;
const float T0 = 298.15;
void setup() {
  // put your setup code here, to run once:
  pinMode(TEMP_PIN, INPUT);
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Lab 1.5 Starting");
}

void convertTension (float sensorVal) {
  float R = ((Vcc / sensorVal) - 1.0) * R0;
  float T = 1 / (log(R / R0) / B + 1 / T0) - 273.15;
  Serial.print("Temperatura: ");
  Serial.println(T);
  delay(1e4);
}

void loop() {
  // put your main code here, to run repeatedly:
  float sensorVal = analogRead(TEMP_PIN);
  convertTension (sensorVal);
}

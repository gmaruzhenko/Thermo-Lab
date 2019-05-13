float voltageToTemp(float v);
void readPins();
void controlHeat();
float temp0 = 0.0, temp1 = 0.0, temp2 = 0.0, temp3 = 0.0, temp4 = 0.0;
//variables used for the feedback loop of the heating element
#define HEATINGPIN 11 //The pin used to digitally control the heating source.
unsigned long time_ref = 0;
unsigned long timeOn = 10000; //in ms
unsigned long timeOff = 10000; //in ms
boolean heating = true;
void setup() {
  Serial.begin(9600);
  //  pinMode(A0, INPUT);
  //  pinMode(A1, INPUT);
  //  pinMode(A2, INPUT);
  //  pinMode(A3, INPUT);
  //  pinMode(A4, INPUT);
  pinMode(HEATINGPIN, OUTPUT);
  digitalWrite(HEATINGPIN, HIGH);
}
void loop() {
  readPins();
  controlHeat();
  delay(1000);
}
void readPins() {
  temp0 = voltageToTemp(analogRead(A0) * 5.0 / 1024.0);
  temp1 = voltageToTemp(analogRead(A1) * 5.0 / 1024.0);
  temp2 = voltageToTemp(analogRead(A2) * 5.0 / 1024.0);
  temp3 = voltageToTemp(analogRead(A3) * 5.0 / 1024.0);
  temp4 = voltageToTemp(analogRead(A4) * 5.0 / 1024.0);
  Serial.print(temp0);
  Serial.print(',');
  Serial.print(temp1);
  Serial.print(',');
  Serial.print(temp2);
  Serial.print(',');
  Serial.print(temp3);
  Serial.print(',');
  Serial.println(temp4);
}
void controlHeat() {
  if (millis() - time_ref > timeOn && heating == true) {
    time_ref = millis();
    heating = false;
    digitalWrite(HEATINGPIN, LOW);
  }
  else if (millis() - time_ref  > timeOff && heating == false) {
    time_ref = millis();
    heating = true;
    digitalWrite(HEATINGPIN, HIGH);
  }
}
float voltageToTemp(float v) {
  return 100.0 * (v - 0.75) + 25.0;
}

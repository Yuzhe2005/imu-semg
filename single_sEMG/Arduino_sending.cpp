const int EMG_PIN0 = A0;
const int EMG_PIN1 = A1;
const int EMG_PIN2 = A2;
const int EMG_PIN3 = A3;
unsigned long t_prev = 0;
const unsigned long interval_us = 1000;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(1000000);
  while(!Serial) {}
}

void loop() {
  // put your main code here, to run repeatedly:
  unsigned long t = micros();
  if (t - t_prev >= interval_us) {
    t_prev = t;
    int a_0 = analogRead(EMG_PIN0);
    int a_1 = analogRead(EMG_PIN1);
    int a_2 = analogRead(EMG_PIN2);
    int a_3 = analogRead(EMG_PIN3);
    Serial.print(a_0);
    Serial.print(',');
    Serial.print(a_1);
    Serial.print(',');
    Serial.print(a_2);
    Serial.print(',');
    Serial.println(a_3);
  }
}

const int EMG_PIN0 = A0;
const int EMG_PIN1 = A1;
const int EMG_PIN2 = A2;
const int EMG_PIN3 = A3;
unsigned long t_prev = 0;
const unsigned long interval_us = 700;

struct pac {
  float a_0;
  float a_1;
  float a_2;
  float a_3;
};

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

    pac packet;
    packet.a_0 = a_0;
    packet.a_1 = a_1;
    packet.a_2 = a_2;
    packet.a_3 = a_3;

    Serial.write((uint8_t*)&packet, sizeof(packet));
  }
}

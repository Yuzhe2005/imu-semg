#include <Wire.h>
#include <Adafruit_LSM6DSOX.h>

#define DRDY_PIN 2

// ——— CONFIG ——————————————————————————————————————————————————————————————
static const uint8_t TCA9548A_ADDR = 0x70;  // I²C address of TCA9548A MUX
static const uint8_t MUX_CHANNEL     = 0;   // Using channel 0 on the MUX
static const int     INT1_PIN        = 2;   // Arduino Due pin wired to LSM6DSOX INT1
static int32_t cnt = 0;

struct SixAxis {
  float ax;
  float ay;
  float az;
  float gx;
  float gy;
  float gz;
};


// IMU object
Adafruit_LSM6DSOX sox = Adafruit_LSM6DSOX();

void selectMuxChannel(uint8_t channel) {
  Wire.beginTransmission(TCA9548A_ADDR);
  Wire.write(1 << channel);
  Wire.endTransmission();
}

void setup() {
  //Initialize SerialUSB at 2 000 000 baud
  SerialUSB.begin(2000000);
  while (!SerialUSB) {}

  //Initialize I²C on SDA1/SCL1 at 1 MHz
  Wire.begin();             
  Wire.setClock(1000000UL); // 1 MHz

  //Select MUX channel so the IMU is on I²C
  selectMuxChannel(MUX_CHANNEL);

  //Initialize the LSM6DSOX over I²C
  if (!sox.begin_I2C()) {
    // If the IMU isn’t found, stay here and print an error
    while (1) {
      SerialUSB.println("ERROR: LSM6DSOX not found on MUX channel 0");
      delay(500);
    }
  }

  //Configure accelerometer → 1.66 kHz, ±2 g
  sox.setAccelDataRate(LSM6DS_RATE_1_66K_HZ);
  sox.setAccelRange(LSM6DS_ACCEL_RANGE_2_G);

  //Configure gyroscope → 1.66 kHz, ±250 dps
  sox.setGyroDataRate(LSM6DS_RATE_1_66K_HZ);
  sox.setGyroRange(LSM6DS_GYRO_RANGE_250_DPS);

  pinMode(DRDY_PIN, INPUT);
  sox.configInt1(
    false,  // tmep
    true,   // gyro
    true,   // acc
    false,  // FIFO
    false   // tap
  );
}

void loop() {
  if (digitalRead(DRDY_PIN)) {

  sensors_event_t accel, gyro, temp;
  sox.getEvent(&accel, &gyro, &temp);

  // Pack into a struct
  SixAxis packet;
  packet.ax = accel.acceleration.x;
  packet.ay = accel.acceleration.y;
  packet.az = accel.acceleration.z;
  packet.gx = gyro.gyro.x;
  packet.gy = gyro.gyro.y;
  packet.gz = gyro.gyro.z;

  // Send raw bytes (24 bytes total)
  SerialUSB.write((uint8_t*)&packet, sizeof(packet));
  }
}


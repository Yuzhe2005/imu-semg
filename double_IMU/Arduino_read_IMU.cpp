#include <Wire.h>
#include <Adafruit_LSM6DSOX.h>

#define DRDY_PIN 2

// ——— CONFIG ——————————————————————————————————————————————————————————————
static const uint8_t TCA9548A_ADDR = 0x70;  // I²C address of TCA9548A MUX
static const uint8_t MUX_CH0       = 0;     // MUX channel for IMU #1
static const uint8_t MUX_CH7       = 7;     // MUX channel for IMU #2
static const int     INT1_PIN      = 2;     // Arduino Due pin wired to both IMU INT1 lines (they can share)

// Data‐packet for one 6-axis IMU (24 bytes total: 6 floats × 4 bytes each)
struct SixAxis {
  float ax;
  float ay;
  float az;
  float gx;
  float gy;
  float gz;
};

// Two sensor objects, one per channel
Adafruit_LSM6DSOX sox0 = Adafruit_LSM6DSOX();  // IMU on channel 0
Adafruit_LSM6DSOX sox7 = Adafruit_LSM6DSOX();  // IMU on channel 7

// Helper: select a single channel on the TCA9548A
void selectMuxChannel(uint8_t channel) {
  Wire.beginTransmission(TCA9548A_ADDR);
  Wire.write(1 << channel);
  Wire.endTransmission();
}

void setup() {
  // Initialize SerialUSB at 2 000 000 baud
  SerialUSB.begin(2000000);
  while (!SerialUSB) {}

  // Initialize I²C on SDA1/SCL1 at 1 MHz
  Wire.begin();
  Wire.setClock(1000000UL);

  pinMode(DRDY_PIN, INPUT);

  // ——— Initialize IMU #1 (channel 0) —————————————————————————————————
  selectMuxChannel(MUX_CH0);
  if (!sox0.begin_I2C()) {
    // If IMU #1 isn't found, halt and emit error
    while (1) {
      SerialUSB.println("ERROR: LSM6DSOX not found on MUX channel 0");
      delay(500);
    }
  }
  // Configure IMU #1: accel 1.66 kHz ±2 g, gyro 1.66 kHz ±250 dps
  sox0.setAccelDataRate(LSM6DS_RATE_1_66K_HZ);
  sox0.setAccelRange(LSM6DS_ACCEL_RANGE_2_G);
  sox0.setGyroDataRate(LSM6DS_RATE_1_66K_HZ);
  sox0.setGyroRange(LSM6DS_GYRO_RANGE_250_DPS);
  // Only route accel+gyro to INT1 (FIFO and tap disabled)
  sox0.configInt1(false, true, true, false, false);

  // ——— Initialize IMU #2 (channel 7) —————————————————————————————————
  selectMuxChannel(MUX_CH7);
  if (!sox7.begin_I2C()) {
    // If IMU #2 isn't found, halt and emit error
    while (1) {
      SerialUSB.println("ERROR: LSM6DSOX not found on MUX channel 7");
      delay(500);
    }
  }
  // Configure IMU #2: same data rates/ranges as IMU #1
  sox7.setAccelDataRate(LSM6DS_RATE_1_66K_HZ);
  sox7.setAccelRange(LSM6DS_ACCEL_RANGE_2_G);
  sox7.setGyroDataRate(LSM6DS_RATE_1_66K_HZ);
  sox7.setGyroRange(LSM6DS_GYRO_RANGE_250_DPS);
  sox7.configInt1(false, true, true, false, false);
}

void loop() {
  // Only proceed if at least one IMU has data ready (shared INT1_PIN)
  // if (digitalRead(DRDY_PIN)) {
    // ——— Read from IMU #1 (channel 0) —————————————————————————————————————
    selectMuxChannel(MUX_CH0);
    sensors_event_t accel0, gyro0, temp0;
    sox0.getEvent(&accel0, &gyro0, &temp0);

    SixAxis packet0;
    packet0.ax = accel0.acceleration.x;
    packet0.ay = accel0.acceleration.y;
    packet0.az = accel0.acceleration.z;
    packet0.gx = gyro0.gyro.x;
    packet0.gy = gyro0.gyro.y;
    packet0.gz = gyro0.gyro.z;

     //Now 中断 only connect MUX_CH0

    // ——— Read from IMU #2 (channel 7) —————————————————————————————————————
    selectMuxChannel(MUX_CH7);
    sensors_event_t accel7, gyro7, temp7;
    sox7.getEvent(&accel7, &gyro7, &temp7);

    SixAxis packet7;
    packet7.ax = accel7.acceleration.x;
    packet7.ay = accel7.acceleration.y;
    packet7.az = accel7.acceleration.z;
    packet7.gx = gyro7.gyro.x;
    packet7.gy = gyro7.gyro.y;
    packet7.gz = gyro7.gyro.z;

    // ——— Transmit both 6-axis packets (48 bytes total) ——————————————————————
    SerialUSB.write((uint8_t*)&packet0, sizeof(packet0));  // 24 bytes
    SerialUSB.write((uint8_t*)&packet7, sizeof(packet7));  // 24 bytes
    // delay(5000);
  // }
}

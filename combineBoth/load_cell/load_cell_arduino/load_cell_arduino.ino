#include "HX711.h"

// HX711 接线定义
const int DOUT_PIN = 2;   // DT 引脚
const int SCK_PIN  = 3;   // SCK 引脚

HX711 scale;

void setup() {
  // 使用 USB-C 串口，波特率 115200
  Serial.begin(115200);
  // 初始化 HX711
  scale.begin(DOUT_PIN, SCK_PIN);
  // 设置校准因子（根据实际校准结果调整）
  scale.set_scale(42275.0f);
  // 去皮（把当前值置零）
  scale.tare();

  Serial.println("HX711 Ready on R4 WiFi");
}

void loop() {
    // 获取 10 次平均值
    float weight = scale.get_units(1);
    // weight /= 47.5;
    // weight *= 2.5;
    Serial.println(weight);
}

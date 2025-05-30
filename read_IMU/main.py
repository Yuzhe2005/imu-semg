from IMU_sensor import IMUReader
from IMU_plotter import RealTimePlotter

def main():
    PORT    = 'COM16'    # ← 根据设备管理器实际端口修改
    BAUD    = 921600     # ← 与 Arduino 代码里 SerialUSB.begin(...) 保持一致
    WINDOW  = 1000       # ← 滑动窗口大小
    YLIM    = None       # ← None 表示自动缩放，或 (-5000,5000) 固定范围
    INTERVAL= 20         # ← 20 ms → ~50 FPS
    BLIT    = True       # ← 更流畅

    imu = IMUReader(PORT, baudrate=BAUD, maxlen=WINDOW)
    try:
        plotter = RealTimePlotter(
            reader=imu,
            maxlen=WINDOW,
            y_limits=YLIM,
            interval=INTERVAL,
            blit=BLIT
        )
        plotter.animate()
    finally:
        imu.stop()

if __name__ == '__main__':
    main()

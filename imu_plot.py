import serial, struct, csv, time
import numpy as np
import matplotlib.pyplot as plt

# ① 改成你的实际端口号：Windows 如 COM5，macOS/Linux 如 /dev/ttyACM0
PORT = "COM16"
BAUD = 921600               # 与 Arduino 端一致

FRAME = struct.Struct("<hhhhhh")   # 小端 6×int16 = 12 字节

# 打开串口
ser = serial.Serial(PORT, BAUD, timeout=1)

# 滚动窗口：显示最近 ~0.5 秒的 X 轴加速度
win_size = 800                         # 1660 Hz ≈ 800 点/0.48 s
buf = np.zeros(win_size)

fig, ax = plt.subplots()
ln, = ax.plot(buf)
ax.set_ylim(-20000, 20000)             # 依据量程调上下限
ax.set_title("LSM6DSOX ax (rolling)")  # 窗口标题

# 同时备份到 CSV
csv_file = open(f"imu_{int(time.time())}.csv", "w", newline="")
writer = csv.writer(csv_file)
writer.writerow(["t", "ax", "ay", "az", "gx", "gy", "gz"])
t0 = time.time()

print("开始接收… 关闭图窗可退出")
while plt.fignum_exists(fig.number):   # 图窗存在则循环
    raw = ser.read(FRAME.size)         # 读满 12 B
    if len(raw) != FRAME.size:
        continue                       # 超时就丢
    ax_, ay_, az_, gx_, gy_, gz_ = FRAME.unpack(raw)
    writer.writerow([time.time() - t0, ax_, ay_, az_, gx_, gy_, gz_])

    # 更新滚动曲线
    buf = np.roll(buf, -1)
    buf[-1] = ax_
    ln.set_ydata(buf)
    plt.pause(0.001)

print("已退出, CSV 保存在脚本同目录")

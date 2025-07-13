import tkinter as tk
from tkinter import messagebox
import serial
import threading

# 配置区：请根据实际串口号修改
PORT      = 'COM27'      # 示例 Windows 路径
BAUD_RATE = 115200

def serial_reader(ser, weight_var):
    """后台线程：不断从串口读数并更新 weight_var"""
    while True:
        try:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if not line:
                continue
            parts = line.split()
            try:
                value = float(parts[0])
                unit  = parts[1] if len(parts) > 1 else ''
                weight_var.set(f"{value:.3f} {unit}")
            except:
                weight_var.set(f"无法解析: {line}")
        except serial.SerialException:
            weight_var.set("串口已关闭")
            break

def start_serial_thread(weight_var):
    """打开串口并起线程读取数据"""
    try:
        ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
    except serial.SerialException as e:
        messagebox.showerror("错误", f"无法打开串口 {PORT}:\n{e}")
        return
    t = threading.Thread(target=serial_reader, args=(ser, weight_var), daemon=True)
    t.start()

def countdown(count, timer_var):
    """每秒更新一次 timer_var 直至 0"""
    if count >= 0:
        timer_var.set(f"{count} s")
        root.after(1000, countdown, count-1, timer_var)
    else:
        timer_var.set("Done")

def restart_countdown(event=None):
    """按空格重启倒计时"""
    countdown(10, timer_var)

# 主程序
root = tk.Tk()
root.title("Load Cell + Countdown")
root.geometry("360x160")

# 实时重量
weight_var = tk.StringVar(value="Waiting for data...")
lbl_weight = tk.Label(root, textvariable=weight_var, font=("Arial", 24))
lbl_weight.pack(pady=(10,0), fill='x')

# 倒计时
timer_var = tk.StringVar(value="10 s")
lbl_timer = tk.Label(root, textvariable=timer_var, font=("Arial", 18), fg="blue")
lbl_timer.pack(pady=(5,10))

# 绑定空格键重启倒计时
root.bind('<space>', restart_countdown)

# 启动串口读取和初始倒计时
root.after(100, lambda: start_serial_thread(weight_var))
root.after(100, lambda: countdown(10, timer_var))

root.mainloop()

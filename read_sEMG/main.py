from sEMG_receiver import ReceiverThreaded
from sEMG_plotter import sEMGplotter

def main():
    port_name = 'COM17'  # 根据实际情况修改

    try:
        rx = ReceiverThreaded(port=port_name,
                              baudrate=115200,
                              buffer_size=4096,
                              window_size=500)
    except RuntimeError as e:
        print(f"ERROR: {e}")
        return

    plotter = sEMGplotter(sensor_receiver=rx,
                          fields=('A0','A1','A4','A3'),
                          figsize=(8,6),
                          interval=100)  # 10 FPS，最少每 100 ms 更新一次

    try:
        plotter.show()
    except KeyboardInterrupt:
        # 如果你按 Ctrl+C 强制退出，也要保证串口线程能关闭
        pass
    finally:
        rx.close()

if __name__ == '__main__':
    main()

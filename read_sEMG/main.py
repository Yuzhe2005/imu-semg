import threading
import sys
from sEMG_sensor import open_serial, read_emg
from sEMG_plotter import EMGPlotter
import matplotlib.pyplot as plt
import serial


def data_reader(ser, plotter, stop_event):
    """Continuously read EMG and append to plotter's data buffer until stopped."""
    while not stop_event.is_set():
        try:
            value = read_emg(ser)
            if value is not None:
                plotter.data.append(value)
        except serial.SerialException:
            break


def main():
    port = 'COM17'  # update as needed
    try:
        ser = open_serial(port)
    except Exception as e:
        print(f"Failed to open serial port {port}: {e}", file=sys.stderr)
        sys.exit(1)

    plotter = EMGPlotter(length=1000)

    # Event to signal thread to stop
    stop_event = threading.Event()

    # Start background thread to read serial data
    thread = threading.Thread(target=data_reader, args=(ser, plotter, stop_event), daemon=True)
    thread.start()

    # Start animation and show plot
    ani = plotter.animate(interval=20)  # 20 ms -> ~50 FPS
    try:
        plt.show()
    finally:
        # Signal thread to stop and close serial
        stop_event.set()
        if ser and ser.is_open:
            ser.close()

if __name__ == '__main__':
    main()
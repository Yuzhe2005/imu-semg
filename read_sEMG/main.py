import threading
import sys
from sEMG_sensor import open_serial, read_emg
from sEMG_plotter import EMGPlotter


def data_reader(ser, plotter):
    """Continuously read EMG and append to plotter's data buffer."""
    try:
        while True:
            value = read_emg(ser)
            if value is not None:
                plotter.data.append(value)
    except Exception as e:
        # Log and exit thread cleanly
        print(f"Data reader error: {e}", file=sys.stderr)


def main():
    port = 'COM17'  # update as needed
    try:
        ser = open_serial(port)
    except Exception as e:
        print(f"Failed to open serial port {port}: {e}", file=sys.stderr)
        sys.exit(1)

    plotter = EMGPlotter(length=1000)

    # Start background thread to read serial data
    thread = threading.Thread(target=data_reader, args=(ser, plotter), daemon=True)
    thread.start()

    # Start animation
    ani = plotter.animate(interval=20)  # 20 ms -> ~50 FPS
    plt = plotter.fig.canvas.manager.canvas.figure.canvas.manager.window
    import matplotlib.pyplot as plt_show
    plt_show.show()
    ser.close()

if __name__ == '__main__':
    main()
# main.py
import threading
import sys
import csv
import matplotlib.pyplot as plt

from sEMG_sensor import open_serial
from sEMG_plotter import QuadEMGPlotter

def data_reader(ser, plotter):
    """
    Continuously read EMG lines from serial.
    Expect each line as 'value0,value1,value2,value3', where:
      - value0 is A0 reading (float or int)
      - value1 is A1 reading
      - value2 is A2 reading
      - value3 is A3 reading
    Append to the appropriate deque and store in storage lists.
    """
    try:
        while True:
            raw = ser.readline().decode('ascii', errors='ignore').strip()
            if not raw:
                continue

            parts = raw.split(',')
            if len(parts) != 4:
                # If line is malformed, skip it
                continue
            try:
                v0 = float(parts[0])
                v1 = float(parts[1])
                v2 = float(parts[2])
                v3 = float(parts[3])
            except ValueError:
                # If conversion fails, skip
                continue

            # Append to each channel’s deque
            plotter.data_A0.append(v0)
            plotter.data_A1.append(v1)
            plotter.data_A2.append(v2)
            plotter.data_A3.append(v3)

            # Store for CSV output later
            plotter.storage_A0.append(v0)
            plotter.storage_A1.append(v1)
            plotter.storage_A2.append(v2)
            plotter.storage_A3.append(v3)

    except Exception as e:
        print(f"Data reader error: {e}", file=sys.stderr)

def main():
    port = 'COM17'  # <-- change this to your actual serial port
    try:
        ser = open_serial(port)
    except Exception as e:
        print(f"Failed to open serial port {port}: {e}", file=sys.stderr)
        sys.exit(1)

    print("[Port connected]")

    # Create a QuadEMGPlotter (four-channel) with a window length of 1000 samples
    plotter = QuadEMGPlotter(length=1000)

    # Start background thread to read serial data
    thread = threading.Thread(target=data_reader, args=(ser, plotter), daemon=True)
    thread.start()

    # Start animation (this will pop up a matplotlib window)
    ani = plotter.animate(interval=20)  # 20 ms ≈ 50 FPS

    # Show the figure (blocks here until the window is closed)
    plt.show()

    # After the window is closed, close serial port
    ser.close()

    print("[Saving data to CSV]")

    # Write all stored data into a CSV with columns: Sample, A0, A1, A2, A3
    with open('all_data_four_channels.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Sample', 'A0', 'A1', 'A2', 'A3'])
        for idx, (a0, a1, a2, a3) in enumerate(zip(
            plotter.storage_A0,
            plotter.storage_A1,
            plotter.storage_A2,
            plotter.storage_A3
        )):
            writer.writerow([idx, a0, a1, a2, a3])

    print("[Data saved. Program complete]")

if __name__ == '__main__':
    main()

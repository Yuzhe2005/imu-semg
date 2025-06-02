
from imu_serial import IMUSerialReader
from imu_buffer import IMUBuffer
from imu_plotter import IMUPlotter
import csv

def main():
    # Configuration
    SERIAL_PORT = "COM16"       
    BAUD_RATE   = 2000000      
    WINDOW_SIZE = 1024        
    # INTERVAL_MS = 10           

    imu_buffer = IMUBuffer(WINDOW_SIZE)

    # Start serial reader thread
    serial_reader = IMUSerialReader(SERIAL_PORT, BAUD_RATE, imu_buffer)
    serial_reader.start()

    plotter = IMUPlotter(imu_buffer, WINDOW_SIZE)
    plotter.show()

    serial_reader.stop()

    with open("imu_data.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for row in imu_buffer.storage_ax:
            writer.writerow([row])

if __name__ == "__main__":
    main()

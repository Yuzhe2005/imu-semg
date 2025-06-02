
from imu_serial import IMUSerialReader
from imu_single_buffer import IMUBuffer
from imu_all_buffer import IMUAllBuffer
from imu_plotter import IMUPlotter
import csv

def main():
    # Configuration
    SERIAL_PORT = "COM16"       
    BAUD_RATE   = 2000000      
    WINDOW_SIZE = 1024        
    # INTERVAL_MS = 10           

    imu0_buffer = IMUBuffer(WINDOW_SIZE)
    imu1_buffer = IMUBuffer(WINDOW_SIZE)
    imu_all_buffer = IMUAllBuffer(imu0_buffer, imu1_buffer)
    # print("[IMU_ALL_BUFFER CREATED SUCCESSFULLY]")

    # Start serial reader thread
    serial_reader = IMUSerialReader(SERIAL_PORT, BAUD_RATE, imu_all_buffer)
    serial_reader.start()

    plotter = IMUPlotter(imu_all_buffer, WINDOW_SIZE)
    plotter.show()

    serial_reader.stop()

    with open("imu_data.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for row in imu_all_buffer.IMU0.storage['ax']:
            writer.writerow([row])

if __name__ == "__main__":
    main()

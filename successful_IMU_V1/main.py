
from imu_serial import IMUSerialReader
from imu_single_buffer import IMUBuffer
from imu_all_buffer import IMUAllBuffer
from imu_plotter import IMUPlotter
from scipy.io import loadmat
import scipy.io as sio
import threading
import csv

def main():
    # Configuration
    SERIAL_PORT = "COM16"       
    BAUD_RATE   = 2000000      
    WINDOW_SIZE = 1024        
    # INTERVAL_MS = 10          

    imu0_buffer = IMUBuffer(WINDOW_SIZE)
    imu1_buffer = IMUBuffer(WINDOW_SIZE)
    imu2_buffer = IMUBuffer(WINDOW_SIZE)
    imu3_buffer = IMUBuffer(WINDOW_SIZE)
    imu_all_buffer = IMUAllBuffer(imu0_buffer, imu1_buffer, imu2_buffer, imu3_buffer)
    # print("[IMU_ALL_BUFFER CREATED SUCCESSFULLY]")

    # Start serial reader thread
    serial_reader = IMUSerialReader(SERIAL_PORT, BAUD_RATE, imu_all_buffer)

    def save_data_in_matlab_format(all_buffer):
        for idx in range(all_buffer.num):
            mat_data = {
                'ax': list(all_buffer.IMU[0].storage['ax']),
                'ay': list(all_buffer.IMU[0].storage['ay']),
                'az': list(all_buffer.IMU[0].storage['az']),
                'gx': list(all_buffer.IMU[0].storage['gx']),
                'gy': list(all_buffer.IMU[0].storage['gy']),
                'gz': list(all_buffer.IMU[0].storage['gz'])
            }
            dirPath = "../data"
            filename = f"IMU{idx}_data.mat"
            file_path = dirPath + "/" + filename
            sio.savemat(file_path, mat_data)
            print(f"IMU{idx} data saved to {file_path}")


    DURATION = 10
    t = threading.Thread(target=serial_reader.record, args=(DURATION,), daemon=True)
    t.start()
    
    # serial_reader.start()

    plotter = IMUPlotter(imu_all_buffer, WINDOW_SIZE)
    plotter.show()

    # serial_reader.stop()
    t.join()

    save_data_in_matlab_format(imu_all_buffer)
    
    serial_reader.ser.close()
    print("[All IMU sensors closed]")
    
if __name__ == "__main__":
    main()


from imu_serial import IMUSerialReader
from imu_single_buffer import IMUBuffer
from imu_all_buffer import IMUAllBuffer
from imu_plotter import IMUPlotter
from scipy.io import loadmat
import scipy.io as sio
import threading
import matplotlib.pyplot as plt
import signal

def main():
    # Configuration
    SERIAL_PORT = "COM19"       
    BAUD_RATE   = 2000000      
    WINDOW_SIZE = 1024   
    DURATION = 100 #set duration
     
    INTERVAL_MS = 10          

    imu0_buffer = IMUBuffer(WINDOW_SIZE)
    imu1_buffer = IMUBuffer(WINDOW_SIZE)
    imu2_buffer = IMUBuffer(WINDOW_SIZE)
    imu3_buffer = IMUBuffer(WINDOW_SIZE)
    imu_all_buffer = IMUAllBuffer(imu0_buffer, imu1_buffer, imu2_buffer, imu3_buffer)

    # Start serial reader thread
    serial_reader = IMUSerialReader(SERIAL_PORT, BAUD_RATE, imu_all_buffer)

    print("[Port connected]")
    print(f"[Expected Recording Time: {DURATION}s]")

    def sigint_handler(signum, frame):
        print("\n[Received Ctrl+C, shutting down]")
        serial_reader.running = False
        plt.close('all')

    signal.signal(signal.SIGINT, sigint_handler)

    def save_data_in_matlab_format(all_buffer):
        for idx in range(all_buffer.num):
            mat_data = {
                'ax': list(all_buffer.IMU[idx].storage['ax']),
                'ay': list(all_buffer.IMU[idx].storage['ay']),
                'az': list(all_buffer.IMU[idx].storage['az']),
                'gx': list(all_buffer.IMU[idx].storage['gx']),
                'gy': list(all_buffer.IMU[idx].storage['gy']),
                'gz': list(all_buffer.IMU[idx].storage['gz'])
            }
            dirPath = "../../data"
            filename = f"IMU{idx}_data.mat"
            file_path = dirPath + "/" + filename
            sio.savemat(file_path, mat_data)
            print(f"[IMU{idx} data saved to {file_path}]")

    t = threading.Thread(target=serial_reader.record, args=(DURATION,), daemon=True)
    t.start()

    plotter = IMUPlotter(imu_all_buffer, WINDOW_SIZE)
    plotter.show()

    t.join()

    save_data_in_matlab_format(imu_all_buffer)
    
    serial_reader.ser.close()
    print("[All IMU sensors closed]")
    
if __name__ == "__main__":
    main()

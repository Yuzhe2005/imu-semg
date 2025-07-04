import threading
import signal
import matplotlib.pyplot as plt
import scipy.io as sio
import os

from successful_IMU_V1.imu_serial     import IMUSerialReader
from successful_IMU_V1.imu_all_buffer import IMUAllBuffer
from successful_IMU_V1.imu_single_buffer import IMUBuffer
from successful_sEMG_V2.sEMG_sensor   import SensorReader

from comb_plotter import CombinedPlotter

def main(time_duration, folder_name):

    DURATION = int(time_duration)
    # ——— IMU Setup ———
    IMU_PORT   = "COM19"
    IMU_BAUD   = 2000000
    IMU_WIN    = 1024
    IMU_INT_MS = 10

    imu_buffers = [IMUBuffer(IMU_WIN) for _ in range(4)]
    imu_sensor     = IMUAllBuffer(*imu_buffers)
    imu_reader  = IMUSerialReader(IMU_PORT, IMU_BAUD, imu_sensor)

    # ——— sEMG Setup ———
    EMG_PORT   = "COM17"
    EMG_BAUD   = 1000000
    EMG_WIN    = 1000
    EMG_INT_MS = 20

    emg_sensor = SensorReader(EMG_PORT, baudrate=EMG_BAUD, window_size=EMG_WIN)

    # Ctrl+C clean shutdown
    def signal_handler(sig, frame):
        print("\nStopping…")
        emg_sensor.running = False
        imu_reader.running = False
        plt.close('all')
    signal.signal(signal.SIGINT, signal_handler)

    def save_data_in_matlab_format(emg_sensor, imu_sensor, folder_name):
        for idx in range(imu_sensor.num):
            imu_data = {
                'ax': list(imu_sensor.IMU[idx].storage['ax']),
                'ay': list(imu_sensor.IMU[idx].storage['ay']),
                'az': list(imu_sensor.IMU[idx].storage['az']),
                'gx': list(imu_sensor.IMU[idx].storage['gx']),
                'gy': list(imu_sensor.IMU[idx].storage['gy']),
                'gz': list(imu_sensor.IMU[idx].storage['gz'])
            }
        
        emg_data = {
            'A0': list(emg_sensor.storage['A0']),
            'A1': list(emg_sensor.storage['A1']),
            'A2': list(emg_sensor.storage['A2']),
            'A3': list(emg_sensor.storage['A3'])
        }

        base_data_dir = os.path.join('..', 'data', 'testing data')
        dir_path = os.path.join(base_data_dir, folder_name)
        os.makedirs(dir_path, exist_ok=True)

        imu_filepath = os.path.join(dir_path, 'imu.mat')
        sio.savemat(imu_filepath, imu_data)

        emg_filepath = os.path.join(dir_path, 'emg.mat')
        sio.savemat(emg_filepath, emg_data)

    # Start acquisition threads
    t_imu = threading.Thread(target=imu_reader.record, args=(DURATION,), daemon=True)
    t_semg = threading.Thread(target=emg_sensor.record, args=(DURATION,), daemon=True)

    t_imu.start()
    t_semg.start()

    # Launch combined real-time plot
    cp = CombinedPlotter(imu_sensor, emg_sensor,
                         imu_win=IMU_WIN, emg_win=EMG_WIN,
                         imu_interval=IMU_INT_MS, emg_interval=EMG_INT_MS)
    cp.show()

    t_imu.join()
    t_semg.join()

    save_data_in_matlab_format(emg_sensor, imu_sensor, folder_name)

    # Clean up serial ports on exit
    imu_reader.ser.close()
    emg_sensor.ser.close()
    print("[Done]")

if __name__ == "__main__":
    month = input("Month:")
    date = input("Date:")
    test_round = input("Test round:")
    DURATION = input("Duration:")
    folder_name = month + '_' + date + '_' + "Test round_" + test_round

    main(DURATION, folder_name)

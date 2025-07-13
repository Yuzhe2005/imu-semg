import threading
import signal
import matplotlib.pyplot as plt
import scipy.io as sio
import tkinter as tk
from tkinter import messagebox

from successful_IMU_V1.imu_serial     import IMUSerialReader
from successful_IMU_V1.imu_all_buffer import IMUAllBuffer
from successful_IMU_V1.imu_single_buffer import IMUBuffer
from successful_sEMG_V2.sEMG_sensor   import SensorReader
# from successful_sEMG_V2.sEMG_plotter import EMGPlotter
# from successful_IMU_V1.imu_plotter import IMUPlotter
from load_cell.lc_reader import LoadCellReader

from comb_plotter import CombinedPlotter

def main(time_duration, file_name, mvic):

    DURATION = int(time_duration)
    # ——— IMU Setup ———
    IMU_PORT   = "COM28"
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

    # ——— Load cell Setup ———
    LC_port = "COM27"
    LC_baud = 115200
    LC_WIN = 20
    LC_INT_MS = 50

    # root = tk.Tk()
    # root.title("Load Cell + Countdown")
    # root.geometry("360x160")

    # weight_var = tk.StringVar(value="Waiting for dta...")
    # lbl_weight = tk.Label(root, textvariable=weight_var, font=("Arial", 24))
    # lbl_weight.pack(pady=(10,0), fill='x')

    lc_sensor = LoadCellReader(LC_port, LC_baud, window_size = LC_WIN)

    # Ctrl+C clean shutdown
    def signal_handler(sig, frame):
        print("\nStopping…")
        emg_sensor.running = False
        imu_reader.running = False
        lc_sensor.running = False
        plt.close('all')
    signal.signal(signal.SIGINT, signal_handler)

    def save_data_in_matlab_format(emg_sensor, imu_sensor, lc_sensor, file_name):

        dirPath = "../data/testing data/7_11_DiffMVIC_test_David_round1";

        for idx in range(imu_sensor.num):
            imu_data = {
                'ax': list(imu_sensor.IMU[idx].storage['ax']),
                'ay': list(imu_sensor.IMU[idx].storage['ay']),
                'az': list(imu_sensor.IMU[idx].storage['az'])
                # 'gx': list(imu_sensor.IMU[idx].storage['gx']),
                # 'gy': list(imu_sensor.IMU[idx].storage['gy']),
                # 'gz': list(imu_sensor.IMU[idx].storage['gz'])
            }

            imu_filename = f"imu{idx}_{file_name}.mat"
            imu_filepath = f"{dirPath}/{imu_filename}"
            sio.savemat(imu_filepath, imu_data)
        
        emg_data = {
            'A0': list(emg_sensor.storage['A0']),
            'A1': list(emg_sensor.storage['A1']),
            'A2': list(emg_sensor.storage['A2']),
            'A3': list(emg_sensor.storage['A3'])
        }

        emg_filename = f"emg_{file_name}.mat"
        emg_filepath = f"{dirPath}/{emg_filename}"
        sio.savemat(emg_filepath, emg_data)

        lc_data = {'value' : list(lc_sensor.storage)}

        lc_filename = f"lc_{file_name}.mat"
        lc_filepath = f"{dirPath}/{lc_filename}"
        sio.savemat(lc_filepath, lc_data)

    # Start acquisition threads
    t_imu = threading.Thread(target=imu_reader.record, args=(DURATION,), daemon=True)
    t_semg = threading.Thread(target=emg_sensor.record, args=(DURATION,), daemon=True)
    t_lc = threading.Thread(target=lc_sensor.record, args=(DURATION,), daemon=True)

    t_imu.start()
    t_semg.start()
    t_lc.start()

    # def countdown(count, timer_var):
    #     if count >= 0:
    #         timer_var.set(f"{count} s")
    #         root.after(1000, countdown, count-1, timer_var)
    #     else:
    #         timer_var.set("Done")

    # timer_var = tk.StringVar(value="10 s")
    # lbl_timer = tk.Label(root, textvariable=timer_var, font=("Arial", 18), fg="blue")
    # lbl_timer.pack(pady=(5,10))

    # root.after(100, lambda: countdown(10, timer_var))

    # root.mainloop()

    # Launch combined real-time plot
    cp = CombinedPlotter(imu_sensor, emg_sensor, lc_sensor, mvic,
                         imu_win=IMU_WIN, emg_win=EMG_WIN,
                         imu_interval=IMU_INT_MS, emg_interval=EMG_INT_MS,
                         lc_interval = LC_INT_MS)
    cp.show()

    t_imu.join()
    t_semg.join()
    # t_lc.join()

    save_data_in_matlab_format(emg_sensor, imu_sensor, lc_sensor, file_name)

    # Clean up serial ports on exit
    imu_reader.ser.close()
    emg_sensor.ser.close()
    lc_sensor.ser.close()
    print("[Done]")

if __name__ == "__main__":
    file_name = input("Filename(MVIC):")
    DURATION = input("Duration:")
    MVIC = input("MVIC(kg):")

    main(DURATION, file_name, MVIC)

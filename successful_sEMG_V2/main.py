# main.py

import threading
# import csv
from scipy.io import loadmat
import scipy.io as sio

from sEMG_sensor import SensorReader
from sEMG_plotter import EMGPlotter

def main():
    port = 'COM17'        
    WINDOW_SIZE = 1000    
    DURATION = 10     

    sensor = SensorReader(port, window_size=WINDOW_SIZE)
    print("[Port connected]")

    def save_data_in_matlab_format(sensor):
        mat_data = {
            'A0': list(sensor.storage['A0']),
            'A1': list(sensor.storage['A1']),
            'A2': list(sensor.storage['A2']),
            'A3': list(sensor.storage['A3'])
        }
        dirPath = "../data"
        filename = "sEMG_data.mat"
        file_path = dirPath + "/" + filename
        sio.savemat(file_path, mat_data)
        print(f"[sEMG data saved to {file_path}]")

    t = threading.Thread(target=sensor.record, args=(DURATION,), daemon=True)
    t.start()

    plotter = EMGPlotter(sensor, window_size=WINDOW_SIZE)
    plotter.show()

    t.join()

    save_data_in_matlab_format(sensor)

    sensor.ser.close()
    print("[All EMG sensors closed]")

if __name__ == '__main__':
    main()

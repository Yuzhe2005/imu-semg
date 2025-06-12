import threading
import signal
import matplotlib.pyplot as plt
import scipy.io as sio

from sEMG_sensor import SensorReader
from sEMG_plotter import EMGPlotter

def main(output_filename, time_duration):
    port = 'COM17'        
    WINDOW_SIZE = 1000    
    DURATION = int(time_duration)

    sensor = SensorReader(port, window_size=WINDOW_SIZE)

    print("[Port connected]")
    print(f"[Expected Recording Time: {DURATION}s]")

    def sigint_handler(signum, frame):
        print("\n[Received Ctrl+C, shutting down]")
        sensor.running = False
        plt.close('all')

    signal.signal(signal.SIGINT, sigint_handler)

    def save_data_in_matlab_format(sensor, filename):
        mat_data = {
            'A0': list(sensor.storage['A0']),
            'A1': list(sensor.storage['A1']),
            'A2': list(sensor.storage['A2']),
            'A3': list(sensor.storage['A3'])
        }
        dirPath = "../data/testing data"
        if not filename.endswith('.mat'):
            filename += '.mat'
        file_path = f"{dirPath}/{filename}"
        sio.savemat(file_path, mat_data)
        print(f"[sEMG data saved to {file_path}]")

    t = threading.Thread(target=sensor.record, args=(DURATION,), daemon=True)
    t.start()

    plotter = EMGPlotter(sensor, window_size=WINDOW_SIZE)
    plotter.show()

    t.join()

    save_data_in_matlab_format(sensor, output_filename)

    sensor.ser.close()
    print("[All EMG sensors closed]")

if __name__ == '__main__':
    filename = input("Enter the name of your file (without extension): ")
    DURATION = input("Enter the time duration of the test (s): ")
    main(filename, DURATION)

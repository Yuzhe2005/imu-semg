# sEMG_plotter.py

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class EMGPlotter:
    def __init__(self, sensor, window_size, interval=20):
        self.sensor = sensor
        self.window_size = window_size

        self.fig, self.axes = plt.subplots(2, 2, figsize=(10, 5), sharex=True)
        self.lines = {}

        for i in range(2):
            for j in range(2):
                idx = i * 2 + j
                field = f"A{idx}"
                ax = self.axes[i][j]
                ax.set_title(field)
                ax.set_xlabel("sample #")
                ax.set_ylabel("ADC value")
                ax.set_ylim(0, 1024)

                ax.set_xlim(0, self.window_size - 1)

                line_obj, = ax.plot([], [], lw=1.0, label=field)
                ax.legend(loc="upper right")
                self.lines[field] = line_obj

        plt.tight_layout()

        self.ani = FuncAnimation(
            self.fig,
            self.update,
            interval=interval,
            blit=True,               
            cache_frame_data=False   
        )

    def update(self, frame):
        all_data = self.sensor.get_all_data()

        x = list(range(self.window_size))
        for field, line_obj in self.lines.items():
            y = all_data[field]
            line_obj.set_data(x, y)

        return list(self.lines.values())

    def show(self):
        plt.show()

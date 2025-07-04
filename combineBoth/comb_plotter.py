# plotter.py

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class CombinedPlotter:
    def __init__(self,
                 imu_all_buffer, emg_sensor,
                 imu_win=1024, emg_win=1000,
                 imu_interval=10, emg_interval=20):

        self.imu_buf = imu_all_buffer
        self.emg    = emg_sensor
        rows = self.imu_buf.num + 1
        cols = 6

        self.fig, axes = plt.subplots(rows, cols,
                                      figsize=(12, 8),
                                      squeeze=False)
        plt.tight_layout(h_pad=2, w_pad=1)

        # IMU sub-plots
        imu_fields = ('ax','ay','az','gx','gy','gz')
        self.imu_lines = {}
        for i in range(self.imu_buf.num):
            for j, f in enumerate(imu_fields):
                ax = axes[i][j]
                ax.set_title(f"IMU {i} {f}")
                ax.set_xlim(0, imu_win)
                ax.set_ylim((-20,20) if f.startswith('a') else (-5.5,5.5))
                line, = ax.plot([], [], label=f)
                ax.legend(loc="upper right")
                self.imu_lines[(i,f)] = line

        # sEMG sub-plots on last row
        last = self.imu_buf.num
        self.emg_lines = {}
        for ch in range(4):
            ax = axes[last][ch]
            name = f"A{ch}"
            ax.set_title(f"EMG {name}")
            ax.set_xlim(0, emg_win)
            ax.set_ylim(0, 1024)
            line, = ax.plot([], [], lw=1, label=name)
            ax.legend(loc="upper right")
            self.emg_lines[name] = line

        # hide unused axes
        for c in (4,5):
            axes[last][c].axis('off')

        # single FuncAnimation driving both
        interval = min(imu_interval, emg_interval)
        self.ani = FuncAnimation(self.fig, self._update,
                                 interval=interval,
                                 blit=True,
                                 cache_frame_data=False)

    def _update(self, frame):
        # pull IMU data
        for (i,f), line in self.imu_lines.items():
            data = self.imu_buf.IMU[i].get_all_data()[f]
            line.set_data(range(len(data)), data)

        # pull sEMG data
        emg = self.emg.get_all_data()
        for name, line in self.emg_lines.items():
            y = emg[name]
            line.set_data(range(len(y)), y)

        return list(self.imu_lines.values()) + list(self.emg_lines.values())

    def show(self):
        plt.show()

# # plotter.py

# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation

# class CombinedPlotter:
#     def __init__(self,
#                  imu_all_buffer, emg_sensor,
#                  imu_win=1024, emg_win=1000,
#                  imu_interval=10, emg_interval=20):

#         self.imu_buf = imu_all_buffer
#         self.emg    = emg_sensor
#         rows = self.imu_buf.num + 1
#         cols = 6

#         self.fig, axes = plt.subplots(rows, cols,
#                                       figsize=(12, 8),
#                                       squeeze=False)
#         plt.tight_layout(h_pad=2, w_pad=1)

#         # IMU sub-plots
#         imu_fields = ('ax','ay','az','gx','gy','gz')
#         self.imu_lines = {}
#         for i in range(self.imu_buf.num):
#             for j, f in enumerate(imu_fields):
#                 ax = axes[i][j]
#                 ax.set_title(f"IMU {i} {f}")
#                 ax.set_xlim(0, imu_win)
#                 ax.set_ylim((-20,20) if f.startswith('a') else (-5.5,5.5))
#                 line, = ax.plot([], [], label=f)
#                 ax.legend(loc="upper right")
#                 self.imu_lines[(i,f)] = line

#         # sEMG sub-plots on last row
#         last = self.imu_buf.num
#         self.emg_lines = {}
#         for ch in range(4):
#             ax = axes[last][ch]
#             name = f"A{ch}"
#             ax.set_title(f"EMG {name}")
#             ax.set_xlim(0, emg_win)
#             ax.set_ylim(0, 1024)
#             line, = ax.plot([], [], lw=1, label=name)
#             ax.legend(loc="upper right")
#             self.emg_lines[name] = line

#         # hide unused axes
#         for c in (4,5):
#             axes[last][c].axis('off')

#         # single FuncAnimation driving both
#         interval = min(imu_interval, emg_interval)
#         self.ani = FuncAnimation(self.fig, self._update,
#                                  interval=interval,
#                                  blit=True,
#                                  cache_frame_data=False)

#     def _update(self, frame):
#         # pull IMU data
#         for (i,f), line in self.imu_lines.items():
#             data = self.imu_buf.IMU[i].get_all_data()[f]
#             line.set_data(range(len(data)), data)

#         # pull sEMG data
#         emg = self.emg.get_all_data()
#         for name, line in self.emg_lines.items():
#             y = emg[name]
#             line.set_data(range(len(y)), y)

#         return list(self.imu_lines.values()) + list(self.emg_lines.values())

#     def show(self):
#         plt.show()




import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def combine_plots(ax_src_list):
    """Helper to merge positions of multiple axes into one"""
    x0 = min(ax.get_position().x0 for ax in ax_src_list)
    y0 = min(ax.get_position().y0 for ax in ax_src_list)
    x1 = max(ax.get_position().x1 for ax in ax_src_list)
    y1 = max(ax.get_position().y1 for ax in ax_src_list)
    return [x0, y0, x1 - x0, y1 - y0]

class CombinedPlotter:
    def __init__(self,
                 imu_all_buffer,
                 emg_sensor,
                 lc_sensor,
                 MVIC,
                 imu_win=1024,
                 emg_win=1000,
                 imu_interval=10,
                 emg_interval=20,
                 lc_interval=50,
                 lc_x_offset=0.01):
        # ensure MVIC is numeric
        self.MVIC = int(MVIC)

        self.imu_buf = imu_all_buffer
        self.emg    = emg_sensor
        self.lc     = lc_sensor

        rows = self.imu_buf.num + 1  # number of rows: IMU rows + one sEMG row
        cols = 6
        self.fig = plt.figure(figsize=(12, 2 * rows - 2))

        # IMU subplots (ax, ay, az) + placeholders for gyro columns
        imu_axes = []
        self.imu_lines = {}
        for i in range(self.imu_buf.num):
            placeholders = []
            for j, f in enumerate(('ax', 'ay', 'az')):
                ax = self.fig.add_subplot(rows, cols, i*cols + j + 1)
                ax.set_title(f"IMU {i} {f}")
                ax.set_xlim(0, imu_win)
                ax.set_ylim(-20, 20)
                line, = ax.plot([], [], lw=1)
                self.imu_lines[(i, f)] = line
            # hide gyro columns
            for c in (3, 4, 5):
                ph = self.fig.add_subplot(rows, cols, i*cols + c + 1)
                ph.axis('off')
                placeholders.append(ph)
            imu_axes.append(placeholders)

        # combine placeholders to create the big Load Cell axis
        placeholder_list = [ax for row in imu_axes for ax in row]
        bbox = combine_plots(placeholder_list)
        # apply slight right shift
        bbox[0] += lc_x_offset

        ax_big_lc = self.fig.add_axes(bbox)
        ax_big_lc.set_title(f"Load Cell (% of {self.MVIC})")

        # x-axis: 0 to window size
        ws = self.lc.window_size
        ax_big_lc.set_xlim(0, ws)
        # y-axis: 0 to MVIC, but only percentage ticks shown
        ax_big_lc.set_ylim(0, self.MVIC)

        # retain only percentage ticks: 10%–80%
        pct_vals = [self.MVIC * i / 10 for i in range(1, 9)]
        pct_labels = [f"{i*10}%" for i in range(1, 9)]
        ax_big_lc.set_yticks(pct_vals)
        ax_big_lc.set_yticklabels(pct_labels)

        # add fine dashed grid for reference
        ax_big_lc.yaxis.grid(True, linestyle=':', linewidth=0.5, zorder=0)

        # plot the Load Cell data line
        self.big_lc_line, = ax_big_lc.plot([], [], lw=2, zorder=1)

        # sEMG plots on the last row (four channels)
        emg_row = self.imu_buf.num
        self.emg_lines = {}
        for ch in range(4):
            ax = self.fig.add_subplot(rows, cols, emg_row*cols + ch + 1)
            name = f"A{ch}"
            ax.set_title(f"EMG {name}")
            ax.set_xlim(0, emg_win)
            ax.set_ylim(0, 1024)
            line, = ax.plot([], [], lw=1)
            self.emg_lines[name] = line
        # hide the last two columns
        for c in (4, 5):
            ax = self.fig.add_subplot(rows, cols, emg_row*cols + c + 1)
            ax.axis('off')

        plt.tight_layout()
        interval = min(imu_interval, emg_interval, lc_interval)
        self.ani = FuncAnimation(
            self.fig,
            self._update,
            interval=interval,
            blit=True,
            cache_frame_data=False
        )

    def _update(self, frame):
        # update IMU lines
        for (i, f), line in self.imu_lines.items():
            data = self.imu_buf.IMU[i].get_all_data()[f]
            line.set_data(range(len(data)), data)

        # update Load Cell line and keep y-axis static
        lc_vals = list(self.lc.get_all_data())
        self.big_lc_line.set_data(range(len(lc_vals)), lc_vals)
        self.big_lc_line.axes.set_ylim(0, self.MVIC)

        # update sEMG lines
        emg = self.emg.get_all_data()
        for name, line in self.emg_lines.items():
            y = emg[name]
            line.set_data(range(len(y)), y)

        return (
            list(self.imu_lines.values())
            + [self.big_lc_line]
            + list(self.emg_lines.values())
        )

    def show(self):
        plt.show()

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
                 MVIC,                 # 最大值参数
                 imu_win=1024,
                 emg_win=1000,
                 imu_interval=10,
                 emg_interval=20,
                 lc_interval=50,
                 lc_x_offset=0.01):
        # 1) 强制将 MVIC 转为整数
        self.MVIC = int(MVIC)

        self.imu_buf = imu_all_buffer
        self.emg    = emg_sensor
        self.lc     = lc_sensor

        rows = self.imu_buf.num + 1  # IMU 行 + 最后一行 sEMG
        cols = 6
        # 整体画布高度做了微调
        self.fig = plt.figure(figsize=(12, 2 * rows - 2))

        # --- IMU 子图 (ax, ay, az) + 三个占位 (隐藏) ---
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
            # 占位：隐藏原来 gyro 的三列
            for c in (3, 4, 5):
                ph = self.fig.add_subplot(rows, cols, i*cols + c + 1)
                ph.axis('off')
                placeholders.append(ph)
            imu_axes.append(placeholders)

        # --- 合并所有占位，生成一个大 Load Cell 轴 ---
        placeholder_list = [ax for row in imu_axes for ax in row]
        bbox = combine_plots(placeholder_list)
        # 2) 在这里做一点水平偏移，避免刻度重叠
        bbox[0] += lc_x_offset

        ax_big_lc = self.fig.add_axes(bbox)
        ax_big_lc.set_title(f"Load Cell (0–{self.MVIC} & 10%–80%)")

        # x 轴：0 到窗口大小
        ws = self.lc.window_size
        ax_big_lc.set_xlim(0, ws)
        # y 轴：固定 0 到 self.MVIC
        ax_big_lc.set_ylim(0, self.MVIC)

        # 整数刻度：0, 5, 10, ..., MVIC（向上取整到最接近的 5 倍数）
        max_tick = ((self.MVIC + 4) // 5) * 5
        int_ticks = list(range(0, max_tick + 1, 5))
        ax_big_lc.set_yticks(int_ticks)

        # 百分比刻度：10%–80%
        pct_vals = [self.MVIC * i / 10 for i in range(1, 9)]
        pct_labels = [f"{i*10}%" for i in range(1, 9)]

        # 合并所有刻度，并用字符串标签展示
        all_ticks = int_ticks + pct_vals
        all_labels = [str(t) for t in int_ticks] + pct_labels
        ax_big_lc.set_yticks(all_ticks)
        ax_big_lc.set_yticklabels(all_labels)

        # 3) 添加细虚线网格
        ax_big_lc.yaxis.grid(True, linestyle=':', linewidth=0.5, zorder=0)

        # 主线（Load Cell 实线）
        self.big_lc_line, = ax_big_lc.plot([], [], lw=2, zorder=1)

        # --- sEMG 四通道放在最后一行前四列 ---
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
        # 隐藏最后两列
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
        # 更新所有 IMU 曲线
        for (i, f), line in self.imu_lines.items():
            data = self.imu_buf.IMU[i].get_all_data()[f]
            line.set_data(range(len(data)), data)

        # 更新 Load Cell 曲线，并保持 y 轴不变
        lc_vals = list(self.lc.get_all_data())
        self.big_lc_line.set_data(range(len(lc_vals)), lc_vals)
        self.big_lc_line.axes.set_ylim(0, self.MVIC)

        # 更新 sEMG 曲线
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

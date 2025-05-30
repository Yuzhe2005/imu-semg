import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class RealTimePlotter:
    """
    将 IMUReader.data 中的 6 条 deque，按照 2×3 子图实时刷新展示。
    """

    def __init__(self,
                 reader,
                 maxlen: int = 1000,
                 y_limits: tuple = None,
                 interval: int = 20,
                 blit: bool = True):
        """
        reader:   IMUReader 实例
        maxlen:   deque 长度 (横轴范围)
        y_limits: (min, max) 或 None(自动)
        interval: 帧刷新间隔(ms)，如20→50Hz
        blit:     是否启用 blitting
        """
        self.reader  = reader
        self.maxlen  = maxlen
        self.y_limits = y_limits
        self.interval = interval
        self.blit     = blit
        self.fields   = ['ax','ay','az','gx','gy','gz']

        # 2×3 布局
        self.fig, axes = plt.subplots(2, 3, figsize=(12, 6))
        self.lines = {}

        for ax, fld in zip(axes.flatten(), self.fields):
            # 初始化一条空曲线
            line, = ax.plot(range(maxlen), [0]*maxlen)
            ax.set_title(fld.upper())
            ax.set_xlim(0, maxlen)
            if y_limits:
                ax.set_ylim(*y_limits)
            ax.grid(True)
            self.lines[fld] = line

        self.ani = None

    def _update(self, frame):
        # 每次刷新前，deque 已由后台线程自动填满新样本
        artists = []
        for fld, line in self.lines.items():
            buf = self.reader.data[fld]
            # 更新曲线数据
            line.set_ydata(buf)
            # 如果没有固定 y_limits，则自动缩放
            if self.y_limits is None:
                ax = line.axes
                ax.relim()
                ax.autoscale_view()
            artists.append(line)
        return artists

    def animate(self):
        """ 启动动画循环 """
        self.ani = FuncAnimation(
            self.fig,
            self._update,
            interval=self.interval,
            blit=self.blit,
            cache_frame_data=False,
            save_count=self.maxlen
        )
        plt.tight_layout()
        plt.show()
        return self.ani

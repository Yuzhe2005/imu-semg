import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

class sEMGplotter:
    """
    实时画 4 路通道（A0–A3）的滚动波形；
    主线程只负责不断地把 deque 转成 list/ndarray 再绘图。
    """

    def __init__(self, sensor_receiver, fields=('A0','A1','A4','A3'),
                 figsize=(8,6), interval=100):
        """
        Args:
          sensor_receiver : 上面那个 ReceiverThreaded 实例
          fields          : 要画哪几个通道，对应 receiver.data 的 key
          figsize         : 窗口大小
          interval        : 每隔多少毫秒重绘一次
        """
        self.receiver = sensor_receiver
        self.fields = list(fields)
        self.window_size = sensor_receiver.window_size

        rows = len(self.fields)
        self.fig, axes = plt.subplots(rows, 1, figsize=figsize, sharex=True)

        if isinstance(axes, np.ndarray):
            self.axes = axes
        else:
            self.axes = np.array([axes])

        self.lines = {}
        for i, field in enumerate(self.fields):
            ax = self.axes[i]
            ax.set_ylim(0, 1024)
            ax.set_xlim(0, self.window_size)
            # 不需要图例，只画光滑线条
            line, = ax.plot([], [], lw=0.8)
            self.lines[field] = line
            # 只有最下面的子图显示 X 轴刻度
            if i < rows-1:
                ax.set_xticks([])

        self.fig.tight_layout()

        # blit=True 只重绘被修改过的 line
        self.ani = FuncAnimation(self.fig,
                                 self._update,
                                 init_func=self._init_lines,
                                 interval=interval,
                                 blit=True)

    def _init_lines(self):
        artists = []
        for line in self.lines.values():
            line.set_data([], [])
            artists.append(line)
        return artists

    def _update(self, frame):
        """
        每 interval 毫秒被 FuncAnimation 调用一次。
        只从 receiver.data 里读取最近的 deque，更新 line。
        """
        artists = []
        for field, line in self.lines.items():
            buf = self.receiver.data[field]       # deque
            data_np = np.array(buf)               # 把 deque 转成 numpy array
            x = np.arange(len(data_np))           # 0,1,2,...,N-1
            line.set_data(x, data_np)
            artists.append(line)
        return artists

    def show(self):
        plt.show()

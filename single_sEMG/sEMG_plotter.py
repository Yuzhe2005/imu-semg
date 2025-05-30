import matplotlib.pyplot as plt
from collections import deque
from matplotlib.animation import FuncAnimation

class EMGPlotter:
    def __init__(self, length=500, vmin=0.0, vmax=5.0):
        self.length = length
        self.data = deque([0.0] * length, maxlen=length)
        self.storage = []
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot(range(length), list(self.data))
        
        self.ax.set_ylim(vmin, 1024)
        self.ax.set_title('Real-time EMG (ENV)')
        self.ax.set_xlabel('Sample')

        # self.ax.set_ylabel('Voltage (V)')

    # def init_plot(self):
    #     self.line.set_ydata([0] * self.length)
    #     return (self.line,)

    def update_plot(self, frame):
        self.line.set_ydata(list(self.data))
        # # 
        # self.ax.relim()
        # self.ax.autoscale_view()
        return (self.line,)

    def animate(self, interval=20):
        # interval in milliseconds; cache_frame_data=False avoids warning
        return FuncAnimation(
            self.fig,
            self.update_plot,
            # init_func=self.init_plot,
            blit=True,
            interval=interval,
            cache_frame_data=False
        )
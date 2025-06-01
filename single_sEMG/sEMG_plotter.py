# sEMG_plotter.py
import matplotlib.pyplot as plt
from collections import deque
from matplotlib.animation import FuncAnimation

class QuadEMGPlotter:
    def __init__(self, length=500, vmin=0.0, vmax=1024.0):
        """
        length: number of samples to keep in each deque
        vmin/vmax: y-axis limits for all four channels
        """
        self.length = length

        # Four deques: one for A0, A1, A2, A3
        self.data_A0 = deque([0.0] * length, maxlen=length)
        self.data_A1 = deque([0.0] * length, maxlen=length)
        self.data_A2 = deque([0.0] * length, maxlen=length)
        self.data_A3 = deque([0.0] * length, maxlen=length)

        # Storage lists to save everything once the window closes
        self.storage_A0 = []
        self.storage_A1 = []
        self.storage_A2 = []
        self.storage_A3 = []

        # Create a figure with four vertically stacked subplots, sharing the x-axis
        self.fig, (self.ax0, self.ax1, self.ax2, self.ax3) = plt.subplots(
            4, 1, figsize=(8, 10), sharex=True
        )

        # A0 plot on ax0
        self.line0, = self.ax0.plot(
            range(length), list(self.data_A0), label="A0"
        )
        self.ax0.set_ylim(vmin, vmax)
        self.ax0.set_title("Real-time EMG (A0)")
        self.ax0.set_ylabel("ADC Value")
        self.ax0.legend(loc="upper right")

        # A1 plot on ax1
        self.line1, = self.ax1.plot(
            range(length), list(self.data_A1), label="A1", color="orange"
        )
        self.ax1.set_ylim(vmin, vmax)
        self.ax1.set_title("Real-time EMG (A1)")
        self.ax1.set_ylabel("ADC Value")
        self.ax1.legend(loc="upper right")

        # A2 plot on ax2
        self.line2, = self.ax2.plot(
            range(length), list(self.data_A2), label="A2", color="green"
        )
        self.ax2.set_ylim(vmin, vmax)
        self.ax2.set_title("Real-time EMG (A2)")
        self.ax2.set_ylabel("ADC Value")
        self.ax2.legend(loc="upper right")

        # A3 plot on ax3
        self.line3, = self.ax3.plot(
            range(length), list(self.data_A3), label="A3", color="red"
        )
        self.ax3.set_ylim(vmin, vmax)
        self.ax3.set_title("Real-time EMG (A3)")
        self.ax3.set_xlabel("Sample #")
        self.ax3.set_ylabel("ADC Value")
        self.ax3.legend(loc="upper right")

    def update_plot(self, frame):
        """
        Called by FuncAnimation every interval. Update y-data for all four lines.
        """
        self.line0.set_ydata(list(self.data_A0))
        self.line1.set_ydata(list(self.data_A1))
        self.line2.set_ydata(list(self.data_A2))
        self.line3.set_ydata(list(self.data_A3))
        return (self.line0, self.line1, self.line2, self.line3)

    def animate(self, interval=20):
        """
        interval: milliseconds between frames (e.g., 20 ms ≈ 50 FPS).
        Returns the FuncAnimation object.
        """
        return FuncAnimation(
            self.fig,
            self.update_plot,
            blit=True,
            interval=interval,
            cache_frame_data=False
        )

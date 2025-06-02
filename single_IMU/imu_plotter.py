import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class IMUPlotter:
    """
    Creates a 2*3 grid of real-time plots for 6-axis IMU data stored in IMUBuffer.
    """
    def __init__(self, imu_buffer, window_size: int, field = ('ax', 'ay', 'az', 'gx', 'gy', 'gz'), interval_ms: int = 10):
        self.imu_buffer = imu_buffer
        self.window_size = window_size
        self.fields = field

        # Create figure and axes
        self.fig, self.axes = plt.subplots(2, 3, figsize=(10, 8)) #row and col will change when adding more sensors
        plt.tight_layout(h_pad=2.0, w_pad=2.0)

        self.lines = []

        # Initialize each subplot with titles, labels, and an empty Line2D
        for idx, field in enumerate(self.fields):
            row = idx // 3
            col = idx % 3
            ax = self.axes[row][col]

            ax.set_title(field)
            ax.set_xlabel(f"{field}")
            if (field == 'ax') or (field == 'ay') or (field == 'az'):
                ax.set_ylabel("m/s^2")
                ax.set_ylim(-20, 20)
            else:
                ax.set_ylabel("rad/s")
                ax.set_ylim(-5, 5)
            ax.set_xlim(0, window_size)
            
            # Start with an empty line (no data yet), but label it for the legend
            line, = ax.plot([], [], label=field)
            ax.legend()
            self.lines.append(line)

        # Create the animation, calling self.update() every interval_ms
        self.ani = FuncAnimation(self.fig, self.update, interval=interval_ms, blit=True)

    def update(self, frame):
        """
        Called by FuncAnimation every interval_ms. Fetches latest data from buffer
        and updates each Line2D's x/y data, then rescales axes.
        """
        ax_data, ay_data, az_data, gx_data, gy_data, gz_data = self.imu_buffer.get_all_data()
        all_data = [ax_data, ay_data, az_data, gx_data, gy_data, gz_data]

        for line, data in zip(self.lines, all_data):
            x = range(len(data))
            line.set_data(x, data)

            # ax = line.axes
            # ax.relim()
            # ax.autoscale_view()

        return self.lines

    def show(self):
        """Displays the plot window (blocks until closed)."""
        plt.tight_layout()
        plt.show()

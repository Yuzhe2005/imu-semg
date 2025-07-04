import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class IMUPlotter:
    """
    Creates a grid of real-time plots for 6-axis IMU data stored in IMUBuffer.
    """
    def __init__(self, imu_all_buffer, window_size: int, field = ('ax', 'ay', 'az', 'gx', 'gy', 'gz'), interval_ms: int = 10):
        self.imu_all_buffer = imu_all_buffer
        self.window_size = window_size
        self.fields = field

        # Create figure and axes
        self.fig, self.axes = plt.subplots(imu_all_buffer.num, 6, figsize=(15, imu_all_buffer.num*2)) #row and col will change when adding more sensors
        plt.tight_layout(h_pad=2.0, w_pad=2.0)

        self.lines = {}

        # Initialize each subplot with titles, labels, and an empty Line2D
        for imu_idx in range(imu_all_buffer.num):
            for idx, field in enumerate(self.fields):
                ax = self.axes[imu_idx][idx]

                ax.set_title(field)
                ax.set_xlabel(f"imu {imu_idx} - {field}")
                if (field == 'ax') or (field == 'ay') or (field == 'az'):
                    ax.set_ylabel("m/s^2")
                    ax.set_ylim(-20, 20)
                else:
                    ax.set_ylabel("rad/s")
                    ax.set_ylim(-5.5, 5.5)
                ax.set_xlim(0, window_size)
                
                # Start with an empty line (no data yet), but label it for the legend
                line, = ax.plot([], [], label=field)
                ax.legend()
                self.lines[(imu_idx, field)] = line

        # Create the animation, calling self.update() every interval_ms
        self.ani = FuncAnimation(self.fig, 
                                 self.update, 
                                 interval=interval_ms, 
                                 blit=True,
                                 cache_frame_data = False)

    def update(self, frame):
        """
        Called by FuncAnimation every interval_ms. Fetches latest data from buffer
        and updates each Line2D's x/y data, then rescales axes.
        """

        for (imu_idx, field), line in self.lines.items():
            data = self.imu_all_buffer.IMU[imu_idx].get_all_data()
            
            data_field = data[field]

            line.set_data(range(len(data_field)), data_field)
        return list(self.lines.values())
        
        # for line, data in zip(self.lines, all_data):
        #     x = range(len(data))
        #     line.set_data(x, data)

            # ax = line.axes
            # ax.relim()
            # ax.autoscale_view()

        return self.lines

    def show(self):
        """Displays the plot window (blocks until closed)."""
        plt.tight_layout()
        plt.show()

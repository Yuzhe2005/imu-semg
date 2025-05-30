import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class sEMGplotter:
    def __init__(self,
                 sensor_receiver,                   
                 fields=('A0', 'A1', 'A2', 'A3'),   
                 figsize=(10, 8),                    
                 interval=10):               
    
        self.receiver = sensor_receiver
        self.fields = list(fields)

        rows, cols = len(self.fields), 1
        self.fig, axes = plt.subplots(rows, cols, figsize=figsize)

        self.axes = axes.reshape(-1)

        # if cols == 1:
        #     axes = [axes]
        # self.axes = axes

        self.lines = {}
        for i, field in enumerate(self.fields):
            ax = self.axes[i]
            ax.set_title(f"{field}")
            line, = ax.plot([], [], label=field)
            ax.legend()
            self.lines[field] = line

        self.ani = FuncAnimation(
            self.fig,
            self.update,
            interval=interval,
            cache_frame_data=False
        )

    def update(self, frame):
        self.receiver.process_chunk()

        artists = []
        for field, line in self.lines.items():
            data = list(self.receiver.data.get(field, []))
            line.set_data(range(len(data)), data)
            ax = line.axes
            ax.relim()
            ax.autoscale_view()

            artists.append(line)

        return artists

    def show(self):
        plt.tight_layout()
        plt.show()

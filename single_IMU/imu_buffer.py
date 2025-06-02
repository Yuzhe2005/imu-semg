
from collections import deque

class IMUBuffer:
    """
    Maintains six deque buffers (ax, ay, az, gx, gy, gz) of fixed window size.
    """
    def __init__(self, window_size: int):
        self.window_size = window_size
        self.data = {
            'ax': deque(maxlen=window_size),
            'ay': deque(maxlen=window_size),
            'az': deque(maxlen=window_size),
            'gx': deque(maxlen=window_size),
            'gy': deque(maxlen=window_size),
            'gz': deque(maxlen=window_size)
        }

        self.storage = {
            'ax' : [],
            'ay' : [],
            'az' : [],
            'gx' : [],
            'gy' : [],
            'gz' : []
        }

    def add_sample(self, ax_val, ay_val, az_val, gx_val, gy_val, gz_val):
        """
        Append a new 6-axis sample to each corresponding deque and storage lists.
        """
        self.data['ax'].append(ax_val)
        self.data['ay'].append(ay_val)
        self.data['az'].append(az_val)
        self.data['gx'].append(gx_val)
        self.data['gy'].append(gy_val)
        self.data['gz'].append(gz_val)
        self.storage['ax'].append(ax_val)
        self.storage['ay'].append(ay_val)
        self.storage['az'].append(az_val)
        self.storage['gx'].append(gx_val)
        self.storage['gy'].append(gy_val)
        self.storage['gz'].append(gz_val)
        

    def get_all_data(self):
        """
        Returns six lists (ax, ay, az, gx, gy, gz), each padded with zeros on the left
        if not yet full to reach window_size.
        """
        def pad_or_copy(deq):
            if len(deq) < self.window_size:
                return [0.0] * (self.window_size - len(deq)) + list(deq)
            else:
                return list(deq)

        return (
            pad_or_copy(self.data['ax']),
            pad_or_copy(self.data['ay']),
            pad_or_copy(self.data['az']),
            pad_or_copy(self.data['gx']),
            pad_or_copy(self.data['gy']),
            pad_or_copy(self.data['gz']),
        )

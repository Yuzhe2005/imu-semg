
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

    def add_sample(self, arr):
        """
        Append a new 6-axis sample to each corresponding deque and storage lists.
        """
        self.data['ax'].append(arr[0])
        self.data['ay'].append(arr[1])
        self.data['az'].append(arr[2])
        self.data['gx'].append(arr[3])
        self.data['gy'].append(arr[4])
        self.data['gz'].append(arr[5])
        self.storage['ax'].append(arr[0])
        self.storage['ay'].append(arr[1])
        self.storage['az'].append(arr[2])
        self.storage['gx'].append(arr[3])
        self.storage['gy'].append(arr[4])
        self.storage['gz'].append(arr[5])
        

    def get_all_data(self):
        """
        Returns six lists (ax, ay, az, gx, gy, gz), each padded with zeros on the left
        if not yet full to reach window_size.
        """

        def pad_or_copy(deq):
            # print("[GET_ALL_DATA CALLED]")

            if len(deq) < self.window_size:
                return [0.0] * (self.window_size - len(deq)) + list(deq)
            else:
                return list(deq)

        return {
            'ax': pad_or_copy(self.data['ax']),
            'ay': pad_or_copy(self.data['ay']),
            'az': pad_or_copy(self.data['az']),
            'gx': pad_or_copy(self.data['gx']),
            'gy': pad_or_copy(self.data['gy']),
            'gz': pad_or_copy(self.data['gz']),
        }

    def cleanStorage(self):
        self.storage = {
            'ax' : [],
            'ay' : [],
            'az' : [],
            'gx' : [],
            'gy' : [],
            'gz' : []
        }
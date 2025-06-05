# sEMG_sensor.py

import serial
from collections import deque
import sys
import time
import numpy as np
import struct

class SensorReader:
    def __init__(self, port, baudrate=1000000, timeout=1.0, window_size=1500):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=timeout)
        except Exception as e:
            raise RuntimeError(f"Connection failed {port}: {e}")
        
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

        self.window_size = window_size
        self.packet_size = 4 * 4

        self.data = {
            'A0': deque(maxlen=window_size),
            'A1': deque(maxlen=window_size),
            'A2': deque(maxlen=window_size),
            'A3': deque(maxlen=window_size)
        }

        self.storage = {
            'A0': [],
            'A1': [],
            'A2': [],
            'A3': []
        }

    def cleanStorage(self):
        self.storage = {
            'A0': [],
            'A1': [],
            'A2': [],
            'A3': []
        }

    def record(self, duration=180):
        self.cleanStorage()
        start = time.time()
        print("[Start recording]")
        try:
            while time.time() - start < duration:
                raw = self.ser.read(self.packet_size)
                if len(raw) < self.packet_size:
                    continue
                try:
                    arr = np.frombuffer(raw, dtype='<f4')
                except struct.error:
                    continue

                self.data['A0'].append(arr[0])
                self.data['A1'].append(arr[1])
                self.data['A2'].append(arr[2])
                self.data['A3'].append(arr[3])

                self.storage['A0'].append(arr[0])
                self.storage['A1'].append(arr[1])
                self.storage['A2'].append(arr[2])
                self.storage['A3'].append(arr[3])
        except Exception as e:
            print(f"Recording error: {e}", file=sys.stderr)

    def get_all_data(self):
        def pad_or_copy(deq):
            if len(deq) < self.window_size:
                return [0.0] * (self.window_size - len(deq)) + list(deq)
            else:
                return list(deq)

        return {
            'A0': pad_or_copy(self.data['A0']),
            'A1': pad_or_copy(self.data['A1']),
            'A2': pad_or_copy(self.data['A2']),
            'A3': pad_or_copy(self.data['A3']),
        }

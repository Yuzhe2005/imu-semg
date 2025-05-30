from collections import deque
import time
import struct
import serial

class SensorReader:
    def __init__(self, port, baudrate=2000000, buffer_size=4096, window_size = 2000):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=0)
        except Exception as e:
            raise RuntimeError(f"Failed to open port {port} : {e}")
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

        self.data = {
            # 'timestamp': deque(maxlen=window_size),
            'ax' : deque(maxlen=window_size),
            'ay' : deque(maxlen=window_size),
            'az' : deque(maxlen=window_size),
            'gx' : deque(maxlen=window_size),
            'gy' : deque(maxlen=window_size),
            'gz' : deque(maxlen=window_size),
        }
        self.buffer_size = buffer_size
        self.port = port
        # self.storage = {
        #     'timestamp' : [],
        #     'ax' : [],
        #     'ay' : [],
        #     'az' : [],
        #     'gx' : [],
        #     'gy' : [],
        #     'gz' : [],
        # }

    def append(self, entry):
        for key in self.data:
            try:
                self.data[key].append(entry[key])
            except Exception:
                continue

    def read_chunk(self):
        try:
            return self.ser.read(self.buffer_size)
        except Exception as e:
            print(f"[{self.ser.port}] Read error: {e}")
            return b''
        
    def process_chunk(self):
        raw = self.read_chunk()
        for entry in parse_all_data(raw):
            self.append(entry)
        
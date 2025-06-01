import serial
from collections import deque
from sEMG_parser import parse_all_data

class Receiver:
    def __init__(self, port, baudrate = 115200, buffer_size = 4096, window_size = 2000):
        # print("[Receiver Test Point]\n")
        try:
            self.ser = serial.Serial(port, baudrate, timeout = 10)
        except Exception as e:
            raise RuntimeError(f"Failed to open port {port}: {e}")
        
        # print("[Connection with 'COM17' Successful]\n")
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

        self.buffer_size = buffer_size
        self.buf = bytearray()

        self.data = {
            'A0': deque(maxlen = window_size),
            'A1': deque(maxlen = window_size),
            'A2': deque(maxlen = window_size),
            'A3': deque(maxlen = window_size)
        }

    def read_chunk(self):
        try:
            return self.ser.read(self.buffer_size)
        except Exception as e:
            print(f"Read error: {e}")
            return b''
        
    def append(self, entry):
        for key in self.data:
            try: 
                self.data[key].append(entry[key])
            except Exception:
                continue
        
    def process_chunk(self):
        raw = self.read_chunk()
        # print("[Process_chunk CheckPoint]\n")
        # print(len(raw))
        for entry in parse_all_data(raw, self.buf):
            self.append(entry)

    def close(self):
        try:
            self.ser.close()
        except Exception as e:
            print(f"[{self.ser.port}] Close error: {e}")


    
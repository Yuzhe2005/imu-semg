import serial
import time
from collections import deque

class LoadCellReader:
    def __init__(self, port, baudrate=115200, timeout=1.0, window_size = 20):
        try: 
            self.ser = serial.Serial(port, baudrate, timeout = timeout)
        except Exception as e:
            raise RuntimeError(f"Connection failed {port}: {e}")
        
        self.storage = []

        self.data = deque(maxlen = window_size)

        self.window_size = window_size
        self.running = False

    def record(self, duration = 10):
        self.storage = []
        start = time.time()
        self.running = True
        print("[Load Cell sStart recording]")
        try: 
            while self.running and (time.time() - start) < duration:
                line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                if not line:
                    continue
                parts = line.split()
                
                value = float(parts[0])
                self.storage.append(value)
                self.data.append(value)
            
            print(f"[LC Record time: {time.time() - start}s]")
        except Exception as e:
            print(f"[{self.ser.port}] Record error: {e}")
        finally:
            self.running = False

    def get_all_data(self):
        def pad_or_copy(deq):
            if len(deq) < self.window_size: 
                return [0.0] * (self.window_size - len(deq)) + list(deq)
            else:
                return list(deq)
        
        return pad_or_copy(self.data)
           

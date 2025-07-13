import serial
import time

class LoadCellReader:
    def __init__(self, weight_var, port, baudrate=115200, timeout=1.0):
        try: 
            self.ser = serial.Serial(port, baudrate, timeout = timeout)
        except Exception as e:
            raise RuntimeError(f"Connection failed {port}: {e}")
        
        self.storage = []

        self.running = False

        self.weight_var = weight_var

    def record(self, duration = 10):
        self.storage = []
        start = time.time()
        self.running = True
        print("[Load Cell sStart recording]")

        while self.running and (time.time() - start) < duration:
            try:
                line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                if not line:
                    continue
                parts = line.split()
                try:
                    value = float(parts[0])
                    self.storage.append(value)
                    unit  = parts[1] if len(parts) > 1 else ''
                    self.weight_var.set(f"{value:.3f} {unit}")
                except:
                    self.weight_var.set(f"unable to analyze: {line}")
            except serial.SerialException:
                self.weight_var.set("port closed")
                break

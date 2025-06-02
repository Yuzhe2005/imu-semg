
import serial
import threading
import struct
import numpy as np

class IMUSerialReader:
    """
    Continuously reads raw binary SixAxis packets (6 floats, little-endian)
    from a serial port and passes unpacked samples to an IMUBuffer.
    """
    def __init__(self, port: str, baudrate: int, imu_all_buffer, timeout: float = 1.0):
        """
        port: serial port name (e.g., "COM3" or "/dev/ttyACM0")
        baudrate: must match Arduino SerialUSB.begin(baudrate)
        imu_buffer: instance of IMUBuffer to store incoming samples
        timeout: serial read timeout in seconds
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.imu_all_buffer = imu_all_buffer
        self._stop_event = threading.Event()
        self.thread = threading.Thread(target=self._reader_thread, daemon=True)

        # Each packet is 6 floats = 6 * 4 bytes = 24 bytes
        self.packet_size = 4 * 6 * 3  # important: bytes

    def start(self):
        """Starts the background thread to read serial data."""
        self.thread.start()

    def stop(self):
        """Signals the reader thread to stop and waits for it to finish."""
        self._stop_event.set()
        self.thread.join()

    def _reader_thread(self):
        try:
            ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
        except serial.SerialException as e:
            print(f"ERROR: could not open serial port {self.port}: {e}")
            return

        ser.reset_input_buffer()

        # print("[START READING DATA]")
        while not self._stop_event.is_set():
            raw = ser.read(self.packet_size)
            if len(raw) < self.packet_size:
                continue  # incomplete packet or timeout
            try:
                arr = np.frombuffer(raw, dtype='<f4')
            except struct.error:
                continue  # skip malformed data

            self.imu_all_buffer.add_all_sample(arr)
            # print("[DATA ADDED]")

        ser.close()

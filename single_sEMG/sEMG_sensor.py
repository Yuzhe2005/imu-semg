# sEMG_sensor.py
import serial

def open_serial(port: str, baud: int = 1000000, timeout: float = 1.0):
    """Open and return a serial.Serial instance."""
    ser = serial.Serial(port, baud, timeout=timeout)
    return ser

def read_emg(ser):
    """
    Read one line of EMG data from serial, parse float voltage.
    Returns None if no valid data.
    """
    line = ser.readline().decode('ascii', errors='ignore').strip()
    if not line:
        return None
    try:
        return float(line)
    except ValueError:
        return None

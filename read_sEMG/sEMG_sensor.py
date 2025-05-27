import serial


def open_serial(port: str, baud: int = 115200, timeout: float = 1.0):
    """Open and return a serial.Serial instance."""
    ser = serial.Serial(port, baud, timeout=timeout)
    return ser


def read_emg(ser):
    """
    Read one line of EMG data from serial, parse float voltage.
    Returns None if no valid data or port is closed.
    """
    if not ser or not ser.is_open:
        return None
    try:
        line = ser.readline().decode('ascii', errors='ignore').strip()
    except Exception:
        return None

    if not line:
        return None
    try:
        return float(line)
    except ValueError:
        return None

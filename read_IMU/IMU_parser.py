import struct

SYNC = b'\xAA\xBB'

def parse_all_data(raw_bytes):
    FRAME_SIZE = 12
    L = len(raw_bytes)


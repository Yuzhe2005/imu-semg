import struct

def parse_all_data(raw_bytes):


    SYNC = b'\xAA\x55'

    results = []

    # buf = b''
    buf = bytearray()

    for b in raw_bytes:
        print("[Parse_all_data Check Point] This is the a byte of 'raw_bytes'\n")
        print(b)
        # print(raw_bytes[1])
        # try:
        buf.append(b)
        # except Exception as e:
        #     print("这里有错")

        idx = buf.find(SYNC)
        if idx < 0:
            continue
        
        if len(buf) < idx + 10:
            buf = buf[idx:]
            continue
        frame = buf[idx+2:idx+10]
        buf = buf[idx+10:]
        vals = struct.unpack('<4H', frame)
        results.append({'A0': vals[0], 'A1': vals[1], 'A2': vals[2], 'A3': vals[3]})
    
    return results


    
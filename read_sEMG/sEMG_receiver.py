import serial
import threading
from collections import deque
import struct
import time

class ReceiverThreaded:
    """
    用一个后台线程不断从串口读数据、解析成 4 通道的数值，并 append 到各自的 deque。
    主线程只需“读”这些 deque，不再做任何串口 I/O。
    """

    def __init__(self, port, baudrate=115200, buffer_size=4096, window_size=500):
        """
        Args:
          port        : 串口号，例如 "COM3" 或 "/dev/ttyUSB0"
          baudrate    : 波特率，需与 Arduino 端 Serial.begin 保持一致
          buffer_size : 每次从串口尝试读取的最大字节数
          window_size : 每个通道保留的样本数量（滚动窗口大小）
        """
        # 1) 打开串口
        try:
            self.ser = serial.Serial(port, baudrate, timeout=0.01)
        except Exception as e:
            raise RuntimeError(f"Failed to open port {port}: {e}")

        # 2) 清空输入缓存
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

        self.buffer_size = buffer_size
        self.window_size = window_size

        # 3) 四个 deque：存放最近 window_size 个样本
        self.data = {
            'A0': deque([0]*window_size, maxlen=window_size),
            'A1': deque([0]*window_size, maxlen=window_size),
            'A4': deque([0]*window_size, maxlen=window_size),
            'A3': deque([0]*window_size, maxlen=window_size),
        }

        # 4) 内部字节缓冲区，用来拼凑不完整的帧
        self._buf = bytearray()
        self._SYNC = b'\xAA\x55'
        self._struct = struct.Struct('<4H')

        # 5) 用于控制后台线程循环的停止标志
        self._stop_event = threading.Event()

        # 6) 创建并启动后台读取线程
        self._thread = threading.Thread(target=self._read_loop, daemon=True)
        self._thread.start()

    def _read_loop(self):
        """
        后台线程函数：不断读取串口字节、累积到 self._buf，
        只要发现完整帧 (SYNC + 8 字节 payload) 就解包并 append 到 deque。
        如果 stop_event 被 set，就跳出循环，线程结束。
        """
        while not self._stop_event.is_set():
            try:
                raw = self.ser.read(self.buffer_size)
            except Exception as e:
                print(f"Serial read error: {e}")
                raw = b''

            if raw:
                self._buf.extend(raw)

                # 不断查找 sync 标记并提取完整帧
                idx = self._buf.find(self._SYNC)
                while idx >= 0 and len(self._buf) >= idx + 10:
                    # 提取帧中的 8 字节数据
                    frame = self._buf[idx+2 : idx+10]
                    # 删除已经处理过的字节
                    del self._buf[: idx + 10]

                    try:
                        v0, v1, v2, v3 = self._struct.unpack(frame)
                    except struct.error:
                        # 如果解包失败，就跳过这次，继续寻找下一个 sync
                        idx = self._buf.find(self._SYNC)
                        continue

                    # 将解析到的四通道数据分别 append 到对应 deque
                    self.data['A0'].append(v0)
                    self.data['A1'].append(v1)
                    self.data['A4'].append(v2)
                    self.data['A3'].append(v3)

                    # 继续查找下一帧
                    idx = self._buf.find(self._SYNC)
            else:
                # 如果这次没读到字节，稍微 sleep 下，避免 CPU 占满
                time.sleep(0.001)

        # End of loop：如果 stop_event 已被 set，就退出线程
        # 串口最后在 close() 里关闭

    def close(self):
        """
        停止后台线程并关闭串口。
        """
        # 1) 通知线程停止
        self._stop_event.set()
        # 2) 等待线程真正结束
        self._thread.join(timeout=1.0)
        # 3) 关闭串口
        try:
            self.ser.close()
        except Exception as e:
            print(f"[{self.ser.port}] Close error: {e}")

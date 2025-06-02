from imu_single_buffer import IMUBuffer

class IMUAllBuffer:

    def __init__(self, IMU0, IMU1):
        self.IMU0 = IMU0
        self.IMU1 = IMU1

    def add_all_sample(self, arr):
        self.IMU0.add_sample(arr[:6])
        self.IMU1.add_sample(arr[-6:])




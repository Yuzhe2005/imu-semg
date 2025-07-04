# from imu_single_buffer import IMUBuffer

class IMUAllBuffer:

    def __init__(self, IMU0, IMU1, IMU2, IMU3):
        self.num = 4
        self.IMU = [IMU0, IMU1, IMU2, IMU3]

    def add_all_sample(self, arr):
        self.IMU[0].add_sample(arr[:6])
        self.IMU[1].add_sample(arr[6:12])
        self.IMU[2].add_sample(arr[12:18])
        self.IMU[3].add_sample(arr[-6:])

    def cleanStorage(self):
        self.IMU[0].cleanStorage()
        self.IMU[1].cleanStorage()
        self.IMU[2].cleanStorage()
        self.IMU[3].cleanStorage()



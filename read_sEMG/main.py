import matplotlib.pyplot as plt
from sEMG_plotter import sEMGplotter
from sEMG_receiver import Receiver
from collections import deque

def main():
    re = Receiver('COM17', buffer_size = 2000)
    # print("[Test Point 1]\n")

    re.process_chunk();
    # test = re.data['A0']
    # print(test)

    plotter = sEMGplotter(re)
    plotter.show()

if __name__ == '__main__':
    main()
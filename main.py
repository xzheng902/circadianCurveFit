# main.py
# Mike Zheng
# 2/13/19

import sys
import numpy as np
import matplotlib.pyplot as plt

import data
import analysis

def main(argv):
    if len(argv) < 2:
        print( 'Usage: python3 %s <csv filename>' % (argv[0]))
        exit(0)

    expList = data.read(argv[1])

    if len(argv) == 3:
        idx = int(argv[2])
        if idx>len(expList)-1:
            idx = len(expList)-1
    else:
        idx = 0

    print(expList[idx])
    # non-linear curve fit
    params = analysis.least_squares_Hirota(expList[idx])
    x = np.linspace(24, 96, 500)
    y = analysis.obj_func_Hirota(x, params[0], params[1], params[2], params[3], params[4], params[5])
    # red fit
    plt.plot(x, y, 'r-')

    # blue raw data
    plt.plot(expList[idx].getdata()[:,0], expList[idx].getdata()[:,1], 'b-')
    plt.show()

if __name__ == "__main__":
    main(sys.argv)

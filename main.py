# main.py
# Mike Zheng
# 2/13/19

import sys
import numpy as np
import matplotlib.pyplot as plt

import data
import analysis
import accuracy

def main(argv):
    if len(argv) < 2:
        print( 'Usage: python3 %s <csv filename> <optional numtest>' % (argv[0]))
        exit(0)

    expList = data.read(argv[1])

    if len(argv) == 3:
        idx = int(argv[2])
        if idx>len(expList)-1:
            idx = len(expList)-1
    else:
        idx = -1

    # if input index, then plot that exp
    if idx >= 0:
        print(expList[idx])
        # non-linear curve fit
        params = analysis.least_squares_Hirota(expList[idx])
        x = np.array(expList[idx].getdata()[:,0])
        y_data = np.array(expList[idx].getdata()[:,1])
        y_exp = analysis.obj_func_Hirota(x, params[0], params[1], params[2], params[3], params[4], params[5])

        # make figure
        fig = plt.figure()
        ax = fig.add_subplot(111)
        # red fit
        ax.plot(x, y_exp, 'r-')
        # blue raw data
        ax.plot(x, y_data, 'b-')
        ax.text(0.5, 0.95, "Period = %.2f" % params[4], horizontalalignment='center',verticalalignment='center', transform=ax.transAxes, fontsize=8)
        rmse = accuracy.rmse(y_data, y_exp)
        rsquare = accuracy.rsquare(y_data, y_exp)
        ax.text(0.5, 0.9, "RMSE = %.4f R^2 = %.4f" % (rmse, rsquare) , horizontalalignment='center',verticalalignment='center', transform=ax.transAxes, fontsize=8)
        plt.show()
    # otherwise plot all experiments in the list
    else:
        fig = plt.figure()
        # calculate the layout n*4
        numRows = int(len(expList)/4)
        if len(expList)%4>0:
            numRows += 1
        for i in range(len(expList)):
            params = analysis.least_squares_Hirota(expList[i])
            x = np.array(expList[i].getdata()[:,0])
            y_data = np.array(expList[i].getdata()[:,1])
            y_exp = analysis.obj_func_Hirota(x, params[0], params[1], params[2], params[3], params[4], params[5])
            ax = fig.add_subplot(numRows, 4, i+1)
            # red fit
            ax.plot(x, y_exp, 'r-')
            # blue raw data
            ax.plot(x, y_data, 'b-')
            ax.text(0.5, 0.95, "Period = %.2f" % params[4], horizontalalignment='center',verticalalignment='center', transform=ax.transAxes, fontsize=6)
            rmse = accuracy.rmse(y_data, y_exp)
            rsquare = accuracy.rsquare(y_data, y_exp)
            ax.text(0.5, 0.85, "RMSE = %.4f R^2 = %.4f" % (rmse, rsquare) , horizontalalignment='center',verticalalignment='center', transform=ax.transAxes, fontsize=6)

        plt.show()



if __name__ == "__main__":
    main(sys.argv)

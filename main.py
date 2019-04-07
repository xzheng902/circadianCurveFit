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
        x = np.array(expList[idx].processData()[:,0])
        y_data = np.array(expList[idx].processData()[:,1])
        # make figure
        fig = plt.figure()
        ax = fig.add_subplot(111)
        # blue raw data
        ax.plot(x, y_data, 'b-')
        params = analysis.least_squares_Hirota(expList[idx])
        if params is None:
            print("Curve_fit failed for experiemnt "+str(idx))
        else:
            y_exp = analysis.obj_func_Hirota(x, params[0], params[1], params[2], params[3], params[4], params[5])
            # red fit
            ax.plot(x, y_exp, 'r-')
            ax.text(0.5, 0.95, "Period = %.2f" % params[4], horizontalalignment='center',verticalalignment='center', transform=ax.transAxes, fontsize=8)
            rmse = accuracy.rmse(y_data, y_exp)
            rsquare = accuracy.rsquare(y_data, y_exp)
            try:
                peakDiffSquare = accuracy.peakDiffSquare(x, y_data, y_exp, params[3], params[4])
                ax.text(0.5, 0.85, "RMSE = %.4f R^2 = %.4f\n PeakSquareDiff = %.4f" % (rmse, rsquare, peakDiffSquare) , horizontalalignment='center',verticalalignment='center', transform=ax.transAxes, fontsize=6)
            except:
                print("Unable to compute peakDiffSquare for experiment index "+str(idx))
                ax.text(0.5, 0.85, "RMSE = %.4f R^2 = %.4f" % (rmse, rsquare) , horizontalalignment='center',verticalalignment='center', transform=ax.transAxes, fontsize=6)
        plt.show()
    # otherwise plot all experiments in the list
    else:
        fig = plt.figure()
        # calculate the layout n*4
        numRows = int(len(expList)/4)
        if len(expList)%4>0:
            numRows += 1
        for i in range(len(expList)):
            x = np.array(expList[i].processData()[:,0])
            y_data = np.array(expList[i].processData()[:,1])
            params = analysis.least_squares_Hirota(expList[i])
            ax = fig.add_subplot(numRows, 4, i+1)
            # blue raw data
            ax.plot(x, y_data, 'b-')
            if params is None:
                print("Curve_fit failed for experiemnt "+str(i))
                continue
            y_exp = analysis.obj_func_Hirota(x, params[0], params[1], params[2], params[3], params[4], params[5])
            # red fit
            ax.plot(x, y_exp, 'r-')
            ax.text(0.5, 0.95, "Period = %.2f" % params[4], horizontalalignment='center',verticalalignment='center', transform=ax.transAxes, fontsize=6)
            rmse = accuracy.rmse(y_data, y_exp)
            rsquare = accuracy.rsquare(y_data, y_exp)
            try:
                peakDiffSquare = accuracy.peakDiffSquare(x, y_data, y_exp, params[3], params[4])
                ax.text(0.5, 0.85, "RMSE = %.4f R^2 = %.4f\n PeakSquareDiff = %.4f" % (rmse, rsquare, peakDiffSquare) , horizontalalignment='center',verticalalignment='center', transform=ax.transAxes, fontsize=6)
            except:
                print("Unable to compute peakDiffSquare for experiment index "+str(i))
                ax.text(0.5, 0.85, "RMSE = %.4f R^2 = %.4f" % (rmse, rsquare) , horizontalalignment='center',verticalalignment='center', transform=ax.transAxes, fontsize=6)

        plt.show()



if __name__ == "__main__":
    main(sys.argv)

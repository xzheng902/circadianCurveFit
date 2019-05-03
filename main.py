# main.py
# Mike Zheng
# 2/13/19

import sys
import numpy as np
import matplotlib.pyplot as plt

import data
import analysis
import accuracy
import residual_analysis

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
        ax.plot(x, y_data, label="data")
        # params = analysis.least_squares_Hirota(expList[idx])
        params_fit0 = analysis.fit0(x, y_data)
        # params_fit0 = analysis.fit0(np.array(expList[idx].windowBaselinedData()[:,0]), np.array(expList[idx].windowBaselinedData()[:,1]))
        # print("old hirota params: ",params)
        # print("fit0 params: ", params_fit0)
        if params_fit0 is None:
            print("fit0 failed for experiemnt "+str(idx))
        else:
            y_exp = analysis.obj_func_Hirota(x, params_fit0[0], params_fit0[1], params_fit0[2], params_fit0[3], params_fit0[4], params_fit0[5])
            # red fit
            ax.plot(x, y_exp, label="fit0")
        params_fit1 = analysis.fit1(x, y_data)
        if params_fit1 is None:
            print("fit1 failed for experiemnt "+str(idx))
        else:
            y_exp = analysis.obj_func_Hirota(x, params_fit1[0], params_fit1[1], params_fit1[2], params_fit1[3], params_fit1[4], params_fit1[5])
            ax.plot(x, y_exp, label="fit1")
        # params_fit2 = analysis.fit2(x, y_data)
        # if params_fit2 is None:
        #     print("fit2 failed for experiemnt "+str(idx))
        # else:
        #     y_exp = analysis.obj_func_Hirota(x, params_fit2[0], params_fit2[1], params_fit2[2], params_fit2[3], params_fit2[4], params_fit2[5])
        #     ax.plot(x, y_exp, label="fit2")
        # params_fit4 = analysis.fit4(x, y_data)
        # if params_fit4 is None:
        #     print("fit4 failed for experiemnt "+str(idx))
        # else:
        #     y_exp = analysis.obj_func_Hirota(x, params_fit4[0], params_fit4[1], params_fit4[2], params_fit4[3], params_fit4[4], params_fit4[5])
        #     ax.plot(x, y_exp, label="fit4")
        plt.legend()
            # green residual
            # ax.plot(x, y_data-y_exp, 'g-')
            # residual_analysis.residual_fft(y_data-y_exp)
            # ax.text(0.5, 0.95, "Period = %.2f" % params[4], horizontalalignment='center',verticalalignment='center', transform=ax.transAxes, fontsize=8)
            # rmse = accuracy.rmse(y_data, y_exp)
            # rsquare = accuracy.rsquare(y_data, y_exp)
            # rsquare_damp = accuracy.rsquare_damp(y_data, y_exp, x, params[2])
            # try:
            #     peakDiffSquare = accuracy.peakDiffSquare(x, y_data, y_exp, params[3], params[4])
            #     ax.text(0.5, 0.85, "RMSE = %.4f R^2 = %.4f R^2d = %.4f\n PeakSquareDiff = %.4f" % (rmse, rsquare, rsquare_damp, peakDiffSquare) , horizontalalignment='center',verticalalignment='center', transform=ax.transAxes, fontsize=6)
            # except:
            #     print("Unable to compute peakDiffSquare for experiment index "+str(idx))
            #     ax.text(0.5, 0.85, "RMSE = %.4f R^2 = %.4f R^2d = %.4f" % (rmse, rsquare, rsquare_damp) , horizontalalignment='center',verticalalignment='center', transform=ax.transAxes, fontsize=6)
            # output = accuracy.criteria(params[4], rsquare, rsquare_damp)
            # ax.text(0.8, 0.8, output, horizontalalignment='center',verticalalignment='center', transform=ax.transAxes, fontsize=12)
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
            rsquare_damp = accuracy.rsquare_damp(y_data, y_exp, x, params[2])
            try:
                peakDiffSquare = accuracy.peakDiffSquare(x, y_data, y_exp, params[3], params[4])
                ax.text(0.5, 0.85, "RMSE = %.4f R^2 = %.4f R^2d = %.4f\n PeakSquareDiff = %.4f" % (rmse, rsquare, rsquare_damp, peakDiffSquare) , horizontalalignment='center',verticalalignment='center', transform=ax.transAxes, fontsize=6)
            except:
                print("Unable to compute peakDiffSquare for experiment index "+str(i))
                # ax.text(0.5, 0.85, "RMSE = %.4f R^2 = %.4f R^2d = %.4f" % (rmse, rsquare, rsquare_damp) , horizontalalignment='center',verticalalignment='center', transform=ax.transAxes, fontsize=6)
            output = accuracy.criteria(params[4], rsquare, rsquare_damp)
            ax.text(0.8, 0.7, output, horizontalalignment='center',verticalalignment='center', transform=ax.transAxes, fontsize=12)

        plt.show()



if __name__ == "__main__":
    main(sys.argv)

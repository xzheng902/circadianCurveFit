# main_batch.py
# Mike Zheng
# 3/8/19

# run analysis on a directory

import sys
import numpy as np
import matplotlib.pyplot as plt

import data
import analysis
import accuracy
import readdir

def main(argv):
    if len(argv) < 2:
        print( 'Usage: python3 %s <directory name>' % (argv[0]))
        exit(0)

    filels = readdir.readdir(argv[1])
    if len(filels) == 0:
        print("No file in directory")
        exit(0)

    exps = []
    periods = []
    rmses = []
    rsquares = []
    peakDiffSquares = []


    for file in filels:
        expList = data.read(file)
        for i in range(len(expList)):
            x = np.array(expList[i].processData()[:,0])
            y_data = np.array(expList[i].processData()[:,1])
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.plot(x, y_data, 'b-')
            params = analysis.least_squares_Hirota(expList[i])
            if params is None:
                print("Curve_fit failed for experiemnt "+str(i))
                rmses.append(-1)
                rsquares.append(-1)
                peakDiffSquares.append(-1)
                exp = file.split('/')[-1][:-4]+"_"+str(i)
                exps.append(exp)
                periods.append(-1)
                continue
            y_exp = analysis.obj_func_Hirota(x, params[0], params[1], params[2], params[3], params[4], params[5])
            ax.plot(x, y_exp, 'r-')
            # green residual
            ax.plot(x, y_data-y_exp, 'g-')
            ax.text(0.5, 0.95, "Period = %.2f" % params[4], horizontalalignment='center',verticalalignment='center', transform=ax.transAxes, fontsize=8)
            rmse = accuracy.rmse(y_data, y_exp)
            rsquare = accuracy.rsquare(y_data, y_exp)
            try:
                peakDiffSquare = accuracy.peakDiffSquare(x, y_data, y_exp, params[3], params[4])
                ax.text(0.5, 0.85, "RMSE = %.4f R^2 = %.4f\n PeakSquareDiff = %.4f" % (rmse, rsquare, peakDiffSquare) , horizontalalignment='center',verticalalignment='center', transform=ax.transAxes, fontsize=6)
            except:
                print("Unable to compute peakDiffSquare for experiment index "+str(i))
                ax.text(0.5, 0.85, "RMSE = %.4f R^2 = %.4f" % (rmse, rsquare) , horizontalalignment='center',verticalalignment='center', transform=ax.transAxes, fontsize=6)
                peakDiffSquare = -1
            rmses.append(rmse)
            rsquares.append(rsquare)
            peakDiffSquares.append(peakDiffSquare)
            exp = file.split('/')[-1][:-4]+"_"+str(i)
            exps.append(exp)
            periods.append(params[4])
            fig.savefig("res_"+exp, dpi=600)
            plt.close(fig)

            # plt.show()

    results = np.matrix([rmses, rsquares, peakDiffSquares]).T
    fp = open('results.csv', 'w')
    fp.write('exp, period, rmse, rsquare, peakDiffSquare\n')
    for i in range(results.shape[0]):
        fp.write(str(exps[i])+','+str(periods[i])+','+str(results[i,0])+','+str(results[i,1])+','+str(results[i,2])+'\n')

    fp.close()



if __name__ == "__main__":
    main(sys.argv)

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
import residual_analysis

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
    rsquare_damps = []
    peakDiffSquares = []
    outputs = []
    dates = []

    params_full = []

    for file in filels:
        expList = data.read(file)
        for i in range(len(expList)):
            x = np.array(expList[i].processData()[:,0])
            y_data = np.array(expList[i].processData()[:,1])
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.plot(x, y_data, 'b-')
            params = analysis.fit_hirota(x, y_data)
            params_full.append(params)
            if params is None:
                print("Curve_fit failed for experiemnt "+str(i))
                rmses.append(-1)
                rsquares.append(-1)
                rsquare_damps.append(-1)
                peakDiffSquares.append(-1)
                exp = file.split('/')[-1][:-4]+"_"+str(i)
                exps.append(exp)
                dates.append(expList[i].date)
                periods.append(-1)
                outputs.append(False)
                fig.savefig(exp, dpi=600)
                continue
            y_exp = analysis.obj_func_Hirota(x, params[0], params[1], params[2], params[3], params[4], params[5])
            ax.plot(x, y_exp, 'r-')
            # # green residual
            # ax.plot(x, y_data-y_exp, 'g-')
            ax.text(0.5, 0.95, "Period = %.2f" % params[4], horizontalalignment='center',verticalalignment='center', transform=ax.transAxes, fontsize=8)
            rmse = accuracy.rmse(y_data, y_exp)
            rsquare = accuracy.rsquare(y_data, y_exp)
            rsquare_damp = accuracy.rsquare_damp(y_data, y_exp, x, params[2])
            try:
                peakDiffSquare = accuracy.peakDiffSquare(x, y_data, y_exp, params[3], params[4])
                ax.text(0.5, 0.85, "RMSE = %.4f R^2 = %.4f R^2d = %.4f\n PeakSquareDiff = %.4f" % (rmse, rsquare, rsquare_damp, peakDiffSquare) , horizontalalignment='center',verticalalignment='center', transform=ax.transAxes, fontsize=6)
            except:
                print("Unable to compute peakDiffSquare for experiment index "+str(i))
                ax.text(0.5, 0.85, "RMSE = %.4f R^2 = %.4f R^2d = %.4f" % (rmse, rsquare, rsquare_damp) , horizontalalignment='center',verticalalignment='center', transform=ax.transAxes, fontsize=6)
                peakDiffSquare = -1
            output = accuracy.criteria(params[4], rsquare, rsquare_damp)
            outputs.append(output)
            ax.text(0.8, 0.78, output, horizontalalignment='center',verticalalignment='center', transform=ax.transAxes, fontsize=12)
            rmses.append(rmse)
            rsquares.append(rsquare)
            rsquare_damps.append(rsquare_damp)
            peakDiffSquares.append(peakDiffSquare)
            exp = file.split('/')[-1][:-4]+"_"+str(i)
            exps.append(exp)
            dates.append(expList[i].date)
            periods.append(params[4])
            fig.savefig(exp, dpi=600)
            plt.close(fig)


            # plt.show()

    results = np.matrix([rmses, rsquares, rsquare_damps, peakDiffSquares]).T
    fp = open('results.csv', 'w')
    fp.write('exp, period, rmse, rsquare, rsqare_damp, peakDiffSquare\n')
    for i in range(results.shape[0]):
        fp.write(str(exps[i])+','+str(periods[i])+','+str(results[i,0])+','+str(results[i,1])+','+str(results[i,2])+','+str(results[i,3])+'\n')
    fp.close()

    fp = open('results_good.csv', 'w')
    fp.write('exp, date, baseline, amplitude, damp, phase, period, trend\n')
    for i in range(results.shape[0]):
        if outputs[i] is True:
            fp.write(str(exps[i])+','+str(dates[i])+','+str(params_full[i][0])+','+str(params_full[i][1])+','+str(params_full[i][2])+','+str(params_full[i][3])+','+str(params_full[i][4])+','+str(params_full[i][5])+'\n')
    fp.close()




if __name__ == "__main__":
    main(sys.argv)

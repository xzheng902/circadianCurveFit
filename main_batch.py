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

    rmses = []
    rsquares = []
    peakDiffSquares = []


    for file in filels:
        expList = data.read(file)
        for i in range(len(expList)):
            x = np.array(expList[i].getdata()[:,0])
            y_data = np.array(expList[i].getdata()[:,1])
            params = analysis.least_squares_Hirota(expList[i])
            if params is None:
                print("Curve_fit failed for experiemnt "+str(i))
                rmses.append(-1)
                rsquares.append(-1)
                peakDiffSquares.append(-1)
                continue
            y_exp = analysis.obj_func_Hirota(x, params[0], params[1], params[2], params[3], params[4], params[5])
            rmse = accuracy.rmse(y_data, y_exp)
            rsquare = accuracy.rsquare(y_data, y_exp)
            try:
                peakDiffSquare = accuracy.peakDiffSquare(x, y_data, y_exp, params[3], params[4])
            except:
                peakDiffSquare = -1
            rmses.append(rmse)
            rsquares.append(rsquare)
            peakDiffSquares.append(peakDiffSquare)

    results = np.matrix([rmses, rsquares, peakDiffSquares]).T
    # fp = open(argv[1]+'/results.csv', 'w')
    # fp.write('rmse, rsquare, peakDiffSquare\n')
    # for i in range(results.shape[0]):
    #     fp.write(str(results[i,0])+','+str(results[i,1])+','+str(results[i,2])+'\n')
    #
    # fp.close()



if __name__ == "__main__":
    main(sys.argv)

# accuracy.py
# Mike Zheng
# 2/23/19

# library of accuracy measures

import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt

# root mean square error (rmse)
def rmse(obs, exp):
    residual = exp-obs
    mse = np.mean(np.square(residual))
    rmse = np.sqrt(mse)
    return rmse

# rsquare
def rsquare(obs, exp):
    residual = exp-obs
    sse = np.sum(np.square(residual))
    mean = np.mean(obs)
    sst = np.sum(np.square(obs-mean))
    return 1-sse/sst

# calculate the sum of sqaure of peak difference
def peakDiffSquare(x, obs, exp, exp_phase, exp_period):
    # find the exp peaks based on cosine phase + period
    exp_peaks_formula = []
    exp_peaks_formula_idx = []
    exp_peak = exp_phase
    while (exp_peak > 24):
        exp_peak -= exp_period/2
    exp_peak += exp_period/2
    while (exp_peak < 96):
        exp_peaks_formula.append(exp_peak)
        exp_peaks_formula_idx.append(np.rint(exp_peak*6)-144)
        exp_peak += exp_period/2
    # print(exp_peaks_formula)
    # print(exp_peaks_formula_idx)

    # find the exp peaks based on exp data
    exp_peaks_real = []
    exp_peaks_real_idx = []
    diff0 = exp[1]-exp[0]
    for i in range(1, exp.shape[0]-1):
        diff1 = exp[i+1]-exp[i]
        if (diff0*diff1 < 0):
            exp_peaks_real.append(x[i,0])
            exp_peaks_real_idx.append(i)
        diff0 = diff1
    # print(exp_peaks_real)
    # print(exp_peaks_real_idx)

    # use exp peaks from exp data (not cosine formula)
    # 6 hour window
    obs_peaks = findObsPeaksIdx(x, obs, exp_peaks_real_idx, 36)
    exp_peaks = findObsPeaksIdx(x, exp, exp_peaks_real_idx, 36)

    return np.sum(np.square(np.matrix(obs_peaks)-np.matrix(exp_peaks)))


def parabola(x, a, b, c):
    return a*x*x + b*x + c

# peak detection
# window around expected peaks, model with parabola, find actual peak
def findObsPeaksIdx(x, obs, exp_peaks_idx, window):
    peaks = []
    # plt.plot(x, obs, '-b')

    for exp_peak_idx in exp_peaks_idx:
        # print(exp_peak_idx)
        windowx = x[(int)(exp_peak_idx-window/2):(int)(exp_peak_idx+window/2), 0]
        windowy = obs[(int)(exp_peak_idx-window/2):(int)(exp_peak_idx+window/2), 0]
        # print(windowy)
        popt, pcov = scipy.optimize.curve_fit(parabola, windowx, windowy)
        peaks.append(-popt[1]/(2*popt[0]))
        # # plot
        # parabolay = parabola(windowx, popt[0], popt[1], popt[2])
        # plt.plot(windowx, windowy, '-r')
        # plt.plot(windowx, parabolay, '-g')

    # plt.show()
    return peaks

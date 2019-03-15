# analysis.py
# Mike Zheng
# 2/13/19

# library of analysis functions

import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt

import data

# nonlinear least squares curvefitting
# based on Hirota et al. 2008
def obj_func_Hirota(x, baseline, amplitude, damp, phase, period, trend):
    return baseline + amplitude*(np.exp(- damp*x))*np.cos(2*np.pi*(x-phase)/period) + trend*x

def least_squares_Hirota(full_data):
    # get data from 24-96 hours
    npdata = full_data.windowBaselinedData()
    # find mid point
    midIdx = int(npdata.shape[0]/2)

    est_period = 24.0
    est_damp = 0.005
    # estimate trend (slope of the medians of the first half and that of the second half)
    first_half_medians = np.median(npdata[:midIdx,:], axis=0).tolist()[0]
    second_half_medians = np.median(npdata[midIdx:,:], axis=0).tolist()[0]
    est_trend = (second_half_medians[1]-first_half_medians[1])/(second_half_medians[0]-first_half_medians[0])
    # estimate baseline
    est_baseline = np.median(npdata, axis=0)[0,1]
    # estimate phase
    # FIX this
    est_phase = npdata[np.argmax(npdata, 0)[0,1],0]
    # estimate amplitude
    est_amp = (np.max(npdata,axis=0)[0,1]-np.min(npdata, axis=0)[0,1])/2

    # curve fit
    try:
        popt, pcov = scipy.optimize.curve_fit(obj_func_Hirota, np.array(npdata[:,0]).flatten(), np.array(npdata[:,1]).flatten(), p0=[est_baseline, est_amp, est_damp, est_phase, est_period, est_trend])
    except:
        return None


    return popt

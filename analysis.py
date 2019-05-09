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
# use this func as model
def obj_func_Hirota(x, baseline, amplitude, damp, phase, period, trend):
    return baseline + amplitude*(np.exp(- damp*x))*np.cos(2*np.pi*(x-phase)/period) + trend*x

# takes in full Data object
# does not do remove outlier, smooth, detrend etc.
# NOT CURRENT
def least_squares_Hirota(full_data):
    # get data from 24-96 hours
    npdata = full_data.windowBaselinedData()
    # print(npdata.shape)
    # find mid point
    midIdx = int(npdata.shape[0]/2)

    est_period = 24.0
    est_damp = 0.005
    # estimate trend (slope of the medians of the first half and that of the second half)
    first_half_medians = np.median(npdata[:midIdx,:], axis=0).tolist()[0]
    second_half_medians = np.median(npdata[midIdx:,:], axis=0).tolist()[0]
    # print(first_half_medians, second_half_medians)
    est_trend = (second_half_medians[1]-first_half_medians[1])/(second_half_medians[0]-first_half_medians[0])
    # estimate baseline
    est_baseline = np.median(npdata, axis=0)[0,1]
    # print(est_baseline)
    # estimate phase
    # FIX this
    est_phase = npdata[np.argmax(npdata, 0)[0,1],0]
    # print(est_phase)
    # estimate amplitude
    est_amp = (np.max(npdata,axis=0)[0,1]-np.min(npdata, axis=0)[0,1])/2
    # print(est_amp)
    # print(est_trend, est_baseline, est_phase, est_amp)


    # curve fit
    try:
        popt, pcov = scipy.optimize.curve_fit(obj_func_Hirota, np.array(npdata[:,0]).flatten(), np.array(npdata[:,1]).flatten(), p0=[est_baseline, est_amp, est_damp, est_phase, est_period, est_trend])
    except:
        return None

    return popt


# fit hirota
def fit_hirota(x, y):
    # print(x.shape)
    # print(y.shape)
    midIdx = int(x.shape[0]/2)
    est_period = 24.0
    est_damp = 0.005
    # estimate trend (slope of the medians of the first half and that of the second half)
    first_half_medians_y = np.median(y[:midIdx,:])
    second_half_medians_x = np.median(x[midIdx:,:])
    second_half_medians_y = np.median(y[midIdx:,:])
    first_half_medians_x = np.median(x[:midIdx,:])
    # print(first_half_medians_x, first_half_medians_y, second_half_medians_x, second_half_medians_y)
    est_trend = (second_half_medians_y-first_half_medians_y)/(second_half_medians_x-first_half_medians_x)
    # print(est_trend)
    # estimate baseline
    est_baseline = np.median(y)
    # print(est_baseline)
    # # estimate phase
    # # FIX this
    est_phase = x[np.argmax(y)][0]
    # print(est_phase)
    # estimate amplitude
    est_amp = (np.max(y)-np.min(y))/2
    # print(est_amp)

    # curve fit
    try:
        popt, pcov = scipy.optimize.curve_fit(obj_func_Hirota, x.flatten(), y.flatten(), p0=[est_baseline, est_amp, est_damp, est_phase, est_period, est_trend])
    except:
        return None

    return popt


# analysis code 5 methods

# fit0
# based on original Hirota
# fit y-(e^(-lambda*t)*A*cos(2*pi*(x-phase)/period)+trend*x+baseline) -> 0
def obj_func_fit0(params, x,y):
    baseline = params[0]
    amplitude = params[1]
    damp = params[2]
    phase = params[3]
    period = params[4]
    trend = params[5]
    sine = amplitude*np.cos(2*np.pi*(x-phase)/period)
    return ((y - np.exp(- damp*x)*sine + trend*x+baseline)).T[0,:]

# fit0
def fit0(x, y):
    # print(x.shape)
    # print(y.shape)
    midIdx = int(x.shape[0]/2)
    est_period = 24.0
    est_damp = 0.005
    # estimate trend (slope of the medians of the first half and that of the second half)
    first_half_medians_y = np.median(y[:midIdx,:])
    second_half_medians_x = np.median(x[midIdx:,:])
    second_half_medians_y = np.median(y[midIdx:,:])
    first_half_medians_x = np.median(x[:midIdx,:])
    # print(first_half_medians_x, first_half_medians_y, second_half_medians_x, second_half_medians_y)
    est_trend = (second_half_medians_y-first_half_medians_y)/(second_half_medians_x-first_half_medians_x)
    # print(est_trend)
    # estimate baseline
    est_baseline = np.median(y)
    # print(est_baseline)
    # # estimate phase
    # # FIX this
    est_phase = x[np.argmax(y)][0]
    # print(est_phase)
    # estimate amplitude
    est_amp = (np.max(y)-np.min(y))/2
    # print(est_amp)

    p0=np.array([est_baseline, est_amp, est_damp, est_phase, est_period, est_trend], dtype=float)

    fit = scipy.optimize.least_squares(obj_func_fit0, p0, args=(x,y))

    return fit.x

# fit1
# linear fit -> remove linear fit -> fit y-(e^(-lambda*t)*A*cos(2*pi*(x-phase)/period)+trend*x+baseline) -> 0
def obj_func_lin(params, x,y):
    baseline = params[0]
    trend = params[1]
    return (y-(x*trend+baseline)).T[0,:]

# fit linear
def fit_lin(x,y):

    # fit linear first using initial condition: median trend
    midIdx = int(x.shape[0]/2)

    first_half_medians_y = np.median(y[:midIdx,:])
    second_half_medians_x = np.median(x[midIdx:,:])
    second_half_medians_y = np.median(y[midIdx:,:])
    first_half_medians_x = np.median(x[:midIdx,:])
    # print(first_half_medians_x, first_half_medians_y, second_half_medians_x, second_half_medians_y)
    est_trend = (second_half_medians_y-first_half_medians_y)/(second_half_medians_x-first_half_medians_x)
    # print(est_trend)
    # estimate baseline
    est_baseline = np.median(y)

    p0 = [est_baseline, est_trend]
    # print(p0)

    fit = scipy.optimize.least_squares(obj_func_lin, p0, args=(x,y))
    # print(fit.x)

    return fit.x


def obj_func_fit1(params, x,y):
    amplitude = params[0]
    damp = params[1]
    phase = params[2]
    period = params[3]
    return ((y - (amplitude*(np.exp(- damp*x))*np.cos(2*np.pi*(x-phase)/period))).T[0,:])

# fit1
def fit1(x,y):
    fit_linear = fit_lin(x,y)
    # plt.plot(x,y)

    y = y - (x*fit_linear[1]+fit_linear[0])

    est_period = 24.0
    est_damp = 0.005
    # plt.plot(x,y)

    # estimate phase
    est_phase = x[np.argmax(y)][0]
    # print(est_phase)
    # estimate amplitude
    est_amp = (np.max(y)-np.min(y))/2
    # print(est_amp)

    p0 = [est_amp, est_damp, est_phase, est_period]

    fit = scipy.optimize.least_squares(obj_func_fit1, p0, args=(x,y))
    # plt.plot(x,obj_func_Hirota(x, 0, fit.x[0], fit.x[1], fit.x[2], fit.x[3], 0))

    return [fit_linear[0], fit.x[0], fit.x[1], fit.x[2], fit.x[3], fit_linear[1]]


# fit 2
# fit e^(lambda*t)*y-(A*cos(2*pi*(x-phase)/period)+trend*x+baseline) -> 0
def obj_func_fit2(params, x, y):
    baseline = params[0]
    amplitude = params[1]
    damp = params[2]
    phase = params[3]
    period = params[4]
    trend = params[5]

    sine = amplitude*np.cos(2*np.pi*(x-phase)/period)
    return (np.exp(damp*x)*y-(sine+trend*x+baseline)).T[0,:]


# fit 2
def fit2(x, y):
    # print(x.shape)
    # print(y.shape)
    midIdx = int(x.shape[0]/2)
    est_period = 24.0
    est_damp = 0.005
    # estimate trend (slope of the medians of the first half and that of the second half)
    first_half_medians_y = np.median(y[:midIdx,:])
    second_half_medians_x = np.median(x[midIdx:,:])
    second_half_medians_y = np.median(y[midIdx:,:])
    first_half_medians_x = np.median(x[:midIdx,:])
    # print(first_half_medians_x, first_half_medians_y, second_half_medians_x, second_half_medians_y)
    est_trend = (second_half_medians_y-first_half_medians_y)/(second_half_medians_x-first_half_medians_x)
    # print(est_trend)
    # estimate baseline
    est_baseline = np.median(y)
    # print(est_baseline)
    # # estimate phase
    # # FIX this
    est_phase = x[np.argmax(y)][0]
    # print(est_phase)
    # estimate amplitude
    est_amp = (np.max(y)-np.min(y))/2
    # print(est_amp)
    # print((np.exp(est_damp*x)))

    p0=np.array([est_baseline, est_amp, est_damp, est_phase, est_period, est_trend], dtype=float)

    fit = scipy.optimize.least_squares(obj_func_fit2, p0, args=(x,y),bounds=([-np.inf, -np.inf, 0, -np.inf, -np.inf, -np.inf], [np.inf, np.inf, 0.05, np.inf, np.inf, np.inf]))

    return fit.x


# skip fit 3


# fit 4
# fit e^(lambda*t)*(y-trend*x-baseline)-A*cos(2*pi*(x-phase)/period) -> 0
def obj_func_fit4(params, x, y):
    baseline = params[0]
    amplitude = params[1]
    damp = params[2]
    phase = params[3]
    period = params[4]
    trend = params[5]

    sine = amplitude*np.cos(2*np.pi*(x-phase)/period)
    return (np.exp(damp*x)*(y-trend*x-baseline)-sine).T[0,:]


# fit 2
def fit4(x, y):
    # print(x.shape)
    # print(y.shape)
    midIdx = int(x.shape[0]/2)
    est_period = 24.0
    est_damp = 0.005
    # estimate trend (slope of the medians of the first half and that of the second half)
    first_half_medians_y = np.median(y[:midIdx,:])
    second_half_medians_x = np.median(x[midIdx:,:])
    second_half_medians_y = np.median(y[midIdx:,:])
    first_half_medians_x = np.median(x[:midIdx,:])
    # print(first_half_medians_x, first_half_medians_y, second_half_medians_x, second_half_medians_y)
    est_trend = (second_half_medians_y-first_half_medians_y)/(second_half_medians_x-first_half_medians_x)
    # print(est_trend)
    # estimate baseline
    est_baseline = np.median(y)
    # print(est_baseline)
    # # estimate phase
    # # FIX this
    est_phase = x[np.argmax(y)][0]
    # print(est_phase)
    # estimate amplitude
    est_amp = (np.max(y)-np.min(y))/2
    # print(est_amp)
    # print((np.exp(est_damp*x)))

    p0=np.array([est_baseline, est_amp, est_damp, est_phase, est_period, est_trend], dtype=float)

    fit = scipy.optimize.least_squares(obj_func_fit4, p0, args=(x,y),bounds=([-np.inf, -np.inf, 0, -np.inf, -np.inf, -np.inf], [np.inf, np.inf, 0.05, np.inf, np.inf, np.inf]))
    # print(fit)

    return fit.x

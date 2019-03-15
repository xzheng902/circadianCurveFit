# data_generator.py
# Mike Zheng
# 3/1/19

# generate circadian data with different noise level and phase

import sys
import numpy as np
import matplotlib.pyplot as plt

def obj_func_Hirota(x, baseline, amplitude, damp, phase, period, trend):
    return baseline + amplitude*(np.exp(- damp*x))*np.cos(2*np.pi*(x-phase)/period) + trend*x

# Hirota obj func with normal y noise
def obj_func_Hirota_ynoise(x, baseline, amplitude, damp, phase, period, trend, noise):
    y_noise = noise * np.random.normal(size=x.size)
    return y_noise + baseline + amplitude*(np.exp(- damp*x))*np.cos(2*np.pi*(x-phase)/period) + trend*x

# Hirota obj func with normal period noise
def obj_func_Hirota_periodnormalnoise(x, baseline, amplitude, damp, phase, period, trend, noise):
    period_noise = noise * np.random.normal(size=x.size)
    return baseline + amplitude*(np.exp(- damp*x))*np.cos(2*np.pi*(x-phase)/(period+period_noise)) + trend*x

# Hirota obj func with increasing period noise+period normal noise
def obj_func_Hirota_periodincnoise(x, baseline, amplitude, damp, phase, period, trend, inc, noise):
    period_normal_noise = noise * np.random.normal(size=x.size)
    period_inc_noise = np.linspace(0-inc/2, inc/2, x.size)
    # print(period_inc_noise+period_normal_noise)
    return baseline + amplitude*(np.exp(- damp*x))*np.cos(2*np.pi*(x-phase)/(period+period_inc_noise+period_normal_noise)) + trend*x

# Hirota obj func with increasing period noise
def obj_func_Hirota_allnoise(x, baseline, amplitude, damp, phase, period, trend, inc, pnoise, ynoise):
    y_noise = ynoise * np.random.normal(size=x.size)
    period_normal_noise = pnoise * np.random.normal(size=x.size)
    period_inc_noise = np.linspace(0-inc/2, inc/2, x.size)
    return y_noise + baseline + amplitude*(np.exp(- damp*x))*np.cos(2*np.pi*(x-phase)/(period+period_inc_noise+period_normal_noise)) + trend*x

# Hirota obj func with increasing damping noise + normal damping noise
def obj_func_Hirota_dampingnoise(x, baseline, amplitude, damp, phase, period, trend, dinc, dnoise):
    damping_normal_noise = dnoise * np.random.normal(size=x.size)
    damping_inc_noise = np.linspace(0-dinc/2, dinc/2, x.size)
    return baseline + amplitude*(np.exp(- (damping_normal_noise+damping_inc_noise+damp)*x))*np.cos(2*np.pi*(x-phase)/period) + trend*x


# default case
def case0(x, params):
    y = obj_func_Hirota(x, params[0], params[1], params[2], params[3], params[4], params[5])
    return y

# y noise
def case1(x, params, noise):
    y = obj_func_Hirota_ynoise(x, params[0], params[1], params[2], params[3], params[4], params[5], noise)
    return y

def case2(x, params, noise):
    y = obj_func_Hirota_periodnormalnoise(x, params[0], params[1], params[2], params[3], params[4], params[5], noise)
    return y

def case3(x, params, inc, noise):
    y = obj_func_Hirota_periodincnoise(x, params[0], params[1], params[2], params[3], params[4], params[5], inc, noise)
    return y

def case4(x, params, inc, pnoise, ynoise):
    y = obj_func_Hirota_allnoise(x, params[0], params[1], params[2], params[3], params[4], params[5], inc, pnoise, ynoise)
    return y

def case5(x, params, dinc, dnoise):
    y = obj_func_Hirota_dampingnoise(x, params[0], params[1], params[2], params[3], params[4], params[5], dinc, dnoise)
    return y

def main(argv):

    # params based on Bmal1 untreated test idx 5
    baseline = 3.5e+03
    amplitude = 2.0e+03
    damp = 1.9e-02
    phase = 2.0e+01
    period = 2.27e+01
    trend = -1.6e+01

    params = [baseline, amplitude, damp, phase, period, trend]

    # # params based on Bmal untreated test idx 6
    # baseline = 4.6e+03
    # amplitude = 1.7e+03
    # damp = 1.9e-02
    # phase = 2.0e+01
    # period = 2.30e+01
    # trend = -3.7e+01
    #
    # params = [baseline, amplitude, damp, phase, period, trend]

    xdays = np.linspace(0, 7, 1009)
    xhours = np.linspace(0, 168, 1009)

    # baseline
    y = case0(xhours, params)
    datamat = np.matrix(xdays).T
    datamat = np.hstack((datamat, np.matrix(y).T))

    # y noise
    y = case1(xhours, params, 10)
    datamat = np.hstack((datamat, np.matrix(xdays).T, np.matrix(y).T))

    y = case1(xhours, params, 50)
    datamat = np.hstack((datamat, np.matrix(xdays).T, np.matrix(y).T))

    y = case1(xhours, params, 100)
    datamat = np.hstack((datamat, np.matrix(xdays).T, np.matrix(y).T))

    # period normal noise
    y = case2(xhours, params, 0.1)
    datamat = np.hstack((datamat, np.matrix(xdays).T, np.matrix(y).T))

    y = case2(xhours, params, 0.3)
    datamat = np.hstack((datamat, np.matrix(xdays).T, np.matrix(y).T))

    y = case2(xhours, params, 0.6)
    datamat = np.hstack((datamat, np.matrix(xdays).T, np.matrix(y).T))

    y = case2(xhours, params, 1)
    datamat = np.hstack((datamat, np.matrix(xdays).T, np.matrix(y).T))

    # period increase normal noise
    y = case3(xhours, params, 0.1, 0.1)
    datamat = np.hstack((datamat, np.matrix(xdays).T, np.matrix(y).T))

    y = case3(xhours, params, 1, 0.1)
    datamat = np.hstack((datamat, np.matrix(xdays).T, np.matrix(y).T))

    y = case3(xhours, params, 2, 0.1)
    datamat = np.hstack((datamat, np.matrix(xdays).T, np.matrix(y).T))

    y = case3(xhours, params, 4, 0.1)
    datamat = np.hstack((datamat, np.matrix(xdays).T, np.matrix(y).T))

    # all
    y = case4(xhours, params, 0.5, 0.1, 10)
    datamat = np.hstack((datamat, np.matrix(xdays).T, np.matrix(y).T))

    y = case4(xhours, params, 1, 0.3, 30)
    datamat = np.hstack((datamat, np.matrix(xdays).T, np.matrix(y).T))

    y = case4(xhours, params, 1.5, 0.3, 30)
    datamat = np.hstack((datamat, np.matrix(xdays).T, np.matrix(y).T))

    y = case4(xhours, params, 2, 0.5, 50)
    datamat = np.hstack((datamat, np.matrix(xdays).T, np.matrix(y).T))

    # damping noise
    y = case5(xhours, params, 0.01, 0.001)
    datamat = np.hstack((datamat, np.matrix(xdays).T, np.matrix(y).T))

    y = case5(xhours, params, 0.1, 0.001)
    datamat = np.hstack((datamat, np.matrix(xdays).T, np.matrix(y).T))

    y = case5(xhours, params, 0.2, 0.001)
    datamat = np.hstack((datamat, np.matrix(xdays).T, np.matrix(y).T))

    y = case5(xhours, params, 0.4, 0.001)
    datamat = np.hstack((datamat, np.matrix(xdays).T, np.matrix(y).T))


    # write the data to a file
    numExp = (int)(datamat.shape[1]/2)
    fp = open('../testdata/test-test-test-test.csv', 'w');
    s = "1/1/11, "
    for i in range(numExp-1):
        s+= ",1/1/11, "
    s+= "\nTime (days),counts/sec"
    for i in range(numExp-1):
        s+= ",Time (days),counts/sec"
    s+= "\n"

    for r in range(datamat.shape[0]):
        s += str(datamat[r,0])
        for c in range(1,datamat.shape[1]):
            s += "," + str(datamat[r,c])
        s += "\n"
    fp.write(s)
    fp.close()

if __name__ == "__main__":
    main(sys.argv);

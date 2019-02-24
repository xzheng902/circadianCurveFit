# accuracy.py
# Mike Zheng
# 2/23/19

# library of accuracy measures

import numpy as np

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

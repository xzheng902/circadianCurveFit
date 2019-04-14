# residual_analysis.py
# Mike Zheng
# 4/14/19

import sys
import numpy as np
import matplotlib.pyplot as plt

def residual_fft(res):

    fig = plt.figure()
    ax = fig.add_subplot(111)

    # sample spacing
    T = 1.0/6

    sp = np.fft.fft(res)
    freq = np.fft.fftfreq(res.shape[0], T)
    ax.plot(freq, np.abs(sp))
    plt.show()

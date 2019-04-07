# data.py
# Mike Zheng
# 2/12/19

# read indirubin circadian data

import sys
import csv
import numpy as np
import matplotlib.pyplot as plt

# Data class that holds data of one experiment
class Data:

    def __init__(self, filename, index, date, treatment, conc, reporter):
        self.filename = filename
        self.index = index
        self.date = date
        self.data = None
        self.treatment = treatment
        self.conc = conc
        self.reporter = reporter
        self.freq = 0 # number of pts per hour

    # load data matrix
    def loaddata(self, npdata):
        # extract non-empty rows
        for i in range(npdata.shape[0]):
            if npdata[i,0].strip()=="":
                i -= 1
                break
        i += 1
        self.data = npdata[:i, :].astype(np.float64)
        self.data[:,0] *= 24
        self.freq = int(round(self.data.shape[0]/(self.data[-1,0]-self.data[0,0])))

    # get data of a given period
    # default 24-96
    def getdata(self, start=24, end=96):
        for i in range(self.data.shape[0]):
            if self.data[i,0]<start and self.data[i+1,0]>=start:
                start_row = i+1
            elif self.data[i,0]<=end and self.data[i+1,0]>end:
                end_row = i+1
        return self.data[start_row:end_row,:].copy()

    # use a window to detrend the data
    # use convolution
    def windowBaselinedData(self, start=36, end=96, window_half=12):
        d = self.getdata(start-window_half,end+window_half)
        trend = self.calcTrend(d, window_half)
        output = self.getdata(start, end)
        output[:,1] -= np.matrix(trend).T
        return output

    def calcTrend(self, d, window_half=12):
        numpts = int(np.round(window_half*2*self.freq))+1
        kernel = np.ones((1,numpts), dtype=np.float64)/numpts
        trend = np.convolve(np.array(d[:,1].T)[0], np.array(kernel)[0], 'valid')
        return trend

    # remove outlier
    # find dy, if two consecutive dy are both large, then replace it with
    # average of first and third point
    def removeOutliers(self, d):
        # find diff
        arr1 = np.zeros((1,d.shape[0]+1))
        arr1[0,:-1]=d[:,1].copy().T
        arr2 = np.zeros((1,d.shape[0]+1))
        arr2[0,1:]=d[:,1].copy().T
        diff = (arr1-arr2)[0,1:-1]

        # test if points deviate too much more than 5 times stdev
        diff_stdev = np.std(diff)
        state = 0
        for i in range(diff.shape[0]):
            if diff[i]>5*diff_stdev:
                if state == 2:
                    # print("fix idx: ",i)
                    d[i,1] = (d[i-1,1]+d[i+1,1])/2
                    state = 0
                else:
                    state = 1
            elif diff[i]<-5*diff_stdev:
                if state == 1:
                    # print("fix idx: ",i)
                    d[i,1] = (d[i-1,1]+d[i+1,1])/2
                    state = 0
                else:
                    state = 2
            else:
                state =0
        #
        # plt.plot(np.linspace(0,100,diff.shape[0]), diff)
        # plt.show()

        return d

    # remove outlier, smooth, and detrend
    def processData(self, start=36, end=96, window_half=12):
        # remove outlier
        d = self.getdata(start-window_half-1/6,end+window_half+1/6)
        processed = self.removeOutliers(d)

        # smooth
        smoothed = self.calcTrend(processed, 1/6)
        processed = processed[1:-1,:]
        processed[:,1] = np.matrix(smoothed).T

        # get data and detrend
        trend = self.calcTrend(processed)
        for i in range(processed.shape[0]):
            if processed[i,0]<start and processed[i+1,0]>=start:
                start_row = i+1
            elif processed[i,0]<=end and processed[i+1,0]>end:
                end_row = i+1
        processed = processed[start_row:end_row,:].copy()
        processed[:,1] -= np.matrix(trend).T

        return processed



    def __str__(self):
        s = "File: "+self.filename+"\nExperiment: "+str(self.index)+"\nDate: "+self.date
        if self.data is None:
            s += "\nData is empty"
        else:
            s += "\nThere are "+str(self.data.shape[0])+" data points."
        return s


# read a file and returns a list of Data objects
def read(filename):
    print("reading "+filename)
    filenameParsed = filename.split('-')
    fp = open(filename, 'rU')
    dataList = list(csv.reader( fp ))
    npdatafull = np.matrix(dataList[3:])
    # initialize output experiment list (a list of Data objects)
    expList = []
    # handle first line
    i = 0
    for col in dataList[0]:
        if col.strip()!="":
            expList.append(Data(filename, i, col, filenameParsed[3][:-4], filenameParsed[2], filenameParsed[1]))
            i += 1
    # load data to Data objects
    for i in range(len(expList)):
        expList[i].loaddata(npdatafull[:,2*i:2*i+2])
    fp.close()
    return expList


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print( 'Usage: python3 %s <csv filename>' % (sys.argv[0]))
        exit(0)

    expList = read(sys.argv[1])
    print(expList[0])
    # print(expList[0].getdata())
    plt.plot(expList[0].getdata()[:,0], expList[0].getdata()[:,1])
    plt.show()

    # detrended = expList[0].windowBaselinedData()
    # print(detrended)
    # plt.plot(detrended[:,0], detrended[:,1])
    # plt.show()

    processed = expList[0].processData()
    # print(processed)
    plt.plot(processed[:,0], processed[:,1])
    plt.show()

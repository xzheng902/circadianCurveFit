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

    def __init__(self, filename, index, date):
        self.filename = filename
        self.index = index
        self.date = date
        self.data = None

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

    # get data of a given period
    # default 24-96
    def getdata(self, start=24, end=96):
        for i in range(self.data.shape[0]):
            if self.data[i,0]<start and self.data[i+1,0]>=start:
                start_row = i+1
            elif self.data[i,0]<=end and self.data[i+1,0]>end:
                end_row = i+1
        return self.data[start_row:end_row,:]

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
    fp = open(filename, 'rU')
    dataList = list(csv.reader( fp ))
    npdatafull = np.matrix(dataList[3:])
    # initialize output experiment list (a list of Data objects)
    expList = []
    # handle first line
    i = 0
    for col in dataList[0]:
        if col.strip()!="":
            expList.append(Data(filename, i, col))
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
    # plt.plot(expList[0].getdata()[:,0], expList[0].getdata()[:,1])
    # plt.show()

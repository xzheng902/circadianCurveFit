# jitter_plot.py
# Mike Zheng
# 3/14/19

import sys
import numpy as np
import matplotlib.pyplot as plt

# class to hold particular treatment, reporter pair and data
class Experiment:

    def __init__(self, treatment, reporter):
        self.treatment = treatment
        self.reporter = reporter
        self.data = []
        self.npdata = None
        self.legend = {}
        # the legend is hard coded to make sure the order is correct
        # Indirubin Bmal1
        self.legend1 = {'nontreated': 1, 'DMSO': 2, 'p8uM':3, '2uM': 4, '7uM': 5, '10uM':6}
        # Indirubin Per2
        self.legend2 = {'nontreated': 1, 'p8uM':2, '2uM': 3, '7uM': 4, '10uM':5}

    # reformat self.data for plotting
    def reformatData(self):
        if self.reporter == 'Bmal1':
            tmp = []
            catsIdx = 1
            for pt in self.data:
                conc = pt[0]
                if conc not in self.legend1:
                    self.legend1[conc] = catsIdx
                    catsIdx += 1
                tmp.append([float(self.legend1[conc]),pt[1]])
        elif self.reporter == 'Per2':
            tmp = []
            catsIdx = 1
            for pt in self.data:
                conc = pt[0]
                if conc not in self.legend2:
                    self.legend2[conc] = catsIdx
                    catsIdx += 1
                tmp.append([float(self.legend2[conc]),pt[1]])

        self.npdata = np.matrix(tmp)

    def plot(self):
        if self.npdata is None:
            print("npdata does not exist")
            return
        data_jittered = self.npdata.copy()
        noise = np.matrix(np.random.uniform(-0.1,0.1,data_jittered.shape[0])).T
        data_jittered[:,0] += noise
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.scatter(np.array(data_jittered[:,0].T)[0], np.array(data_jittered[:,1].T)[0], marker='.')
        if self.reporter == 'Bmal1':
            ax.set_xticks([1,2,3,4,5,6])
            ax.set_xticklabels(['nontreated','DMSO', 'p8uM', '2uM', '7uM', '10uM'])
            ax.set_title("Indirubin Bmal1")
        elif self.reporter == 'Per2':
            ax.set_xticks([1,2,3,4,5])
            ax.set_xticklabels(['nontreated', 'p8uM', '2uM', '7uM', '10uM'])
            ax.set_title("Indirubin Per2")


        plt.show()


def main(argv):
    if len(argv)<2:
        print( 'Usage: python3 %s <csv filename>' % (argv[0]))
        exit(0)

    # read file and parse exp col and period col
    exps = []

    fp = open(argv[1], 'rU')
    buf = fp.readline()
    buf = fp.readline().strip()
    while buf!='':
        words = buf.split(',')
        expinfo = words[0].split('-')
        # check if in exp list
        exist = False
        period = float(words[1])
        treatment = expinfo[3].split('_')[0]
        reporter = expinfo[1]
        for exp in exps:
            if treatment == exp.treatment and reporter == exp.reporter:
                exp.data.append([expinfo[2], period])
                exist = True
        # create new exp if necessary
        if not exist:
            newexp = Experiment(treatment, reporter)
            newexp.data.append([expinfo[2], period])
            exps.append(newexp)

        buf = fp.readline().strip()
    fp.close()

    for exp in exps:
        print("Experiment: "+exp.treatment+" "+exp.reporter)
        print("Number of data points: "+str(len(exp.data)))
        exp.reformatData()
        exp.plot()



if __name__ == "__main__":
    main(sys.argv)

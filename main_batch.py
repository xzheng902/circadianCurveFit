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

def main(argv):
    if len(argv) < 2:
        print( 'Usage: python3 %s <directory name>' % (argv[0]))
        exit(0)



if __name__ == "__main__":
    main(sys.argv)

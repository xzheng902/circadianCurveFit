# readdir.py
# Mike Zheng
# 2/19/19

# python3 readdir.py /Users/xiaoyuezheng/Desktop/CS_IS/indirubindatabmal1reporters

import sys
import os

# return a list of file paths of a given directory
def readdir(dir):
    filelist = []
    for root, directories, filenames in os.walk(dir):
        # for directory in directories:
        #     print(os.path.join(root, directory))
        for filename in filenames:
            if filename[0] != '.':
                filelist.append(os.path.join(root,filename))
    return filelist


def main(argv):
    if len(argv) < 2:
        print( 'Usage: python3 %s <directory path>' % (argv[0]))
        exit(0)

    print(readdir(argv[1]))

if __name__ == "__main__":
    main(sys.argv)

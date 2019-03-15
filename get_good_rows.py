# get_good_rows.py
# Mike Zheng
# 3/14/19

# keep the row as long as it has "good" in it

import sys

def main(argv):
    if len(argv)<2:
        print( 'Usage: python3 %s <csv filename>' % (argv[0]))
        exit(0)

    lines = []
    # read file
    fp = open(argv[1], 'rU')
    buf = fp.readline().strip()
    lines.append(buf)
    while buf!='':
        words = buf.split(',')
        if "good" in words:
            lines.append(buf)
        buf = fp.readline().strip()
    fp.close()

    # write file
    fp = open('goodresults.csv', 'w')

    for line in lines:
        fp.write(line+"\n")

    fp.close()


if __name__=="__main__":
    main(sys.argv)

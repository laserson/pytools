import sys

import seqtools

if len(sys.argv) == 3:
    inhandle = open(sys.argv[1],'r')
    outhandle = open(sys.argv[2],'w')
elif len(sys.argv) == 2:
    inhandle = open(sys.argv[1],'r')
    outhandle = sys.stdout
elif len(sys.argv) == 1:
    inhandle = sys.stdin
    outhandle = sys.stdout

for line in inhandle:
    if line.strip() == '':
        print >>outhandle, ''
        continue
    descr = line.split()[0]
    seq = line.split()[1]
    print >>outhandle, ">%s\n%s" % (descr,seq)

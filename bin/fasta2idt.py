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

for (descr,seq) in seqtools.FastaIterator(inhandle):
    print >>outhandle, "%-30s%s" % (descr,seq)

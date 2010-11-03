import os
import sys
import optparse

import numpy as np
import matplotlib.pyplot as plt

import seqtools

option_parser = optparse.OptionParser()
option_parser.add_option('-o','--out',dest='outname')
(options,args) = option_parser.parse_args()

if len(args) == 1:
    inhandle = open(args[0],'r')
elif len(args) == 0:
    inhandle = sys.stdin

read_lengths = []
for (name,read) in seqtools.FastaIterator(inhandle):
    read_lengths.append(len(read))

print "Number of reads: %i" % len(read_lengths)
print "Shortest read length: %i bp" % min(read_lengths)
print "Longest read length: %i bp" % max(read_lengths)
print "Median read length: %i bp" % np.median(read_lengths)
print "Mean read length: %i bp" % np.mean(read_lengths)

if options.outname == None:
    outname = os.path.splitext(os.path.basename(args[0]))[0]+'.readlenhist'
else:
    outname = options.outname

fig = plt.figure()
ax = fig.add_subplot(111)
ax.hist(read_lengths,bins=range(max(read_lengths)+1),linewidth=0,log=False)
ax.set_xlabel('Read length')
fig.savefig(outname+'.pdf')
fig.savefig(outname+'.png')

outname = outname+'.log'
figlog = plt.figure()
ax = figlog.add_subplot(111)
ax.hist(read_lengths,bins=range(max(read_lengths)+1),linewidth=0,log=True)
ax.set_xlabel('Read length')
figlog.savefig(outname+'.pdf')
figlog.savefig(outname+'.png')

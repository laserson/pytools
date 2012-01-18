#! /usr/bin/env python

import os
import sys
import argparse

import numpy as np
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt

import seqtools

argparser = argparse.ArgumentParser(description=None)
argparser.add_argument('positional',nargs='+')
argparser.add_argument('--log',action='store_true')
args = argparser.parse_args()

if len(args) == 2:
    inhandle = open(args.positional[0],'r')
    outfile = args.positional[1]
elif len(args) == 1:
    inhandle = open(args.positional[0],'r')
    outfile = 'lenhist.png'
elif len(args) == 0:
    inhandle = sys.stdin
    outfile = 'lenhist.png'

read_lengths = []
for (name,read) in seqtools.FastaIterator(inhandle):
    read_lengths.append(len(read))

print "Number of reads: %i" % len(read_lengths)
print "Shortest read length: %i bp" % min(read_lengths)
print "Longest read length: %i bp" % max(read_lengths)
print "Median read length: %i bp" % np.median(read_lengths)
print "Mean read length: %i bp" % np.mean(read_lengths)

if not args.log:
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.hist(read_lengths,bins=range(max(read_lengths)+1),linewidth=0,log=False)
    ax.set_xlabel('Read length')
    fig.savefig(outfile)
else:
    figlog = plt.figure()
    ax = figlog.add_subplot(111)
    ax.hist(read_lengths,bins=range(max(read_lengths)+1),linewidth=0,log=True)
    ax.set_xlabel('Read length')
    fig.savefig(outfile)

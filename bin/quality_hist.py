import sys

from Bio import SeqIO

import numpy as np
import scipy as sp
import scipy.stats

import matplotib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt

input_file = sys.argv[1]
output_file = sys.argv[2]

qualities = []
for record in SeqIO.parse(input_file,'fastq'):
    qualities.append(record.letter_annotations['phred_quality'])

qualities = np.array(qualities)

positions = qualities.shape[1]

p5  = sp.stats.scoreatpercentile(qualities,5)
p25 = sp.stats.scoreatpercentile(qualities,25)
p50 = sp.stats.scoreatpercentile(qualities,50)
p75 = sp.stats.scoreatpercentile(qualities,75)
p95 = sp.stats.scoreatpercentile(qualities,95)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(positions,p5, s=3,c='k',linewidths=0)
ax.scatter(positions,p95,s=3,c='k',linewidths=0)
for (pos,low,high) in zip(positions,p25,p75):
    ax.axvline(pos,low,high,color='k',lw=1)
ax.scatter(positions,p50,s=5,c='k',linewidths=0)
ax.set_xlabel('position')
ax.set_ylabel('phred score')
fig.savefig(output_file)
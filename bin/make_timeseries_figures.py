#! /usr/bin/env python

import optparse

import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections

import vdj
import vdj.analysis

option_parser = optparse.OptionParser()
option_parser.add_option('-r','--threshold',type='float')
option_parser.add_option('-o','--outputbasename')
option_parser.add_option('-n','--normalize',action='store_true')
(options,args) = option_parser.parse_args()

if len(args) == 1:
    inhandle = open(args[0],'r')
else:
    raise ValueError, "Must give a single argument to vdjxml file"

# read in times
for line in inhandle:
    if line.startswith('#times'):
        times = np.asarray(map(float,line.split()[1:]))
        break

# read in data
labels = []
timeseriesmatrix = []
for line in inhandle:
    data = line.split()
    labels.append(data[0].strip())
    timeseriesmatrix.append(map(int,data[1:]))
timeseriesmatrix = np.asarray(timeseriesmatrix)

# normalize if desired
if options.normalize:
    timeseriesmatrix = np.float_(timeseriesmatrix) / timeseriesmatrix.sum(axis=0)

# define which idxs to plot
if options.threshold:
    idxs = np.sum(timeseriesmatrix>=options.threshold,axis=1)>0 # breaks threshold at least once
else:
    idxs = [True]*timeseriesmatrix.shape[0]
# idxs = np.sum(time_series_freqs>0,axis=1)>2 # seen at least twice
# idxs_bool = np.logical_and(idxs_bool_1,idxs_bool_2)
# idxs_bool = np.array([False]*len(reference_clones))
print "Number of lines plotted: %i" % np.sum(idxs)

# ==================
# = Make the plots =
# ==================

# get output names
if options.outputbasename:
    outputbasename = options.outputbasename
else:
    outputbasename = '.'.join(args[0].split('.')[:-1])

random_color = lambda: '#%02x%02x%02x' % tuple(np.random.randint(0,256,3))

segments = [zip(times,timeseries) for timeseries in timeseriesmatrix[idxs]]
colors = [random_color() for i in xrange(len(segments))]
lines = mpl.collections.LineCollection(segments,colors=colors,linewidths=0.5)
lines.set_alpha(0.75)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.add_collection(lines)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_position(('outward',5))
ax.spines['left'].set_position(('outward',5))
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(times))
ax.set_xlim([times.min(),times.max()])
ax.autoscale_view(scalex=False,scaley=True)
# ax.set_yscale('log')
ax.set_xlabel('time')
ax.set_ylabel(options.quantify+' frequency')
# fig.show()
fig.savefig(outbasename+'.%stimeseries.png' % options.quantify)
fig.savefig(outbasename+'.%stimeseries.pdf' % options.quantify)

# # only stuff that's positive everywhere
segments = [np.asarray(zip(times,freqs)) for freqs in freqmatrix[idxs]]
segments = [segment[segment[:,1]>0] for segment in segments if segment[:,1].sum()>0]
lines = mpl.collections.LineCollection(segments,colors=colors,linewidths=0.5)
lines.set_alpha(0.75)

figlog = plt.figure()
ax = figlog.add_subplot(111)
ax.add_collection(lines)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_position(('outward',5))
ax.spines['left'].set_position(('outward',5))
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(times))
ax.set_yscale('log')
ax.set_xlim([times.min(),times.max()])
ax.set_xlabel('time')
ax.set_ylabel(options.quantify+' frequency')
# fig.show()
figlog.savefig(outbasename+'.%stimeseries.log.png' % options.quantify)
figlog.savefig(outbasename+'.%stimeseries.log.pdf' % options.quantify)

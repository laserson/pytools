#! /usr/bin/env python

import optparse
import colorsys

import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

import scale
import timeseries
import streamgraph

option_parser = optparse.OptionParser()
option_parser.add_option('-f','--filter',type='choice',choices=['none','seen2','sum2','sum3'],default='none')
(options,args) = option_parser.parse_args()

if len(args) == 2:
    inhandle = open(args[0],'r')
else:
    raise ValueError, "need input and output names"

data = timeseries.load_timeseries(inhandle)
matrix = data['matrix']
labels = np.asarray(data['labels'])
times = data['times']
sums = data['sums']

streams = matrix / sums

# determine colors for the streamgraph
colors = []
time_idxs = np.arange(streams.shape[1])
onset_time = lambda stream: np.min(time_idxs[stream > 0])
weight = lambda stream: np.sum(stream)
Hscale = scale.linear(range(len(times))).range(0,1-1./len(times))
Lscale = scale.root(streams.sum(axis=1)).range(0.8,0.5).power(4)
for stream in streams:
    h = Hscale(onset_time(stream))
    l = Lscale(weight(stream))
    colors.append( colorsys.hls_to_rgb(h,l,1) + (1.,) )
colors = np.array(colors)

# sort streamgraphs appropriately
argsort_onset = streamgraph.argsort_onset(streams)
streams = streams[argsort_onset]
matrix = matrix[argsort_onset]
colors = colors[argsort_onset]

# argsort_inside_out = streamgraph.argsort_inside_out(streams)
# streams = streams[argsort_inside_out]
# colors = colors[argsort_inside_out]

# filter out some clones
if options.filter == 'none':
    filter_idxs = np.ones(streams.shape[0]) > 0     # all streams
elif options.filter == 'seen2':
    filter_idxs = np.sum(streams > 0, axis=1) >= 2  # seen twice
elif options.filter == 'sum2':
    filter_idxs = np.sum(matrix, axis=1) >= 2  # sum=2
elif options.filter == 'sum3':
    filter_idxs = np.sum(matrix, axis=1) >= 3  # sum=3
else:
    raise ValueError, "what filter do you want me to use?"

fig = plt.figure(figsize=(24,16))
ax = fig.add_subplot(111)
streamgraph.streamgraph(ax, streams[filter_idxs], x=times, colors=colors[filter_idxs])
streamgraph.format_streamgraph(ax)
ax.xaxis.set_ticks(times)
ax.autoscale_view()
# fig.show()
fig.savefig(args[1],dpi=120)

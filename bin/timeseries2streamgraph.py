#! /usr/bin/env python

import optparse
import colorsys

import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

import timeseries
import streamgraph

option_parser = optparse.OptionParser()
# option_parser.add_option('-x','--xxx',dest='xxxx',type='int')
(options,args) = option_parser.parse_args()

if len(args) == 2:
    inhandle = open(args[0],'r')
else:
    raise ValueError, "need input and output names"

data = timeseries.load_timeseries(inhandle)
matrix = data['matrix']
labels = data['labels']
times = data['times']
sums = data['sums']

streams = matrix / sums

# determine colors for the streamgraph
colors = []
min_norm_weight = streams.sum(axis=1).min()
max_norm_weight = streams.sum(axis=1).max()
onset_time = lambda stream: np.min(np.arange(len(stream))[stream > 0])
weight = lambda stream: np.sum(stream)
for stream in streams:
    h = float(onset_time(stream)) / (len(times)-1)
    l = (weight(stream) - min_norm_weight) / (max_norm_weight - min_norm_weight) * 0.3 + 0.5
    colors.append( colorsys.hls_to_rgb(h,l,1) + (1.,) )
colors = np.array(colors)

# sort streamgraphs appropriately
argsort_onset = streamgraph.argsort_onset(streams)
streams = streams[argsort_onset]
colors = colors[argsort_onset]

# argsort_inside_out = streamgraph.argsort_inside_out(streams)
# streams = streams[argsort_inside_out]
# colors = colors[argsort_inside_out]

# filter out some clones
stream_filter = np.sum(streams > 0, axis=1) >= 2
streams = streams[stream_filter]
colors = colors[stream_filter]

fig = plt.figure(figsize=(24,16))
ax = fig.add_subplot(111)
streamgraph.streamgraph(ax, streams, x=times, colors=colors)
ax.autoscale_view()
# fig.show()
fig.savefig(args[1])

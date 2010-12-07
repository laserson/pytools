#! /usr/bin/env python

import sys
import optparse
import json

import timeseries
from streamgraph_html import streamgraph_html

option_parser = optparse.OptionParser()
# option_parser.add_option('-x','--xxx',dest='xxxx',type='int')
(options,args) = option_parser.parse_args()

if len(args) == 2:
    inhandle = open(args[0],'r')
    outhandle = open(args[1],'w')
elif len(args) == 1:
    inhandle = open(args[0],'r')
    outhandle = sys.stdout
elif len(args) == 0:
    inhandle = sys.stdin
    outhandle = sys.stdout

data = timeseries.load_timeseries(inhandle)

# eliminate numpy-ness of objects before JSON output
np_matrix = data['matrix']
py_matrix = []

if np_matrix[0][0].dtype.kind == 'i':
    num_type = int
elif np_matrix[0][0].dtype.kind == 'f':
    num_type = float
else:
    raise TypeError, "data matrix must be int or float types"
    
for row in np_matrix:
    py_matrix.append(map(num_type,list(row)))
data['matrix'] = py_matrix
data['labels'] = list(data['labels'])

for label in data.keys():
    if label == 'labels' or label == 'matrix':
        continue
    data[label] = list(data[label])

streamgraph_output = streamgraph_html % (json.dumps(data))

outhandle.write(streamgraph_output)

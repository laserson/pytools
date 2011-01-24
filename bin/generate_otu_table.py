#! /usr/bin/env python

import optparse
import os

import vdj.analysis

option_parser = optparse.OptionParser()
option_parser.add_option('-m','--mapping_file')
(options,args) = option_parser.parse_args()

if len(args) != 2:
    raise ValueError, "need input and output filenames"

# Read sample mapping file
mapping_handle = open(options.mapping_file,'r')
samples = [(line.split('\t')[0].strip(),line.split('\t')[2].strip()) for line in mapping_handle if not line.startswith('#')]
mapping_handle.close()

# Load count data
infilename = args[0]
inhandle = open(infilename,'r')
(uniq_feature_values,countdict) = vdj.analysis.vdjxml2countdict(inhandle,['barcode','clone'])
inhandle.close()

# Convert to matrix form
countmatrix = vdj.analysis.countdict2matrix(['barcode','clone'],uniq_feature_values,countdict).transpose()

# Reorder columns to correspond to mapping file order
sample_idxs = dict([(v,i) for (i,v) in enumerate(uniq_feature_values['barcode'])])
argsort = [sample_idxs[sample] for (sample,descr) in samples]
countmatrix = countmatrix[:,argsort]

# Dump OTU table
basename = os.path.basename(args[0])
outfilename = args[1]
outhandle = open(outfilename,'w')

print >>outhandle, "#OTU counts %s" % basename
header = "OTU ID"
for (sample,descr) in samples: header += "\t%s" % ('_'.join([sample,descr]))
print >>outhandle, header

for (label,countvector) in zip(uniq_feature_values['clone'],countmatrix):
    line = label
    for count in countvector:
        line += "\t%i" % int(count)
    print >>outhandle, line

outhandle.close()

#! /usr/bin/env python

import sys
import argparse
from collections import defaultdict

from seqtools import FastaIterator

argparser = argparse.ArgumentParser(description=None)
argparser.add_argument('input',nargs='?',type=argparse.FileType('r'),default=sys.stdin)
argparser.add_argument('output',nargs='?',type=argparse.FileType('w'),default=sys.stdout)
args = argparser.parse_args()

counts = defaultdict(list)
for (name,seq) in FastaIterator(args.input):
    counts[seq].append(name)

for seq in sorted(counts.keys(), key=lambda k: len(counts[k]), reverse=True):
    for name in counts[seq]:
        args.output.write(">%s\n%s\n" % (name,seq))

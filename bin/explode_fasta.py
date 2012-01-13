#! /usr/bin/env python

import os
import sys
import argparse

import vdj
from pyutils import cleanup_id

argparser = argparse.ArgumentParser(description=None)
argparser.add_argument('input_file',nargs='?',type=argparser.FileType('r'),default=sys.stdin)
argparser.add_argument('output_dir',nargs='?',default=os.getcwd())
args = argparser.parse_args()

for chain in vdj.parse_imgt(args.input_file):
    output_file = os.path.join(args.output_dir,'%s.imgt' % cleanup_id(chain.id))
    with open(output_file,'w') as op:
        print >>op, chain

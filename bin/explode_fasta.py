#! /usr/bin/env python

import os
import sys
import argparse

from Bio import SeqIO

from pyutils import cleanup_id

argparser = argparse.ArgumentParser(description=None)
argparser.add_argument('input_file',nargs='?',type=argparse.FileType('r'),default=sys.stdin)
argparser.add_argument('output_dir',nargs='?',default=os.getcwd())
args = argparser.parse_args()

for record in SeqIO.parse(args.input_file,'fasta'):
    output_file = os.path.join(args.output_dir,'%s.fasta' % cleanup_id(record.id))
    with open(output_file,'w') as op:
        print >>op, record.format('fasta')

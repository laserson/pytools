#! /usr/bin/env python

import sys
import argparse

from Bio import SeqIO
    
argparser = argparse.ArgumentParser(description=None)
argparser.add_argument('input_file',nargs='?',type=argparse.FileType('rb'),default=sys.stdin)
argparser.add_argument('output_file',nargs='?',type=argparse.FileType('w'),default=sys.stdout)
args = argparser.parse_args()

for record in SeqIO.parse(args.input_file,'sff'):
    start = record.annotations['clip_qual_left']
    end   = record.annotations['clip_qual_right']
    args.output_file.write( record[start:end].format('fastq') )

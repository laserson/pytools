#! /usr/bin/env python

import subprocess
import argparse

argparser = argparse.ArgumentParser(description=None)
argparser.add_argument('-q','--query',required=True)
argparser.add_argument('-t','--target',required=True)
argparser.add_argument('-o','--output',required=True)
argparser.add_argument('-u','--usearch',default='usearch')
args = argparser.parse_args()

usearch_cmd = "%s --query %s --db %s --nofastalign --maxaccepts 0 --maxrejects 0 --global --id 0 --userout %s --userfields query+target+id0+id1+id2+id3+id4+gaps+intgaps+qloz+qhiz+tloz+thiz+ql+tl+cols+intcols"

p = subprocess.Popen(usearch_cmd % (args.usearch,args.query,args.target,args.output),shell=True)
p.wait()

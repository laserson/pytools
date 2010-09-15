#! /usr/bin/env python

import sys
import optparse

parser = optparse.OptionParser()
parser.add_option('-s','--size',type='int')
parser.add_option('-o','--offset',type='int')
(options, args) = parser.parse_args()

if len(args) == 2:
    inhandle = open(args[0],'r')
    outhandle = open(args[1],'w')
elif len(args) == 1:
    inhandle = open(args[0],'r')
    outhandle = sys.stdout
elif len(args) == 0:
    inhandle = sys.stdin
    outhandle = sys.stdout


#-----------------------------------------------------------------------------

def fasta_parser(handle):
    # taken from biopython
    
    #Skip any text before the first record (e.g. blank lines, comments)
    while True:
        line = handle.readline()
        if line == "" : return #Premature end of file, or just empty?
        if line[0] == ">":
            break
    
    while True:
        if line[0]!=">":
            raise ValueError("Records in Fasta files should start with '>' character")
        descr = line[1:].rstrip()
        
        lines = []
        line = handle.readline()
        while True:
            if not line : break
            if line[0] == ">": break
            lines.append(line.rstrip().replace(" ","").replace("\r",""))
            line = handle.readline()
        
        yield (descr,"".join(lines))
 
        if not line : return #StopIteration
    assert False, "Should not reach this line"

#-----------------------------------------------------------------------------

tile_size = options.size
tile_offset = options.offset

for (descr,seq) in fasta_parser(inhandle):
    pos = 0
    num = 0
    while pos < len(seq):
        if pos+tile_size >= len(seq):    # last tile in seq
            print >>outhandle, '>%s|tile%03i\n%s' % (descr,num,seq[-tile_size:])
        else:
            print >>outhandle, '>%s|tile%03i\n%s' % (descr,num,seq[pos:pos+tile_size])
        pos += tile_offset
        num += 1

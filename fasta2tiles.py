#! /usr/bin/env python

import sys
import optparse

import blast

parser = optparse.OptionParser()
parser.add_option('-s','--size',type='int')
parser.add_option('-o','--offset',type='int')
parser.add_option('-p','--blastp',action='store_true')
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
    num = 1
    while pos < len(seq):
        if pos+tile_size >= len(seq):    # last tile in seq
            tile = seq[-tile_size:]
            start = len(seq) - tile_size
            end = len(seq)
        else:
            tile = seq[pos:pos+tile_size]
            start = pos
            end = pos+tile_size
        
        if options.blastp == True:
            num_hits = blast.number_genome_qblast_protein_hits(tile)
            print >>outhandle, '>%s|tile%03i|%i|%i|%i\n%s' % (descr,num,start,end,num_hits,tile)
        else:
            print >>outhandle, '>%s|tile%03i|%i|%i\n%s' % (descr,num,start,end,tile)
        
        pos += tile_offset
        num += 1

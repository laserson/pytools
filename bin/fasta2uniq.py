import sys

import seqtools

if len(sys.argv) == 3:
    inhandle = open(sys.argv[1],'r')
    outhandle = open(sys.argv[2],'w')
elif len(sys.argv) == 2:
    inhandle = open(sys.argv[1],'r')
    outhandle = sys.stdout
elif len(sys.argv) == 1:
    inhandle = sys.stdin
    outhandle = sys.stdout

all_seqs = []
uniq_seqs = set()

for (descr,seq) in seqtools.FastaIterator(inhandle):
    all_seqs.append((descr,seq))
    uniq_seqs.add(seq)

for (descr,seq) in all_seqs:
    if seq in uniq_seqs:
        outhandle.write('>%s\n%s\n' % (descr,seq))
        uniq_seqs.remove(seq)

    
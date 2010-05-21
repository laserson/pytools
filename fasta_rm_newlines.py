import sys

from Bio import SeqIO

if len(sys.argv) == 3:
    inhandle = open(sys.argv[1],'r')
    outhandle = open(sys.argv[2],'w')
elif len(sys.argv) == 2:
    inhandle = open(sys.argv[1],'r')
    outhandle = sys.stdout
elif len(sys.argv) == 1:
    inhandle = sys.stdin
    outhandle = sys.stdout

# SeqIO.write does not allow access to the wrap parameter
# SeqIO.write(SeqIO.parse(inhandle,'fasta'),outhandle,'fasta')

print_fasta = lambda r: outhandle.write(">%s\n%s\n" % (r.description,r.seq.tostring()))
map(print_fasta,SeqIO.parse(inhandle,'fasta'))

#! /usr/bin/env python

# take a FASTA file of DNA sequences (short oligos) with IUPAC degeneracies
# and ambiguities and expand all combinatorial possibilities into a new FASTA
# file
#
# works by implementing a recursive depth first search

import sys
from Bio           import SeqIO
from Bio.Alphabet  import IUPAC
from Bio.Data      import IUPACData
from Bio.SeqRecord import SeqRecord

true =  1
false = 0

IUPAC_vals = IUPACData.ambiguous_dna_values


#################
##     DFS     ##
#################

class node:
    def __init__(self, cum, rem):
        self.visited =    false
        self.neighbors =  []
        self.cumul_seq =  cum
        self.remain_seq = rem

# to use: must supply:
#    1. a list where the sequences will be pushed and
#    2. a node with cumul_seq empty and remain_seq = IUPAC DNA sequence


def expand_seq( curr_node, cum_list ):
    curr_node.visited = true

    # if we are not at the end of the tree yet
    if len(curr_node.remain_seq) > 0:
        # construct neighbors of current node based on remaining sequence
        for nucleotide in IUPAC_vals[ curr_node.remain_seq[0] ]:
            curr_node.neighbors.append( node(curr_node.cumul_seq + nucleotide, curr_node.remain_seq[1:]) )

        # implement recursive DFS
        for neighbor in curr_node.neighbors:
            if neighbor.visited == false:
                expand_seq( neighbor, cum_list )

    # we should only run this when there are no neighbors left
    elif len(curr_node.remain_seq) == 0:
        cum_list.append(curr_node.cumul_seq)


##################
##     MAIN     ##
##################
        
ipf = open( sys.argv[1], 'r' )
opf = open( sys.argv[2], 'w' )

for line in ipf:
    # if fasta header
    if line[0] == '>':
        cur_fasta = line.strip()
    else:
        cur_seq = line.strip()
        cur_seq = cur_seq.upper()

        # perform DFS and expand out sequences
        expanded_list = []
        start_node = node('',cur_seq)

        expand_seq( start_node, expanded_list )

        # spit out sequences in new file
        for s in expanded_list:
            opf.write(cur_fasta + '\n')
            opf.write(s + '\n')
            
ipf.close()
opf.close()



####################################
####################################
##
##   THE CODE BELOW IS FOR
##   PYTHON 2.5 AND THE LATEST
##   VERSION OF BIOPYTHON, WHICH
##   ARE NOT INSTALLED ON orchestra
##
##   I HAVE REWRITTEN THE CODE
##   ABOVE SO THAT IT DOES NOT USE
##   THE BIOPYTHON SYSTEM, AND
##   PARSES THE FILE MANUALLY
##
##   -UL, 14 April 2008
##
####################################
####################################
##
###################
####     MAIN     ##
###################
##
##ipf = open( sys.argv[1], 'r' )
##opf = open( sys.argv[2], 'w' )
##
##for seq_record in SeqIO.parse(ipf, "fasta"):
##    # make seq object kosher
##    seq_record.seq.data = seq_record.seq.data.upper()
##    seq_record.seq.alphabet = IUPAC.ambiguous_dna
##    
##    # perform DFS and expand out sequences
##    expanded_list = []
##    start_node = node('',seq_record.seq)
##
##    expand_seq( start_node, expanded_list )
##
##    # spit out sequences in new file
##    # fasta headers will have numbers appended
##    expand_fasta = [ SeqRecord(s,seq_record.id+'_deg_'+str(i)) for (i,s) in zip(range(1,length(expanded_list)+1),expanded_list) ]
##    SeqIO.write(expand_fasta, opf, "fasta")
##
##ipf.close()
##opf.close()
##
####################################
####################################

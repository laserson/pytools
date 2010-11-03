#! /usr/bin/env python

# take a FASTA file of DNA sequences (short oligos) with IUPAC degeneracies
# and ambiguities and expand all combinatorial possibilities into a new FASTA
# file
#
# works by implementing a recursive depth first search

IUPAC_vals = {'A': 'A',
              'B': 'CGT',
              'C': 'C',
              'D': 'AGT',
              'G': 'G',
              'H': 'ACT',
              'K': 'GT',
              'M': 'AC',
              'N': 'GATC',
              'R': 'AG',
              'S': 'CG',
              'T': 'T',
              'V': 'ACG',
              'W': 'AT',
              'X': 'GATC',
              'Y': 'CT'}

# ======================
# = Depth first search =
# ======================

class dfs_node:
    def __init__(self, cum, rem):
        self.visited =    False
        self.neighbors =  []
        self.cumul_seq =  cum
        self.remain_seq = rem

# to use: must supply:
#    1. a list where the sequences will be pushed and
#    2. a dfs_node with cumul_seq empty and remain_seq = IUPAC DNA sequence

def dfs_expand_seq( curr_dfs_node, cum_list ):
    curr_dfs_node.visited = True

    # if we are not at the end of the tree yet
    if len(curr_dfs_node.remain_seq) > 0:
        # construct neighbors of current dfs_node based on remaining sequence
        for nucleotide in IUPAC_vals[ curr_dfs_node.remain_seq[0] ]:
            curr_dfs_node.neighbors.append( dfs_node(curr_dfs_node.cumul_seq + nucleotide, curr_dfs_node.remain_seq[1:]) )

        # implement recursive DFS
        for neighbor in curr_dfs_node.neighbors:
            if neighbor.visited == False:
                dfs_expand_seq( neighbor, cum_list )

    # we should only run this when there are no neighbors left
    elif len(curr_dfs_node.remain_seq) == 0:
        cum_list.append(curr_dfs_node.cumul_seq)

def expand_seq(seq):
    expanded_list = []
    start_node = dfs_node('',seq)
    dfs_expand_seq( start_node, expanded_list )
    return expanded_list

# ========
# = MAIN =
# ========

if __name__ == '__main__':
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
    
    for record in SeqIO.parse(inhandle,'fasta'):
        seq = record.seq.tostring().upper()
        expanded_seqs = expand_seq( seq )
        for (i,s) in enumerate(expanded_seqs):
            outhandle.write(">%s|%i\n%s\n" % (record.description,i+1,s))     # write fasta output

import sys
import math
import copy
import glob
from Bio           import SeqIO
from Bio.Seq       import Seq
from Bio.Alphabet  import IUPAC
from Bio.Data      import IUPACData
from Bio.SeqRecord import SeqRecord
from numpy import zeros, arange
import numpy as np
#from editdist import distance as editdist
import random
import string
import operator

def getFasta(filename):
    ip = open(filename,'r')
    seqs = list(SeqIO.parse(ip,'fasta'))
    ip.close()
    
    idwarn = False
    for seq in seqs:
        seq.id = ''
        seq.name = ''
        if len(seq.description.split()) != 1:
            idwarn = True
            break
    if idwarn == True:
        print "WARNING: Sequence identifiers contain multiple fields"
    
    return seqs

def random_DNA_sequence(N):
    alpha = {0:'A',1:'C',2:'G',3:'T'}
    randints = np.random.random_integers(0,3,N)
    randDNA = ''.join([alpha[i] for i in randints])
    return randDNA

def revcomp(seq):
    """Compute reverse complement of sequence.  seq must be pure string; will return all uppercase."""
    
    complement = {      # IUPAC codes
                    'A':'T',
                    'C':'G',
                    'G':'C',
                    'T':'A',
                    'R':'Y',
                    'Y':'R',
                    'S':'S',
                    'W':'W',
                    'K':'M',
                    'M':'K',
                    'B':'V',
                    'D':'H',
                    'H':'D',
                    'V':'B',
                    'N':'N'
                 }
                
    return ''.join( [ complement[nt] for nt in seq[::-1].upper() ] )

def seqString(seqobj):
    if isinstance(seqobj,SeqRecord):
        seq = seqobj.seq.tostring().upper()
    elif isinstance(seqobj,Seq):
        seq = seqobj.tostring().upper()
    elif isinstance(seqobj,str):
        seq = seqobj.upper()
    return seq

def seqStrings(seqs):
    return [seqString(s) for s in seqs]

def stripBio(seqs):
    return seqStrings(seqs)

def randalphanum(n):
    alphanum = string.digits+string.ascii_uppercase
    return ''.join([random.choice(alphanum) for i in range(n)])

def agencourt2fasta(loc):
    
    files = glob.glob(loc+'/*')
    
    records = []
    for f in files:
        records.extend( getFasta( f ) )
    
    return records


def primerID( seq, pri ):
    '''
    seq and pri are lists of SeqRecord objects.  returns a dictionary
    with key=id of sequence and value=list of ids of primers that land
    in the sequence (or rev comps)
    '''
    
    primers = []
    for p in pri:
        primers += seqtools.degex(p)
    
    res = {}
    for s in seq:
        res[s.id] = []
        for p in primers:
            if (p.seq.tostring() in s.seq.tostring()) \
               or (p.seq.reverse_complement().tostring() in s.seq.tostring()) \
               or (p.seq.tostring() in s.seq.reverse_complement().tostring()) \
               or (p.seq.reverse_complement().tostring() in s.seq.reverse_complement().tostring()):
                if p.id not in res[s.id]: res[s.id].append(p.id)
    
    return res


#%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%% OLIGO Tm CALC
#%%%%%%%%%%%%%%%%%%%%%%%%%%%

def oligoTm(seqobj):
    """
    Takes either a SeqRecord object, a Seq object, or a string
    and computes the melting temp based on the NN model (yes?).
    This is Kun's code
    
    CHECK THE NN PARAMETERS
    """
    
    if isinstance(seqobj,SeqRecord):
        seq = seqobj.seq.tostring().upper()
    elif isinstance(seqobj,Seq):
        seq = seqobj.tostring().upper()
    elif isinstance(seqobj,str):
        seq = seqobj.upper()
    
    # set the default tm parameters
    C_primer = 200
    C_Mg = 1.5
    C_MonovalentIon = 50
    C_dNTP = 0.8
    percentage_DMSO = 0
    percentage_annealed = 50
    
    percentage_annealed = percentage_annealed/100.0
    percentage_DMSO = percentage_DMSO/100.0
    #Some constants
    R = 1.987
    deltaH = dict()
    deltaS = dict()
    
    # updated by Sri
    deltaH =  {     "AA": -7.6,  "TT": -7.6, "AT": -7.2, "TA": -7.2, "CA": -8.5, "TG": -8.5, "GT": -8.4, "AC": -8.4,"CT": -7.8, "AG": -7.8, "GA": -8.2, "TC": -8.2,"CG": -10.6,"GC": -9.8, "GG": -8.0, "CC": -8.0, "A": 2.2, "T": 2.2, "G": 0.0, "C": 0.0}
    deltaS = { "AA": -21.3, "TT": -21.3, "AT": -20.4, "TA": -21.3, "CA": -22.7, "TG": -22.7, "GT": -22.4, "AC": -22.4, "CT": -21.0, "AG": -21.0, "GA": -22.2, "TC": -22.2,"CG": -27.2, "GC": -24.4, "GG": -19.9, "CC":-19.9, "A": 6.9, "T": 6.9, "G": 0.0, "C": 0.0}
    # deltaH =  {  "AA": -7.9,  "TT": -7.9, "AT": float((-1)*7.2), "TA": -7.2, "CA": -8.5, "TG": -8.5, "GT": -8.4, "AC": -8.4,"CT": -7.8, "AG": -7.8, "GA": -8.2, "TC": -8.2,"CG": -10.6,"GC": -9.8, "GG": -8.0, "CC": -8.0, "A": 2.3, "T": 2.3, "G": 0.1, "C": 0.1}
    # deltaS = { "AA": -22.2, "TT": -22.2, "AT": -20.4, "TA": -21.3, "CA": -22.7, "TG": -22.7, "GT": -22.4, "AC": -22.4, "CT": -21.0, "AG": -21.0, "GA": -22.0, "TC": -22.0,"CG": -27.2, "GC": -24.4, "GG": -19.9, "CC":-19.9, "A": 4.1, "T": 4.1, "G": -2.8, "C": -2.8}
    
    C_SodiumEquivalent = C_MonovalentIon + 120 * math.sqrt(C_Mg-C_dNTP)
    seqLength = len(seq)
    dH = 0.2 + deltaH[str(seq[0])] + deltaH[str(seq[len(seq)-1])]
    dS = -5.7 + deltaS[seq[0]] + deltaS[seq[len(seq)-1]]
    for i in range(0, seqLength - 1):
        dH += deltaH[str(seq[i:i+2])]
        dS +=  deltaS[seq[i:i+2]]
    dS = dS + 0.368 * seqLength * math.log(C_SodiumEquivalent/1000.0)
    #val = math.log(C_primer*(1-percentage_annealed)/percentage_annealed)
    Tm =(dH * 1000) / (dS + R * (math.log(C_primer*(1-percentage_annealed)/percentage_annealed)-21.4164)) - 273.15 - 0.75*percentage_DMSO
    return Tm
    
    # C_SodiumEquivalent = C_MonovalentIon + 120 * math.sqrt(C_Mg-C_dNTP)
    # seqLength = len(seq)
    # dH = deltaH[str(seq[0])] + deltaH[str(seq[len(seq)-1])]
    # dS = deltaS[seq[0]] + deltaS[seq[len(seq)-1]]
    # for  i in range(0, seqLength - 1):
    #     dH = dH + deltaH[str(seq[i:i+2])]
    #     dS = dS +  deltaS[seq[i:i+2]]
    # dS = dS + 0.368 * seqLength * math.log(C_SodiumEquivalent/1000.0)
    # val = math.log(C_primer*(1-percentage_annealed)/percentage_annealed)
    # Tm =(dH * 1000) / (dS + R * (math.log(C_primer*(1-percentage_annealed)/percentage_annealed)-21.4164)) - 273.15 - 0.75*percentage_DMSO
    # return Tm



#%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%% Expand Degenerate Seqs
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#################
##     DFS     ##
#################

class node:
    def __init__(self, cum, rem):
        self.visited =    False
        self.neighbors =  []
        self.cumul_seq =  cum
        self.remain_seq = rem

# to use: must supply:
#    1. a list where the sequences will be pushed and
#    2. a node with cumul_seq empty and remain_seq = IUPAC DNA sequence


def expand_seq( curr_node, cum_list ):
    curr_node.visited = True
    
    # if we are not at the end of the tree yet
    if len(curr_node.remain_seq) > 0:
        # construct neighbors of current node based on remaining sequence
        for nucleotide in IUPACData.ambiguous_dna_values[ curr_node.remain_seq[0] ]:
            curr_node.neighbors.append( node(curr_node.cumul_seq + nucleotide, curr_node.remain_seq[1:]) )
        
        # implement recursive DFS
        for neighbor in curr_node.neighbors:
            if neighbor.visited == False:
                expand_seq( neighbor, cum_list )
    
    # we should only run this when there are no neighbors left
    elif len(curr_node.remain_seq) == 0:
        cum_list.append(curr_node.cumul_seq)


def degex(seqrec):
    """
    Take a SeqRecord object with potentialy IUPAC degenerate
    codes and return a list of SeqRecord objects with the
    sequences expanded out
    """
    seqrec.seq.data = seqrec.seq.data.upper()
    seqrec.seq.alphabet = IUPAC.ambiguous_dna
    
    # perform DFS and expand out sequences
    expanded_list = []
    start_node = node('',seqrec.seq.tostring())
    
    expand_seq( start_node, expanded_list )
    
    # create a list of SeqRecord objects expanded seqs
    expanded_seqrec = []
    for s in expanded_list:
        x = copy.copy(seqrec)
        x.seq = Seq( s, IUPAC.unambiguous_dna )
        expanded_seqrec.append(x)
    
    return expanded_seqrec



## TOO SLOW.  USING C VERSION INSTEAD
##
##def editdist(seq1, seq2):
##        '''
##        Compute the Levenshtein edit distance between two sequences
##        based on:
##        http://www.poromenos.org/node/87
##        '''
##        if len(seq1) > len(seq2):
##                seq1,seq2 = seq2,seq1
##        if len(seq2) == 0:
##                return len(seq1)
##
##        N1 = len(seq1) + 1
##        N2 = len(seq2) + 1
##        distmat = zeros((N1,N2))
##        distmat[:,0] = arange(N1)
##        distmat[0,:] = arange(N2)
##        
##        for i in xrange(1, N1):
##                for j in xrange(1, N2):
##                        deletion = distmat[i-1,j] + 1
##                        insertion = distmat[i,j-1] + 1
##                        substitution = distmat[i-1,j-1]
##                        if seq1[i-1] != seq2[j-1]:
##                                substitution += 1
##                        distmat[i,j] = min(insertion, deletion, substitution)
##
##        return distmat[N1-1][N2-1]
##

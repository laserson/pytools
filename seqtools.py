import string
import random

random.seed()

# ==============================
# = General sequence utilities =
# ==============================

def substitute(seq,pos,sub):
    return seq[:pos] + sub + seq[pos+1:]

complement_table = string.maketrans('ACGTRYSWKMBDHVN','TGCAYRSWMKVHDBN')

def reverse(seq):
    return seq[::-1]

def complement(seq):
    return seq.upper().translate(complement_table)

def reverse_complement(seq):
    """Compute reverse complement of sequence.
    
    Mindful of IUPAC ambiguities.
    Return all uppercase.
    """
    return reverse(complement(seq))
    # return seq.upper().translate(complement_table)[::-1]



def gc_content(seq):
    gc = seq.lower().count('g') + seq.lower().count('c')
    return float(gc) / len(seq)

def random_dna_seq(n):
    choice = random.choice
    return reduce(lambda cumul,garbage:cumul+choice('ACGT'),xrange(n),'')

# ============================
# = biopython-specific tools =
# ============================

from Bio.Seq       import Seq
from Bio.SeqRecord import SeqRecord

def make_SeqRecord(name,seq):
    return SeqRecord(Seq(seq),id=name,name=name,description=name)

def get_string(seqobj):
    if isinstance(seqobj,SeqRecord):
        seq = seqobj.seq.tostring().upper()
    elif isinstance(seqobj,Seq):
        seq = seqobj.tostring().upper()
    elif isinstance(seqobj,str):
        seq = seqobj.upper()
    return seq
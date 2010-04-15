import string

# ==============================
# = General sequence utilities =
# ==============================

def substitute(seq,pos,sub):
    return seq[:pos] + sub + seq[pos+1:]

complement = string.maketrans('ACGTRYSWKMBDHVN','TGCAYRSWMKVHDBN')

def reverse_complement(seq):
    """Compute reverse complement of sequence.
    
    Mindful of UIPAC ambiguities.
    Return all uppercase.
    """
    return seq.upper().translate(complement)[::-1]

def reverse(seq):
    return seq[::-1]

def complement(seq):
    return seq.upper().translate(complement)


# ============================
# = biopython-specific tools =
# ============================

from Bio.Seq       import Seq
from Bio.SeqRecord import SeqRecord

def get_string(seqobj):
    if isinstance(seqobj,SeqRecord):
        seq = seqobj.seq.tostring().upper()
    elif isinstance(seqobj,Seq):
        seq = seqobj.tostring().upper()
    elif isinstance(seqobj,str):
        seq = seqobj.upper()
    return seq
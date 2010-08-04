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


# for generating 'safe' filenames from identifiers
cleanup_table = string.maketrans('/*|','___')
def cleanup_id(identifier):
    return identifier.translate(cleanup_table)


# ==========================
# = Manual FASTA iteration =
# ==========================

# taken from biopython

identity = string.maketrans('','')
nonalpha = identity.translate(identity,string.ascii_letters)

def FastaIterator(handle,title2ids=lambda s: s):
    while True:
        line = handle.readline()
        if line == '' : return
        if line[0] == '>':
            break
    
    while True:
        if line[0] != '>':
            raise ValueError("Records in Fasta files should start with '>' character")
        descr = title2ids(line[1:].rstrip())
        fullline = ''
        line = handle.readline()
        while True:
            if not line : break
            if line[0] == '>': break
            fullline += line.translate(identity,nonalpha)
            line = handle.readline()
        
        yield (descr,fullline)
        
        if not line : return #StopIteration
    assert False, "Should not reach this line"


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


def get_features(feature_list,feature_type):
    target_features = []
    for feature in feature_list:
        if feature.type == feature_type:
            target_features.append(feature)
    return target_features


def advance_to_features(feature_iter,feature_types):
    # note, here feature_types is a list of possible stopping points
    for feature in feature_iter:
        if feature.type in feature_types:
            return feature
    raise ValueError, "didn't find %s in record" % feature_types


def advance_to_feature(feature_iter,feature_type):
    return advance_to_features(feature_iter,[feature_type])

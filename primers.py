import oligoTm
import unafold
import seqtools

def generate_candidates(seq,minlen=18,maxlen=30):
    candidates = []
    for start in xrange(len(seq)):
        length = minlen
        while length <= maxlen and start+length <= len(seq):
            candidates.append( seq[start:start+length] )
    return candidates

def choose_PCR_primer(seq,target_Tm=62.):
    
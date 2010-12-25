import oligoTm
import unafold
import seqtools

def generate_candidates(seq,minlen=18,maxlen=30):
    candidates = []
    for start in xrange(len(seq)):
        length = minlen
        while length <= maxlen and start+length <= len(seq):
            candidates.append( seq[start:start+length] )
            length += 1
    return candidates

def choose_PCR_primer(seq,target_Tm=62.):
    candidates = generate_candidates(seq)
    
    # filter for Tm
    candidates = filter(lambda s: abs(oligoTm.oligoTm(s) - target_Tm) <= 2, candidates)
    if len(candidates) == 0:
        raise ValueError, "No primer candidates meet Tm cutoffs"
    
    # filter for 0.4-0.6 GC content
    candidates = filter(lambda s: abs(seqtools.gc_content(s) - 0.5) <= 0.1,candidates)
    if len(candidates) == 0:
        raise ValueError, "No primer candidates meet GC content cutoffs"
    
    # rank on secondary structure minimization
    candidates.sort(key=unafold.hybrid_ss_min)
    
    return candidates[0]

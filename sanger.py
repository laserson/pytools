import os
import tempfile

import exonerate

standard_primers = {    # 5' -> 3'
    'M13R' : 'caggaaacagctatgac',
    'M13F-20' : 'gtaaaacgacggccag',
    'T3' : 'attaaccctcactaaaggga',
    'T7' : 'taatacgactcactataggg'
}

standard_vectors = {
    'pCR4-TOPO-left' : 'catgattacgccaagctcagaattaaccctcactaaagggactagtcctgcaggtttaaacgaattcgccctt',
    'pCR4-TOPO-right' : 'aagggcgaattcgcggccgctaaattcaattcgccctatagtgagtcgtattacaattca'
}

def align2left(left,right):
    """Align 2 seqs, forcing alignment of right-end of left.
    
                     ...RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR...
    ...LLLLLLLLLLLLLLLLLLLLLLLLLLL  <- (forced aln here)
    
    Uses exonerate.
    """
    cmd = exonerate.ExonerateCommand('findend','parsable')
    
    try:
        (fdq,query) = tempfile.mkstemp()
        (fdt,target) = tempfile.mkstemp()
    finally:
        
    
    
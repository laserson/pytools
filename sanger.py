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

def trimleft(left,read):
    """Align 2 seqs, forcing alignment of right-end of left.
    
                     ...RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR...
    ...LLLLLLLLLLLLLLLLLLLLLLLLLLL  <- (forced aln here)
    
    Uses exonerate.
    """
    # perform alignment
    cmd = exonerate.ExonerateCommand('findend','parsable','bestonly')
    rawaln = exonerate.run_exonerate2(cmd,left,read)
    aln = exonerate.parse_aln(rawaln)
    
    # check that the right-end of left was successfully placed
    if aln['query_len'] != aln['query_aln_end']:
        raise ValueError, "failed to align right-end of left sequence"
    
    # return trimmed sequence
    return read[aln['target_aln_end']:]

def trimright(right,read):
    """Align 2 seqs, forcing alignment of left-end of right.
    
    ...DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD...
        (forced aln here) -> RRRRRRRRRRRRRRRRRRRRRRRRRRRRR...
    
    Uses exonerate.
    """
    # perform alignment
    cmd = exonerate.ExonerateCommand('findend','parsable','bestonly')
    rawaln = exonerate.run_exonerate2(cmd,right,read)
    aln = exonerate.parse_aln(rawaln)
    
    # check that the left-end of right was successfully placed
    if aln['query_aln_end'] != 0:
        raise ValueError, "failed to align left-end of right sequence"
    
    # return trimmed sequence
    return read[aln['target_aln_start']:]

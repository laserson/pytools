from numpy import array, power, log, log10, log1p, choose, sum
from Bio import SeqIO
from itertools import izip
from seqtools import reverse_complement

def stitch(record1, record2):
    seq1 = array([record1.seq.tostring()])
    seq2 = array([reverse_complement(record2.seq.tostring())])
    seq1.dtype = '|S1'
    seq2.dtype = '|S1'
    quals1 = array(record1.letter_annotations['phred_quality'])
    quals2 = array(record2.letter_annotations['phred_quality'][::-1])
    
    log10p_consensus_1 = log1p(-power(10, -quals1 / 10.)) / log(10)
    log10p_consensus_2 = log1p(-power(10, -quals2 / 10.)) / log(10)
    log10p_error_1 = -log10(3) - (quals1 / 10.)
    log10p_error_2 = -log10(3) - (quals2 / 10.)
    
    min_overlap = 1
    max_overlap = max(len(record1), len(record2))
    overlaps = {}
    for overlap in range(1, max_overlap):
        s1 = seq1[-overlap:]
        s2 = seq2[:overlap]
        q1 = quals1[-overlap:]
        q2 = quals2[:overlap]
        lpc1 = log10p_consensus_1[-overlap:]
        lpc2 = log10p_consensus_2[:overlap]
        lpe1 = log10p_error_1[-overlap:]
        lpe2 = log10p_error_2[:overlap]
        
        consensus = choose(q1 < q2, [s1, s2])
        score = sum(choose(consensus == s1, [lpe1, lpc1])) + sum(choose(consensus == s2, [lpe2, lpc2])) + len(consensus) * log10(4) * 2    # last term is null hypothesis, p=1/4
        consensus.dtype = '|S%i' % len(consensus)
        overlaps[overlap] = (consensus[0],score)
    
    return overlaps

import numpy as np

input_file1 = '/n/home00/laserson/data/MS_HIV_MiSeq_data_20120105/samples/HIV1.1.fastq'
input_file2 = '/n/home00/laserson/data/MS_HIV_MiSeq_data_20120105/samples/HIV1.2.fastq'

input_file1 = '/Users/laserson/Dropbox/stitcher/test.1.fastq'
input_file2 = '/Users/laserson/Dropbox/stitcher/test.2.fastq'

it = izip(SeqIO.parse(input_file1,'fastq'), SeqIO.parse(input_file2,'fastq'))
(record1,record2) = it.next()
overlaps = stitch(record1,record2)
scores = [p[1] for p in overlaps.values()]
(entropy(power(10,scores)), max(overlaps.items(),key=lambda i: i[1][1]))

entropies = []
for (i,(rec1,rec2)) in enumerate(izip(SeqIO.parse(input_file1,'fastq'), SeqIO.parse(input_file1,'fastq'))):
    entropies.append(stitch(rec1,rec2))
    if i == 1000:
        break
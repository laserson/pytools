import sys

from Bio import SeqIO
import numpy as np

import seqtools
import oligoTm
import unafold
import blat

# ==================
# = Output primers =
# ==================

def output_primers(primers,names):
    datum = ('name','sequence','len','Tm',r'%GC','ss-dG','BLAT')
    header = "\n%-25s %-30s %-4s %-5s %-4s %-7s %-5s\n" % datum
    sys.stdout.write(header)
    
    lens = map(len,primers)
    Tms = map(oligoTm.oligo_Tm,primers)
    gcs = map(lambda p: seqtools.gc_content(p)*100,primers)
    dGs = map(lambda p: unafold.hybrid_ss_min(p,NA='DNA',sodium=0.05),primers)
    # trunc_primers = [p[-min(18,min(lens)):] for p in primers]
    trunc_primers = primers # NO TRUNCATION
    seqrecords = map(lambda t: seqtools.make_SeqRecord(*t),zip(names,trunc_primers))
    blat_hits = map(blat.search_sequence,seqrecords)
    
    for datum in zip(names,primers,lens,Tms,gcs,dGs,blat_hits):
        primer_string = "%-25s %-30s %-4i %-5.1f %-4.0f %-7.1f %-5i\n" % datum
        sys.stdout.write(primer_string)
    
    summary_data = lambda d: (np.mean(d),np.std(d),np.min(d),np.max(d))
    
    sys.stdout.write('\nsummary:\n')
    sys.stdout.write('num primers: %i\n' % len(primers))
    sys.stdout.write('len    mean: %5.1f    std: %5.1f    min: %5.1f    max %5.1f\n' % summary_data(lens))
    sys.stdout.write('Tm     mean: %5.1f    std: %5.1f    min: %5.1f    max %5.1f\n' % summary_data(Tms))
    sys.stdout.write('%%GC    mean: %5.1f    std: %5.1f    min: %5.1f    max %5.1f\n' % summary_data(gcs))
    sys.stdout.write('dGs    mean: %5.1f    std: %5.1f    min: %5.1f    max %5.1f\n' % summary_data(dGs))
    sys.stdout.write('BLAT  mean: %5.1f    std: %5.1f    min: %5.1f    max %5.1f    total: %5.1f\n' % (summary_data(blat_hits)+(np.sum(blat_hits),)))

if __name__ == '__main__':
    
    if len(sys.argv) == 3:
        inhandle = open(sys.argv[1],'r')
        outhandle = open(sys.argv[2],'w')
    elif len(sys.argv) == 2:
        inhandle = open(sys.argv[1],'r')
        outhandle = sys.stdout
    elif len(sys.argv) == 1:
        inhandle = sys.stdin
        outhandle = sys.stdout
    
    seqrecords = list(SeqIO.parse(inhandle,'fasta'))
    names = [rec.id for rec in seqrecords]
    primers = [seqtools.get_string(rec) for rec in seqrecords]
    
    if not blat.is_server_running():
        blat_server = blat.start_gfServer()
    
    output_primers(primers,names)
    
    # if blat.is_server_running():
    #     blat.stop_gfServer( blat_server )


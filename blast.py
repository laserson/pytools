import sys
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML

def number_genome_qblast_hits(seqreclist):
    fastastring = ''.join([rec.format('fasta') for rec in seqreclist])
    results_handle = NCBIWWW.qblast('blastn','nr',fastastring,expect=1.,word_size=7,nucl_reward=1,nucl_penalty=-3,hitlist_size=1000)
    blast_records = NCBIXML.parse(results_handle)
    
    hits = [len(record.alignments) for record in blast_records]
    
    return hits


# def number_genome_qblast_hits(seqlist):
#     fastastring = ''
#     for (i,seq) in enumerate(seqlist): fastastring += '>seq%i\n%s\n' % (i,seq)
#     
#     results_handle = NCBIWWW.qblast('blastn','nr',fastastring,expect=0.1,word_size=7,nucl_reward=1,nucl_penalty=-3,hitlist_size=500)
#     blast_records = NCBIXML.parse(results_handle)
#     
#     total_hits = 0
#     for record in blast_records: total_hits += len(record.alignments)
#     
#     # print total_hits
#     # sys.stdout.flush()
#     
#     return total_hits

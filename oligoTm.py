import math

from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

def oligoTm(seqobj):
    """Computes the melting temp based on the NN model.
    
    (Originated from Kun Zhang)
    """
    
    if isinstance(seqobj,SeqRecord):
        seq = seqobj.seq.tostring().upper()
    elif isinstance(seqobj,Seq):
        seq = seqobj.tostring().upper()
    elif isinstance(seqobj,str):
        seq = seqobj.upper()
    
    # set the default Tm parameters
    C_primer = 250.0 # nM
    C_Mg = 0.0 # mM  #1.5 # 10mM intracellular concentration
    C_MonovalentIon = 50.0 #mM #10mM Tris-Cl in 9N Ligase  
    C_dNTP = 0.0 #mM #0.8 #mM
    percentage_DMSO = 0
    percentage_annealed = 50
    
    percentage_annealed = percentage_annealed/100.0
    percentage_DMSO = percentage_DMSO/100.0
    
    #Some constants
    R = 1.987
    deltaH = dict()
    deltaS = dict()
    deltaH =  {     "AA": -7.6,  "TT": -7.6, "AT": -7.2, "TA": -7.2, "CA": -8.5, "TG": -8.5, "GT": -8.4, "AC": -8.4,"CT": -7.8, "AG": -7.8, "GA": -8.2, "TC": -8.2,"CG": -10.6,"GC": -9.8, "GG": -8.0, "CC": -8.0, "A": 2.2, "T": 2.2, "G": 0.0, "C": 0.0}
    deltaS = { "AA": -21.3, "TT": -21.3, "AT": -20.4, "TA": -21.3, "CA": -22.7, "TG": -22.7, "GT": -22.4, "AC": -22.4, "CT": -21.0, "AG": -21.0, "GA": -22.2, "TC": -22.2,"CG": -27.2, "GC": -24.4, "GG": -19.9, "CC":-19.9, "A": 6.9, "T": 6.9, "G": 0.0, "C": 0.0}
    
    C_SodiumEquivalent = C_MonovalentIon + 120 * math.sqrt(C_Mg-C_dNTP)
    seqLength = len(seq)
    dH = 0.2 + deltaH[str(seq[0])] + deltaH[str(seq[len(seq)-1])]
    dS = -5.7 + deltaS[seq[0]] + deltaS[seq[len(seq)-1]]
    for i in range(0, seqLength - 1):
        dH += deltaH[str(seq[i:i+2])]
        dS +=  deltaS[seq[i:i+2]]
    dS = dS + 0.368 * seqLength * math.log(C_SodiumEquivalent/1000.0)
    #val = math.log(C_primer*(1-percentage_annealed)/percentage_annealed)
    Tm =(dH * 1000) / (dS + R * (math.log(C_primer*(1-percentage_annealed)/percentage_annealed)-21.4164)) - 273.15 - 0.75*percentage_DMSO
    return Tm

oligo_Tm = oligoTm
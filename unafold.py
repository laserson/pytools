import os
import glob
import random
import tempfile
import subprocess

def hybrid_ss_min(seq,NA='RNA',tmin=37,tinc=1,tmax=37,sodium=1,magnesium=0):
    cmd = 'hybrid-ss-min --quiet --NA=%s --tmin=%f --tinc=%f --tmax=%f --sodium=%f --magnesium=%f %s' % (NA,tmin,tinc,tmax,sodium,magnesium,seq)
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    p.wait()
    dG = float(p.stdout.read())
    return dG

def hybrid_min(seq1,seq2,NA='RNA',tmin=37,tinc=1,tmax=37,sodium=1,magnesium=0):
    cmd = 'hybrid-min --quiet --NA=%s --tmin=%f --tinc=%f --tmax=%f --sodium=%f --magnesium=%f %s %s' % (NA,tmin,tinc,tmax,sodium,magnesium,seq1,seq2)
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    p.wait()
    dG = float(p.stdout.read().split()[0])
    return dG

def hybrid_min_list(seqlist1,seqlist2,NA='RNA',tmin=37,tinc=1,tmax=37,sodium=1,magnesium=0):
    # set up temporary files
    temp_out_prefix = 'temporary_hybrid_%i_%i' % (os.getpid(),random.randint(0,10000))
    seqfile1 = tempfile.NamedTemporaryFile(mode='w',dir='.',prefix='hybrid_min_temp',suffix='.fasta')
    seqfile2 = tempfile.NamedTemporaryFile(mode='w',dir='.',prefix='hybrid_min_temp',suffix='.fasta')
    for (i,seq) in enumerate(seqlist1): print >>seqfile1, ">1_%i\n%s" % (i,seq)
    for (i,seq) in enumerate(seqlist2): print >>seqfile2, ">2_%i\n%s" % (i,seq)
    seqfile1.file.flush()
    seqfile2.file.flush()
    
    # set up and execute command
    cmd = 'hybrid-min --NA=%s --tmin=%f --tinc=%f --tmax=%f --sodium=%f --magnesium=%f --output=%s %s %s' % (NA,tmin,tinc,tmax,sodium,magnesium,temp_out_prefix,seqfile1.name,seqfile2.name)
    p = subprocess.Popen(cmd,shell=True)
    p.wait()
    
    # read results
    ip = open(temp_out_prefix+'.dG','r')
    dGs = []
    for line in ip:
        if line.startswith('#'): continue
        dGs.append(float(line.split()[1]))
    
    # clean up output
    seqfile1.close()
    seqfile2.close()
    for filename in glob.glob(temp_out_prefix+'*'): os.remove(filename)
    
    return dGs

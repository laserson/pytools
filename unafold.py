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

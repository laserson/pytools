# BLAT tools
# based on Sri's code

import sys
import subprocess
import os
import signal
import time

import seqtools

hg_idx = '~/genome/hg19.2bit'

def start_gfServer(file2idx=hg_idx,tileSize=10,stepSize=2,minMatch=2,maxGap=4,repMatch=1000000,debug=False):
    params = (tileSize,stepSize,minMatch,maxGap,repMatch,file2idx)
    cmd = "gfServer start -tileSize=%i -stepSize=%i -minMatch=%i -maxGap=%i -repMatch=%i localhost 17779 %s" % params
    if debug: print "Command is:\n%s" % cmd
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    time.sleep(240)
    print "Finished starting up BLAT server (hopefully)."
    return p

def is_server_running():
    p = subprocess.Popen('ps -A',shell=True,stdout=subprocess.PIPE)
    lines = p.stdout.readlines()
    for line in lines:
        if 'gfServer' in line:
            return True
    return False

def stop_gfServer(p=None):
    if p != None:
        os.kill(p.pid,signal.SIGTERM)
        time.sleep(5)
    else:
        pids = []
        p = subprocess.Popen('ps -A',shell=True,stdout=subprocess.PIPE)
        lines = p.stdout.readlines()
        for line in lines:
            if 'gfServer' in line:
                pids.append(int(line.split()[0]))
        for pid in pids:
            os.kill(pid,signal.SIGTERM)
            time.sleep(5)

# HACK/BUG: for some reason gfClient is doubling the directory prefix.  It works if
#           file2idx='/'
def search_sequences(seqs,file2idx=hg_idx,minScore=20,minIdentity=70,debug=False):
    if not is_server_running():
        raise RuntimeError, "BLAT server not running."
    
    # generate query
    if hasattr(seqs[0],'format'):
        query = ''.join([s.format('fasta') for s in seqs])
    else:
        query = ''.join(['>query%i\n%s\n' % (i,s) for (i,s) in enumerate(seqs)])
    
    # define and run command
    nibdir = os.path.dirname(file2idx)
    params = (minScore,minIdentity,nibdir)
    cmd = "gfClient -minScore=%i -minIdentity=%i -nohead localhost 17779 %s /dev/stdin /dev/stdout" % params
    p = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    p.stdin.write( query )
    p.stdin.close()
    
    # process output
    num = 0
    for line in p.stdout:
        if debug: print line
        if line == "Output is in /dev/stdout\n":
            continue
        num += 1
    
    return num

def search_sequence(seq,file2idx=hg_idx,minScore=20,minIdentity=50,debug=False):
    return search_sequences([seq],file2idx=hg_idx,minScore=5,minIdentity=50,debug=False)

import os
import tempfile
import subprocess

import seqtools

class ExonerateCommand(object):
    """Build command for exonerate"""
    
    options_list = [
        'query',
        'target',
        'querytype',
        'targettype',
        'querychunkid',
        'querychunktotal',
        'targetchunkid',
        'targetchunktotal',
        'verbose',
        'exhaustive',
        'bigseq',
        'forcescan',
        'saturatethreshold',
        'customserver',
        'fastasuffix',
        'model',
        'score',
        'percent',
        'showalignment',
        'showsugar',
        'showcigar',
        'showvulgar',
        'showquerygff',
        'showtargetgff',
        # 'ryo',    NOTE: this is left out as it requires special handling
        'bestn',
        'subopt',
        'gappedextension',
        'refine',
        'refineboundary',
        'dpmemory',
        'compiled',
        'terminalrangeint',
        'terminalrangeext',
        'joinrangeint',
        'joinrangeext',
        'spanrangeint',
        'spanrangeext',
        'extensionthreshold',
        'singlepass',
        'joinfilter',
        'annotation',
        'softmaskquery',
        'softmasktarget',
        'dnasubmat',
        'proteinsubmat',
        'fsmmemory',
        'forcefsm',
        'wordjump',
        'gapopen',
        'gapextend',
        'codongapopen',
        'codongapextend',
        'minner',
        'maxner',
        'neropen',
        'minintron',
        'maxintron',
        'intronpenalty',
        'frameshift',
        'useaatla',
        'geneticcode',
        'hspfilter',
        'useworddropoff',
        'seedrepeat',
        'dnawordlen',
        'proteinwordlen',
        'codonnwordlen',
        'dnahspdropoff',
        'proteinhspdropoff',
        'codonhspdropoff',
        'dnahspthreshold',
        'proteinhspthreshold',
        'codonhspthreshold',
        'dnawordlimit',
        'proteinwordlimit',
        'codonwordlimit',
        'geneseed',
        'geneseedrepeat',
        'alignmentwidth',
        'forwardcoordinates',
        'quality',
        'splice3',
        'splice5',
        'forcegtag']
    
    
    def __init__(self, *args, **kw):
        # register preset handlers
        self.register = {
            'affine:local' : self.preset_affinelocal,
            'affine:global' : self.preset_affineglobal,
            'findend' : self.preset_findend,
            'parsable' : self.preset_parsable,
            'pretty' : self.preset_pretty,
            'bestonly' : self.preset_bestonly,
            'ungapped' : self.preset_ungapped
        }
        
        # these attributes must be handled special, and set manually at the start
        self.options = {}
        self.ryo = None
        
        # first execute any registered functions
        for a in args:
            self.register[a]()
        
        # check for ryo output and save it (needs special handling)
        if kw.has_key('ryo'): self.ryo = kw.pop('ryo')
        
        # then set all the manual options supplied
        self.options.update(kw)
        
        # set standard options in case they weren't given initially
        # they can still be overwritten
        self.softset_default()
        
        # return self
    
    def __setattr__(self,name,value):
        """Allows setting of options by acting on object attributes.
        
        For example:
        cmd = ExonerateCommand()
        cmd.querytype = 'dna'
        
        Catches the special cases of ryo and options.
        ryo needs to be set manually
        options shouldn't be overwritten, but lets you...
        """
        if name in ExonerateCommand.options_list:
            self.options[name] = value
        else:
            object.__setattr__(self,name,value)
    
    def __getattr__(self,name):
        if name in ExonerateCommand.options_list:
            return self.options[name]
        else:
            raise AttributeError
    
    def build_command(self):
        self.cmd = 'exonerate'
        for (option,value) in self.options.iteritems():
            self.cmd += ' --%s %s' % (option,value)
        
        # handle ryo output using raw string
        if self.ryo is not None:
            self.cmd += r' --%s "%s"' % ('ryo',self.ryo)
        
        return self.cmd
    
    def softset_default(self):
        """Conditionally override options to a reasonable default."""
        if not self.options.has_key('model'):
            self.model = 'affine:local'
        if not self.options.has_key('querytype'):
            self.querytype = 'dna'
        if not self.options.has_key('targettype'):
            self.targettype = 'dna'
    
    def hardset_preset(self,*args):
        for a in args:
            register[a](self)
    
    def preset_affinelocal(self):
        self.model = 'affine:local'
    
    def preset_affineglobal(self):
        self.model = 'affine:global'
        self.exhaustive = True
    
    def preset_ungapped(self):
        self.model = 'ungapped'
        self.exhaustive = True
    
    def preset_findend(self):
        self.model = 'affine:overlap'
        self.exhaustive = True
    
    def preset_parsable(self):
        self.verbose = 0
        # self.showalignment = False
        # self.showvulgar = False
        self.ryo = 'aln_summary: %qi %ql %qab %qae %qS %ti %tl %tab %tae %tS %s %et %ei %pi\n'
    
    def preset_pretty(self):
        self.showalignment = True
        self.showvulgar = True
        self.showsugar = True
    
    def preset_bestonly(self):
        self.bestn = 1

def run_exonerate(cmd,query=None,target=None):
    """Run exonerate using given ExonerateCommand object
    
    query and target must refer to files
    """
    # check query and target are set properly
    if query is not None: cmd.query = query
    if target is not None: cmd.target = target
    try:
        cmd.query
        cmd.target
    except KeyError:
        print "cmd.query or cmd.target is not set"
        raise
    
    # submit process
    p = subprocess.Popen(cmd.build_command(),shell=True,stdout=subprocess.PIPE)
    aln = p.stdout.read()
    p.wait()
    return aln

def run_exonerate2(cmd,query,target,queryname='query',targetname='target',debug=False):
    """Perform pairwise alignment using cmd ExonerateCommand object
    
    query and target are sequences
    """
    # TODO: see if this can be implemented without writing to temporary files
    
    # write seqs to tempfiles
    (fdq,queryfile) = tempfile.mkstemp()
    (fdt,targetfile) = tempfile.mkstemp()
    iopq = open(queryfile,'w')
    iopt = open(targetfile,'w')
    print >>iopq, ">%s\n%s\n" % (queryname,query)
    print >>iopt, ">%s\n%s\n" % (targetname,target)
    iopq.close()
    iopt.close()
    os.close(fdq)
    os.close(fdt)
    
    try:
        # perform alignment
        cmd.query = queryfile
        cmd.target = targetfile
        aln = run_exonerate(cmd)
    finally:
        # clean up
        os.remove(queryfile)
        os.remove(targetfile)
    
    if debug: print aln
    
    return aln

def iter_alnsummary(rawaln):
    """Return alnsummary line from rawaln."""
    for line in rawaln.split('\n'):
        if line.startswith('aln_summary'):
            yield line

def extract_alnsummary(rawaln):
    """Return alnsummary line from rawaln."""
    return iter_alnsummary(rawaln).next()

def iter_vulgar(rawaln):
    """Return vulgar line from rawaln."""
    for line in rawaln.split('\n'):
        if line.startswith('vulgar'):
            yield line

def extract_vulgar(rawaln):
    """Return vulgar line from rawaln."""
    return iter_vulgar(rawaln).next()

def iter_alnsummary_vulgar(rawaln):
    for (alnsummary,vulgar_commands) in zip(iter_alnsummary(rawaln),iter_vulgar(rawaln)):
        yield (alnsummary,vulgar_commands)

def parse_alnsummary(rawalnsummary):
    """Parse alignment from exonerate using 'parsable' preset.
    
    Takes an alnsummary line from an alignment that was generated from an ryo
    'parsable' preset.
    """
    # 'aln_summary: %qi %ql %qab %qae %qS %ti %tl %tab %tae %tS %s %et %ei %pi\n'
    data = rawalnsummary.split()
    
    aln = {}
    aln['query_id']         = data[1]
    aln['query_len']        = int(data[2])
    aln['query_aln_begin']  = int(data[3])
    aln['query_aln_end']    = int(data[4])
    aln['query_strand']     = data[5]
    aln['target_id']        = data[6]
    aln['target_len']       = int(data[7])
    aln['target_aln_begin'] = int(data[8])
    aln['target_aln_end']   = int(data[9])
    aln['target_strand']    = data[10]
    aln['score']            = int(data[11])
    aln['equiv_total']      = int(data[12])
    aln['equiv_id']         = int(data[13])
    aln['percent_id']       = float(data[14])
    
    return aln

def parse_vulgar(rawvulgar):
    """Parse vulgar line
    
    Takes vulgar line from alignment output
    
    returns only the non-sugar part that allows you to build the aln
    """
    data = rawvulgar.split()[10:]
    cmds = []
    for i in range(0,len(data),3):
        cmds.append( (data[0],int(data[1]),int(data[2])) )
    return cmds

def build_aln(alnsummary,vulgar_commands,queryseq,targetseq):
    """Build full alignment from exonerate using 'parsable' preset and vulgar output"""
    
    queryname = alnsummary['query_id']
    targetname = alnsummary['target_id']
    
    # process strands. the position vars below will always progress
    # from 0->len(seq), so the seqs must be revcomped accordingly
    
    queryposition  = alnsummary['query_aln_begin']
    targetposition = alnsummary['target_aln_begin']
    if alnsummary['query_strand'] == '-':
        queryseq = seqtools.reverse_complement(queryseq)
        queryposition = len(queryseq) - queryposition
    if alnsummary['target_strand'] == '-':
        targetseq = seqtools.reverse_complement(targetseq)
        targetposition = len(targetseq) - targetposition
    pad = abs(queryposition - targetposition)
    
    # build alignment
    queryaln  = ''
    targetaln = ''
    
    # process necessary padding
    if queryposition > targetposition:
        targetaln = ' ' * pad
    else:
        queryaln  = ' ' * pad
    
    # add pre-aln sequence
    queryaln  += queryseq[0:queryposition]
    targetaln += targetseq[0:targetposition]
    
    # walk through alignment (from vulgar output)
    for cmd in vulgar_commands:
        if cmd[0] == 'M':
            assert(cmd[1]==cmd[2])
            queryaln  += queryseq[queryposition:queryposition+cmd[1]]
            targetaln += targetseq[targetposition:targetposition+cmd[2]]
            queryposition  += cmd[1]
            targetposition += cmd[2]
        elif cmd[0] == 'G':
            assert( (cmd[1]==0) != (cmd[1]==0) )    # xor
            if cmd[1] == 0:
                queryaddendum = '-' * cmd[2]
                targetaddendum = targetseq[targetposition:targetposition+cmd[2]]
            elif cmd[2] == 0:
                queryaddendum = queryseq[queryposition:queryposition+cmd[1]]
                targetaddendum = '-' * cmd[1]
            queryaln  += queryaddendum
            targetaln += targetaddendum
            queryposition  += cmd[1]
            targetposition += cmd[2]
        else:
            raise ValueError, "I do not understand the vulgar command %s" % cmd[0]
   
    # add any post-aln sequence
    queryaln  += queryseq[queryposition:]
    targetaln += targetseq[targetposition:]
    
    return (queryaln,targetaln)

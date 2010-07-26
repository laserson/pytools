import os
import tempfile
import subprocess

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
            'findend' : self.preset_findend,
            'parsable' : self.preset_parsable,
            'pretty' : self.preset_pretty,
            'bestonly' : self.preset_bestonly
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
    
    def preset_findend(self):
        self.model = 'affine:overlap'
        self.exhaustive = True
    
    def preset_parsable(self):
        self.verbose = 0
        self.showalignment = False
        self.showvulgar = False
        self.ryo = 'aln_summary: %qi %ql %qab %qae %qS %ti %tl %tab %tae %tS %s %et %ei %pi\n'
    
    def preset_pretty(self):
        # TODO: human-readable output
        pass
    
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

def run_exonerate2(cmd,query,target):
    """Perform pairwise alignment using cmd ExonerateCommand object
    
    query and target are sequences
    """
    # TODO: see if this can be implemented without writing to temporary files
    
    # write seqs to tempfiles
    (fdq,queryfile) = tempfile.mkstemp()
    (fdt,targetfile) = tempfile.mkstemp()
    iopq = open(queryfile,'w')
    iopt = open(targetfile,'w')
    print >>iopq, ">query\n%s\n" % query
    print >>iopt, ">target\n%s\n" % target
    iopq.close()
    iopt.close()
    
    try:
        # perform alignment
        cmd.query = queryfile
        cmd.target = targetfile
        aln = run_exonerate(cmd)
    finally:
        # clean up
        os.remove(queryfile)
        os.remove(targetfile)
    
    return aln

def parse_aln(rawaln):
    """Parse alignment from exonerate using 'parsable' preset"""
    
    # 'aln_summary: %qi %ql %qab %qae %qS %ti %tl %tab %tae %tS %s %et %ei %pi\n'
    data = rawaln.split()
    
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

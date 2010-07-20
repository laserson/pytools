class ExonerateCommand(object):
    """Build command for exonerate"""
    
    register = {
        'affine:local' : self.preset_affinelocal,
        'findend' : self.preset_findend,
        'parsable' : self.preset_parsable,
        'pretty' : self.preset_pretty
    }
    
    def __init__(self, *args, **kw):
        # first execute any registered functions
        for a in args:
            register[a]()
        
        # check for ryo output and save it (needs special handling)
        if kw.has_key('ryo'): self.ryo = kw.pop('ryo')
        
        # then set all the manual options supplied
        self.options = kw
        
        # set standard options in case they weren't given initially
        # they can still be overwritten
        self.softset_default()
        
        return self
    
    def __setattr__(self,name,value):
        """Allows setting of options by acting on object attributes.
        
        For example:
        cmd = ExonerateCommand()
        cmd.querytype = 'dna'
        
        Catches the special cases of ryo and options.
        ryo needs to be set manually
        options shouldn't be overwritten, but lets you...
        """
        if name in self.__dict__:
            object.__setattr__(self,name,value)
        else:
            self.options[name] = value
    
    def __getattr__(self,name):
        if name in self.__dict__:
            return object.__setattr__(self,name)
        else:
            return self.options[name]
    
    def build_command(self):
        self.cmd = 'exonerate'
        for (option,value) in self.options.iteritems():
            self.cmd += ' --%s %s' % (option,value)
        
        # handle ryo output using raw string
        if self.ryo is not None:
            self.cmd += r' --%s "%s"' % ('ryo',self.ryo)
        
        return cmd
    
    def softset_default(self):
        """Conditionally override options to a reasonable default."""
        if not self.options.has_key('model'):
            self.model = 'affine:local'
        if not self.options.has_key('querytype'):
            self.querytype = 'dna'
        if not self.options.has_key('targettype'):
            self.targettype = 'dna'
    
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

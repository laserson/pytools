import copy

from Bio.Seq import Seq, UnknownSeq
from Bio.SeqRecord import SeqRecord
from Bio.SeqFeature import SeqFeature, FeatureLocation
from Bio.Alphabet import NucleotideAlphabet


class SeqRecordLite(object):
    """SeqRecord wrapper that allows simpler attribute access.
    
    The underlying data structure is actually a biopython `SeqRecord` object.
    This class wraps it in a way that maintains the simple-to-use interface to
    get at some common annotations. It also knows how to print out it's data
    as IMGT-flavored INSDC (e.g., GenBank/EMBL).
    """
    
    def __init__(self, biopython_object=None):
        
        # first we define our underlying SeqRecord object
        if biopython_object == None:
            self._record = SeqRecord(seq=UnknownSeq(0,alphabet=NucleotideAlphabet()),id='',name='',description='')
        elif isinstance(biopython_object,Seq):
            self._record = SeqRecord(seq=copy.deepcopy(biopython_object),id='',name='',description='')
        elif isinstance(biopython_object,SeqRecord):
            self._record = copy.deepcopy(biopython_object)
        
        # define dictionary of features for faster lookup
        self._features = {}
        for (i,feature) in enumerate(self._record.features):
            self._features.setdefault(feature.type,[]).append(i)
    
    
    def __getattr__(self,name):
        # This function should only get called if I am looking for an attribute that
        # didn't already have a getter defined or a default method.  In this case, I
        # search the annotations dictionary or the features table of the underlying
        # SeqRecord to try to find the information.
        if name in self._record.annotations:
            return self._record.annotations[name]
        elif name in self._features:
            return [self._record.features[i] for i in self._features[name]]
        raise AttributeError
    
    
    # define properties to access some common SeqRecord interface
    
    @property
    def seq(self):
        return self._record.seq
    
    @seq.setter
    def seq(self,s):
        self._record.seq = s
    
    @property
    def annotations(self):
        return self._record.annotations
    
    @property
    def id(self):
        return self._record.id
    
    @id.setter
    def id(self,i):
        self._record.id = i
    
    @property
    def description(self):
        return self._record.description
    
    @description.setter
    def description(self,d):
        self._record.description = d
    
    @property
    def name(self):
        return self._record.name
    
    @name.setter
    def name(self,n):
        self._record.name = n
    
    @property
    def features(self):
        return self._record.features
    
    def format(self,*args,**kw):
        return self._record.format(*args,**kw)
    
    
    # manipulation of SeqRecord parts
    
    def add_feature(self,start=None,end=None,type='',strand=None,qualifiers=None):
        if start == None or end == None:
            raise ValueError, "if there is no spanning location...use an annotation?"
        location = FeatureLocation(start,end)
        feature = SeqFeature(location=location,type=type,strand=strand,qualifiers=qualifiers)
        self._record.features.append(feature)
        self._features.setdefault(feature.type,[]).append(len(self._record.features) - 1)
        return self
    
    def has_feature(self,type):
        return type in self._features
    
    def del_feature(self,type):
        idxs = self._features.pop(type)
        idxs.sort(reverse=True)
        for i in idxs:
            self._record.features.pop(i)
        return self
    
    
    # some standard interface
    
    def __len__(self):
        return len(self.seq)
    
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return self.format('imgt')

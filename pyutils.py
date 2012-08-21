import copy
import string
import collections
import contextlib

@contextlib.contextmanager
def as_handle(handleish, mode='r', **kwargs):
    """Open handleish as file.
    
    Stolen from Biopython
    """
    if isinstance(handleish, basestring):
        with open(handleish, mode, **kwargs) as fp:
            yield fp
    else:
        yield handleish

# for generating 'safe' filenames from identifiers
cleanup_table = string.maketrans('/*|><+ ','_____p_')
def cleanup_id(identifier):
    return identifier.translate(cleanup_table)


class nesteddict(collections.defaultdict):
    """Nested dictionary structure.
    
    Based on Stack Overflow question 635483
    """
    def __init__(self,default=None):
        if default == None:
            collections.defaultdict.__init__(self, nesteddict)
        else:
            collections.defaultdict.__init__(self, default)
        self.locked = False
    
    def lock(self):
        # self.default_factory = raiseKeyError
        self.default_factory = None
        self.locked = True
        for value in self.itervalues():
            if isinstance(value, nesteddict):
                value.lock()
    
    def unlock(self):
        self.default_factory = nesteddict
        self.locked = False
        for value in self.itervalues():
            if isinstance(value, nesteddict):
                value.unlock()
    
    def islocked(self):
        return self.locked
    
    def todict(self):
        raise NotImplementedError
        for (key,val) in self.iteritems():
            if isinstance(val,nesteddict):
                val.todict()
                self[key] = dict(val)
        self = dict(self)
    
    @staticmethod
    def asdict(d):
        d = copy.deepcopy(d)
        for (key,val) in d.iteritems():
            if isinstance(val,nesteddict):
                d[key] = nesteddict.asdict(val)
        return dict(d)
    
    def nested_setdefault(self,keylist,default):
        curr_dict = self
        for key in keylist[:-1]:
            curr_dict = curr_dict[key]
        key = keylist[-1]
        return curr_dict.setdefault(key,default)
    
    def nested_get(self,keylist,default):
        curr_dict = self
        for key in keylist[:-1]:
            curr_dict = curr_dict[key]
        key = keylist[-1]
        return curr_dict.get(key,default)
    
    def nested_assign(self,keylist,val):
        curr_dict = self
        for key in keylist[:-1]:
            curr_dict = curr_dict[key]
        key = keylist[-1]
        curr_dict[key] = val
        return self
    
    def walk(self):
        for (key,value) in self.iteritems():
            if isinstance(value, nesteddict):
                for tup in value.walk():
                    yield (key,) + tup
            else:
                yield (key,value)
    
    # these functions below implement special cases of nesteddict, where the
    # deepest-level dict is of a particular type (e.g., int for counter, set
    # for uniq objects, etc.)
    # 
    # These functions could be implemented with nested_setdefault and
    # nested_get, but would be less efficient since they would have to
    # traverse the dict structure more times.
    
    def nested_increment(self,keylist,increment=1):
        curr_dict = self
        for key in keylist[:-1]:
            curr_dict = curr_dict[key]
        key = keylist[-1]
        curr_dict[key] = curr_dict.get(key,0) + increment
    
    def nested_add(self,keylist,obj):
        curr_dict = self
        for key in keylist[:-1]:
            curr_dict = curr_dict[key]
        key = keylist[-1]
        curr_dict.setdefault(key,set()).add(obj)









# class ModuleWrapper(object):
#     """Wrap a module to allow user-defined __getattr__
#     
#     see http://stackoverflow.com/questions/2447353/getattr-on-a-module
#     """
#     def __init__(self, module, usergetattr):
#         self.module = module
#         self.usergetattr = usergetattr
#     
#     def __getattr__(self, name):
#         return self.usergetattr(self,name)

import collections

class nesteddict(collections.defaultdict):
    def __init__(self):
        defaultdict.__init__(self, nesteddict)
    
    def walk(self):
        for (key,value) in self.iteritems():
            if isinstance(value, nesteddict):
                for tup in value.walk():
                    yield (key,) + tup
            else:
                yield (key,value)


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

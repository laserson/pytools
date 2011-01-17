import math
import types
import numbers
import bisect

import numpy as np

def is_iterable(x):
    try:
        iter(x)
        return True
    except TypeError:
        return False

class quantitative(object):
    """Implement abstract quantitative scale."""
    
    def __init__(self, *args):
        self._domain = [0,1]
        self._range  = [0,1]
        
        self._transform = lambda x: x
        self._inverse = lambda y: y
        
        self.domain(*args)
    
    def _in_domain(self,x):
        return (x >= min(self._domain)) and (x <= max(self._domain))
    
    def _in_range(self,y):
        return (y >= min(self._range)) and (y <= max(self._range))
    
    def __call__(self,x):
        if not self._in_domain(x):
            raise ValueError, "outside domain"
        segment = bisect.bisect_right(self._domain,x) - 1
        if segment + 1 == len(self._domain): segment -= 1   # deal with extra endpoint (fully closed interval), e.g., [0,1) [1,2) [2,3]
        return (self._transform(x) - self._transform(self._domain[segment])) / (self._transform(self._domain[segment+1]) - self._transform(self._domain[segment])) * (self._range[segment+1] - self._range[segment]) + self._range[segment]
    
    def domain(self,*args):
        if len(args) == 0:
            return self._domain
        elif is_iterable(args[0]):  # given array of data from which to determine domain
            if len(args[0]) < 2: raise ValueError, "domain specification needs at least two numbers"
            self._domain = [np.min(args[0]),np.max(args[0])]
        else:   # given explicit values for piecewise domain
            if len(args) != len(set(args)):
                raise ValueError, "domain values must be unique"
            if list(args) != sorted(list(args)) and list(args)[::-1] != sorted(list(args)):     # FIGURE THIS OUT
                raise ValueError, "domain values must be sorted"
            self._domain = args
        
        self._domain = map(float,self._domain)
        map(self._transform,self._domain)   # test that transform is defined on domain
        
        return self
    
    def range(self,*args):
        if len(args) == 0:
            return self._range
        elif is_iterable(args[0]):  # given array of data from which to determine range
            if len(args[0]) != len(self._domain): raise ValueError, "range specification needs at least two numbers"
            self._range = [np.min(args[0]),np.max(args[0])]
        else:   # given explicit values for piecewise range
            if len(args) != len(set(args)):
                raise ValueError, "range values must be unique"
            if list(args) != sorted(list(args)) and list(args)[::-1] != sorted(list(args)):     # FIGURE THIS OUT
                raise ValueError, "range values must be sorted"
            self._range = args
        
        if len(args) != len(self._domain):
            raise ValueError, "range specification must have same number of points as domain"
        
        return self
    
    def invert(self,y):
        if not self._in_range(x):
            raise ValueError, "outside range"
        segment = bisect.bisect_right(self._range,y) - 1
        if segment == len(self._range): segment -= 1   # deal with extra endpoint (fully closed interval), e.g., [0,1) [1,2) [2,3]
        return self._inverse((y - self._range[segment]) / (self._range[segment+1] - self._range[segment]) * (self._transform(self._domain[segment+1]) - self._transform(self._domain[segment])) + self._transform(self._domain[segment]))

linear = quantitative

class log(quantitative):
    """Implementation of log scale"""
    
    def __init__(self, *args):
        self._domain = [1,10]
        quantitative.__init__(self,*args)
        self.base(10)
    
    def base(self,*args):
        if len(args) == 0:
            return self._base
        else:
            self._base = args[0]
            self._logbase = math.log(self._base)
            self._transform = lambda x: math.log(x) / self._logbase
            self._inverse = lambda y: self._base ** y
            return self

class root(quantitative):
    """root scale"""
    
    def __init__(self, *args):
        quantitative.__init__(self,*args)
        self.power(2)
    
    def power(self,*args):
        if len(args) == 0:
            return self._power
        else:
            self._power = args[0]
            self._transform = lambda x: x**(1./self._power)
            self._inverse = lambda y: y**self._power
            return self



# class ordinal(object):
#     """Implementation for ordinal scale"""
#     
#     def __init__(self, *args):
#         Scale.__init__(self)
#         self._domain = []
#         self._indices = {}
#         self._range = []
#         self._band = 0
#         self.domain(*args)
#         return self
#     
#     def scale(self,x):
#         if x not in self._indices:
#             self._domain.append(x)
#             self._indices[x] = len(self._domain) - 1
#         return self._range[ self._indices[x] % len(self._range) ]
#     
#     def domain(self,*args):
#         if len(args) == 0:
#             return self._domain
#         
#         try:
#             iter(args[0])   # test for array type
#             array = args[0]
#             if len(args) > 1:
#                 array = map(args[1],array)
#         except TypeError:
#             array = args
#         
#         self._domain = list(set(array))
#         self._indices = pv.numerate(self._domain)
#         
#         return self
#     
#     def range(self,*args):
#         if len(args) == 0:
#             return self._range
#         
#         try:
#             iter(args[0])   # test for array type
#             array = args[0]
#             if len(args) > 1:
#                 array = map(args[1],array)
#         except TypeError:
#             array = args
#         
#         if isinstance(array[0],types.StringType):
#             array = map(pv.color,array)
#         
#         self._range = array
#         
#         return self
#     
#     def split(self,_min,_max):
#         step = float(_max - _min) / length(self.domain())
#         self._range = range(_min + step / 2., _max, step)
#         return self
#     
#     def splitFlush(self,_min,_max):
#         n = len(self.domain())
#         step = float(_max - _min) / (n - 1)
#         if n == 1:
#             self._range = (_min + _max) / 2.
#         else:
#             self._range = range(_min, _max + step / 2., step)
#         return self
#     
#     def splitBanded(self,_min,_max,band=1):
#         if band < 0:
#             n = len(self.domain())
#             total = -band * n
#             remaining = _max - _min - total
#             padding = remaining / float(n + 1)
#             self._range = range(_min + padding, _max, padding - band)
#             self._band = -band
#         else:
#             step = float(_max - _min) / (len(self.domain()) + (1 - band))
#             self._range = range(_min + step * (1 - band), _max, step)
#             self._band = step * band
#         return self
#     
#     def by(self,f):
#         raise NotImplementedError
# 
# class quantile(Scale):
#     """quantile scale"""
#     
#     def __init__(self, *args):
#         Scale.__init__(self)
#         self._num_quantiles = -1
#         self._max_quantile_index = -1
#         self._quantile_boundaries = []
#         self._domain = []
#         self._y = linear()  # the range
#         self.domain(*args)
#         return self
#     
#     def scale(self,x):
#         return self._y(max(0, min(self._max_quantile_index, bisect.bisect_right(self._quantile_boundaries, x) - 1)) / float(self._max_quantile_index))
#     
#     def quantiles(self,*args):
#         if len(args) == 0:
#             return self._quantile_boundaries
#         
#         self._num_quantiles = int(args[0])
#         
#         if self._num_quantiles < 0:
#             self._quantile_boundaries = [self._domain[0]] + self._domain
#             self._max_quantile_index = len(self._domain) - 1
#         else:
#             self._quantile_boundaries = [self._domain[0]]
#             for i in range(1,self._num_quantiles+1):
#                 self._quantile_boundaries.append( self._domain[ int(float(i) * (len(self._domain) - 1) / self._num_quantiles) ] )
#             self._max_quantile_index = self._num_quantiles - 1
#         
#         return self
#     
#     def domain(self,*args):
#         if len(args) == 0:
#             return self._domain
#         
#         try:
#             iter(args[0])
#             array = args[0]
#             if len(args) > 1:
#                 array = map(args[1],array)
#         except TypeError:
#             array = args
#         
#         self._domain = array
#         self._domain.sort()
#         self.quantiles(self._num_quantiles)
#         return self
#     
#     def range(self,*args):
#         if len(args) == 0:
#             return self._y.range()
#         
#         self._y.range(*args)
#         return self
#     
#     def by(self,f):
#         raise NotImplementedError
# 

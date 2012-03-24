import random

import numpy as np
import scipy as sp
import scipy.stats
import scipy.spatial

random.seed()
# random.seed(1)

np.random.seed()
# np.random.seed(1)

permutation = np.random.permutation
randint     = np.random.randint

def random_read(seq,read_len):
    position = randint(0,len(seq)-read_len+1)
    return (position,seq[position:position+read_len])

def sample_with_replacement(population,len,choose=random.choice):
    """Sample from a population with replacement
    
    Taken from Python Cookbook, 2nd ed, recipe 18.3
    """
    s = []
    for i in xrange(len):
        s.append(choose(population))
    return s

def multinomial_sample(n,p):
    """Return sample variates from multinomial
    
    NOTE: the numpy/scipy multinomial function will return a vector same
    length as p with the number of observations of each type. This function
    will return a vector of length n that has the actual observations.
    
    n - number of experiments
    p - vector or parameters; must sum to 1
    """
    if sum(p) != 1.: raise ValueError, "p must sum to 1"
    uniform_sample = np.random.uniform(size=n)
    p_cum = np.cumsum(p)
    return np.searchsorted(p_cum,uniform_sample,side='right')

def permsamp(x, nperm, theta):
    '''sample nperm times from the permutation distribution of the data x (numpy)
       theta is the function that takes the data and computes the statistic
       it must know how the data is "encoded" in x
       
       returns a vector of nperm th_star values
    '''
    N = len(x)
    
    def perm_iter():
        for i in xrange(nperm):
            yield x[permutation(N)]
    
    th_star = np.asarray( map(theta,perm_iter()) )
    
    return th_star

def bootstrap(x, nboot, theta):
    '''return n bootstrap replications of theta from x'''
    
    N = len(x)
    
    def rand_iter():
        for i in xrange(nboot):
            yield x[randint(0,N,N)]
    
    th_star = np.asarray( map(theta,rand_iter()) )
    
    return th_star

def sample2counts(sample, categories=0):
    """Return count vector from list of samples.
    
    Take vector of samples and return a vector of counts.  The elts
       refer to indices in something that would ultimately map to the
       originating category (like from a multinomial).  Therefore, if there
       are, say, 8 categories, then valid values in sample should be 0-7.
       If categories is not given, then i compute it from the highest value
       present in sample (+1).
    
    """
    counts = np.bincount(sample)
    if (categories > 0) and (categories > len(counts)):
        counts = np.append( counts, np.zeros(categories-len(counts)) )
    return counts

def counts2sample(counts):
    """Computes a consistent sample from a vector of counts.
    
    Takes a vector of counts and returns a vector of indices x
       such that len(x) = sum(c) and each elt of x is the index of
       a corresponding elt in c
    
    """
    x = np.ones(np.sum(counts),dtype=np.int_)
    
    start_idx = 0
    end_idx = 0
    for i in xrange(len(counts)):
        start_idx = end_idx
        end_idx = end_idx + counts[i]
        x[start_idx:end_idx] = x[start_idx:end_idx] * i 
    return x

def density2d(x,y):
    x = np.asarray(x).ravel()
    y = np.asarray(y).ravel()
    data = np.r_['0,2',x,y]
    kde = sp.stats.kde.gaussian_kde(data)
    return kde(data)

def entropy_bootstrap(pk,size,N=1000):
    """Compute bootstrapped entropy values.

    pk is a multinomial vector (will be normalized)
    size is the number of objects to draw from a multinomial at each iter
    N is number of bootstrap replicates
    """
    pk = np.asarray(pk,dtype=np.float)
    pk = pk / np.sum(pk)
    
    entropies = []
    for i in xrange(N):
        entropies.append( sp.stats.entropy(np.random.multinomial(size,pk)) )
    
    return entropies

def entropy_bootstrap2(pk,N=1000,total=0):
    """Compute bootstrapped entropy values.
    
    pk is a count vector
    sum is the total number of objects to draw from
    N is number of bootstrap replicates
    """
    n = sum(pk)
    if total == 0:
        total = n
    
    pk = list(pk)
    pk.append(total-n)
    pk = np.asarray(pk,dtype=np.float)
    pk = pk / np.sum(pk)
    
    entropies = []
    for i in xrange(N):
        entropies.append( sp.stats.entropy(np.random.multinomial(n,pk)[:-1]) )
    
    return entropies

def silhouette(Y,T):
    """Emulate MATLAB silhouette fn for cluster quality.
    
    Y -- condensed-form pairwise distance matrix
    T -- cluster assignments
    
    Based on StackOverflow #6644445
    """
    n = len(T)          # number of objects
    clusters = set(T)   # the cluster labels
    
    X = sp.spatial.distance.squareform(Y)
    
    s = np.zeros(n)
    for i in xrange(n):
        incluster = T==T[i]
        incluster[i] = False
        if np.sum(incluster) == 0:
            continue
        
        outcluster = lambda j: T==j
        
        # incluster average dist
        a = np.mean( X[incluster,i] )
        
        # min outcluster avg dist
        b = np.min([np.mean( X[outcluster(j),i] ) for j in (clusters-set([T[i]]))])
        
        s[i] = (b - a) / np.max([a,b])
    
    return s

import random

import numpy as np

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

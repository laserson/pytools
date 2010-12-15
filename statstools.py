import random

import numpy as np

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
    
    n - number of experiments
    p - vector or parameters; must sum to 1
    """
    if sum(p) != 1.: raise ValueError, "p must sum to 1"
    uniform_sample = np.random.uniform(size=n)
    p_cum = np.cumsum(p)
    return np.searchsorted(p_cum,uniform_sample,side='right')
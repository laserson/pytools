import random

import numpy as np

randint = np.random.randint

def choose(l):
    return l[randint(len(l))]

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

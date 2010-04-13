# bootstrap.py

import numpy

# INITIALIZATIONS

numpy.random.seed()
# numpy.random.seed(1)

permutation = numpy.random.permutation
randint     = numpy.random.randint

def permsamp(x, nperm, theta, *args):
    '''sample nperm times from the permutation distribution of the data x (numpy)
       theta is the function that takes the data and computes the statistic
       it must know how the data is "encoded" in x
       
       returns a vector of nperm th_star values
    '''
    N = len(x)
    th_star = numpy.zeros(nperm)
    
    for i in xrange(nperm):
        th_star[i] = theta( x[ permutation(N) ], *args )
    
    return th_star

def bootstrap(x, nboot, theta, *args):
    '''return n bootstrap replications of theta from x'''
    
    N = len(x)
    th_star = numpy.zeros(nboot)
    
    for i in xrange(nboot):
        th_star[i] = theta( x[ randint(0,N,N) ], *args )    # bootstrap repl from x
    
    return th_star

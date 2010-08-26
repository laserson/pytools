# 
#  bootstrap.py
#  pytools element
#  
#  Created by Uri Laserson on 2008-12-11.
#  Copyright 2010 Uri Laserson. All rights reserved.
# 

import numpy as np

np.random.seed()
# numpy.random.seed(1)

permutation = np.random.permutation
randint     = np.random.randint

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
    
    # th_star = numpy.zeros(nperm)
    # for i in xrange(nperm):
    #     th_star[i] = theta( x[ permutation(N) ], *args )
    
    return th_star

def bootstrap(x, nboot, theta):
    '''return n bootstrap replications of theta from x'''
    
    N = len(x)
    th_star = np.asarray( map(theta,x[randint(0,N,N)]) )
    
    # th_star = numpy.zeros(nboot)
    # for i in xrange(nboot):
    #     th_star[i] = theta( x[ randint(0,N,N) ], *args )    # bootstrap repl from x
    
    return th_star

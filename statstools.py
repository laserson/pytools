import numpy as np

randint = np.random.randint

def choose(l):
    return l[randint(len(l))]

def random_read(seq,read_len):
    position = randint(0,len(seq)-read_len+1)
    return (position,seq[position:position+read_len])
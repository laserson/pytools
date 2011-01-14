# Based on http://code.activestate.com/recipes/576633/
# which is based on:
# Reference: 'Stacked graphs- geometry & aesthetics' by Byron and Wattenberg
# http://www.leebyron.com/else/streamgraph/download.php?file=stackedgraphs_byron_wattenberg.pdf

import numpy as np
import matplotlib as mpl
# mpl.use('Agg')
import matplotlib.pyplot as plt

# baseline functions
def symmetric(streams):
    """Symmetric baseline ('silhouette')"""
    g0 = -0.5 * np.sum(np.asarray(streams),axis=0)
    return g0

def zero(streams):
    """Zero baseline"""
    return np.zeros(np.asarray(streams).shape[1])

def weighted_wiggle(streams):
    """Weighted-wiggle minimization
    
    NOTE: streams should already be ordered as desired
    """
    streams = np.asarray(streams)
    
    # add a column of zeros on the left side of streams
    f = np.hstack( (np.zeros((streams.shape[0],1)),streams) )
    df = np.diff(f)
    cum_sum_df = np.vstack( (np.zeros((1,df.shape[1])),np.cumsum(df,axis=0)) )[:-1,:]
    dg0 = (-1./np.sum(streams,axis=0)) * np.sum((0.5 * df + cum_sum_df) * streams,axis=0)
    g0 = np.cumsum(dg0)
    return g0

# ordering functions
def onset(streams):
    """Returns permutation indices (like argsort) for onset ordering."""
    streams = np.asarray(streams)
    nonzero_idxs = [np.arange(streams.shape[1])[idxs] for idxs in (streams > 0)]
    onset_idxs = [np.min(nzi) if len(nzi) > 0 else streams.shape[1] for nzi in nonzero_idxs]
    return np.argsort(onset_idxs)

def inside_out(streams):
    """Returns permutation indices (like argsort) for inside-out ordering."""
    upper = []
    lower = []
    weight_up = 0
    weight_lo = 0
    for (i,stream) in enumerate(streams):
        if weight_up >= weight_lo:
            upper.append(i)
            weight_up += np.sum(stream)
        else:
            lower.append(i)
            weight_lo += np.sum(stream)
    
    return upper + lower

def streamgraph(ax,streams, x=None, colors=None, baseline=weighted_wiggle):
    streams = np.asarray(streams)
    
    g0 = baseline(streams)
    
    if x == None:
        x = range(streams.shape[1])
    
    if colors == None:
        colors = map(mpl.cm.bone,np.random.uniform(size=streams.shape[0]))
    
    layers = []
    g_lo = g0
    for stream in streams:
        g_hi = g_lo + stream
        verts_lo = zip(x,g_lo)
        verts_hi = zip(x[::-1],g_hi[::-1])
        layer = verts_lo + verts_hi
        layers.append(layer)
        g_lo = g_hi
    
    polys = mpl.collections.PolyCollection(layers,facecolors=colors,linewidths=0)
    ax.add_collection(polys)
    
    return ax
    
        
# Demo
if __name__ == '__main__':
    np.random.seed(1)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    N_dsets = 50
    T = 100
    amp = 1
    fade = .15
    dsets = []
    for i in xrange(N_dsets):
        this_dset = np.zeros(T)
        t_onset = np.random.randint(.9*T)-T/3
        if t_onset >= 0:   
            remaining_t = np.arange(T-t_onset)     
        else:
            remaining_t = np.arange(T)-t_onset
        this_dset[max(t_onset,0):]=np.exp(-.15*np.random.gamma(10,.1)*remaining_t)\
                            * remaining_t * np.random.gamma(6,.2)# * np.cos(-fade*remaining_t*np.random.gamma(10,.1))**2
        dsets.append(this_dset)
    import pdb
    pdb.set_trace()
    streamgraph(ax,dsets,baseline=symmetric)
    ax.autoscale_view()
    plt.draw()
## end of http://code.activestate.com/recipes/576633/ }}}

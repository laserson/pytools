import random

import numpy as np
import scipy as sp
import scipy.stats

import matplotlib as mpl
import matplotlib.pyplot as plt

def jitter(data, bins=100):
    data = np.asarray(data)
    (hist,edges) = np.histogram(data,bins=bins)
    hist = np.float_(hist) / max(hist)
    idxs = np.searchsorted(edges[:-2],data)
    return hist[idxs]

def jitter_x(x,y,width=None,bins=100):
    x = np.asarray(x)
    y = np.asarray(y)
    
    x_argsort = np.argsort(x)
    x_uniq = sorted(list(set(x)))
    
    # find smallest interval between any two x-values
    if width == None:
        if len(x_uniq) == 1:
            width = 1.
        else:
            interval = min([x[x_argsort[i+1]]-x[x_argsort[i]] for i in xrange(len(x)-1)])
            width = interval / 3.
    
    x_jit = []
    y_jit = []
    for val in x_uniq:
        idx = (x==val)
        scaling_factors = jitter(y[idx],bins=bins)
        for (x_val,y_val,scaling) in zip(x[idx],y[idx],scaling_factors):
            x_jit.append( x_val + width * scaling * random.choice([-1,1]) * np.random.uniform(0,1))
            y_jit.append( y_val )
    
    return (x_jit,y_jit)


# def jitter_x(x,y,width=None):
#     x = np.asarray(x)
#     y = np.asarray(y)
#     
#     x_argsort = np.argsort(x)
#     x_uniq = sorted(list(set(x)))
#     
#     # find smallest interval between any two x-values
#     if width == None:
#         interval = min([x[x_argsort[i+1]]-x[x_argsort[i]] for i in xrange(len(x)-1)])
#         width = interval / 3.
#     
#     x_jit = []
#     y_jit = []
#     for val in x_uniq:
#         idx = (x==val)
#         kernel = sp.stats.kde.gaussian_kde(y[idx])
#         kernel_max = max([kernel(v) for v in set(y[idx])])
#         for (x_val,y_val) in zip(x[idx],y[idx]):
#             x_jit.append( x_val + np.random.uniform(-1,1) * width * kernel(y_val) / kernel_max)
#             y_jit.append( y_val )
#     
#     return (x_jit,y_jit)


class ConstWidthRectangle(mpl.patches.Patch):
    
    def __init__(self, x, y1, y2, w, **kwargs):
        self.x  = x
        self.y1 = y1
        self.y2 = y2
        self.w  = w
        mpl.patches.Patch.__init__(self,**kwargs)
    
    def get_path(self):
        return mpl.path.Path.unit_rectangle()
    
    def get_transform(self):
        box = np.array([[self.x,self.y1],
                        [self.x,self.y2]])
        box = self.axes.transData.transform(box)
        
        w = self.w * self.axes.bbox.width / 2.0
        
        box[0,0] -= w
        box[1,0] += w
        
        return mpl.transforms.BboxTransformTo(mpl.transforms.Bbox(box))

class ConstWidthLine(mpl.lines.Line2D):
    
    def __init__(self,x,y,w,**kwargs):
        self.x = x
        self.y = y
        self.w = w
        mpl.lines.Line2D.__init__(self,[0,1],[0,0],**kwargs) # init to unit line
    
    def get_transform(self):
        # define transform that takes unit horiz line seg
        # and places it in correct position using display
        # coords
        
        box = np.array([[self.x,self.y],
                        [self.x,self.y+1]])
        box = self.axes.transData.transform(box)
        
        w = self.w * self.axes.bbox.width / 2.0
        
        box[0,0] -= w
        box[1,0] += w
        
        #xdisp,ydisp = self.axes.transData.transform_point([self.x,self.y])
        #xdisp -= w
        #xleft  = xdisp - w
        #xright = xdisp + w
        
        return mpl.transforms.BboxTransformTo(mpl.transforms.Bbox(box))
        #return mpl.transforms.Affine2D().scale(w,1).translate(xdisp,ydisp)
    
    def draw(self,renderer):
        # the ONLY purpose of redefining this function is to force the Line2D
        # object to execute recache().  Otherwise, certain changes in the scale
        # do not invalidate the Line2D object, and the transform will not be
        # recomputed (and so the Axes coords computed earlier will be obsolete)
        self.recache()
        return mpl.lines.Line2D.draw(self,renderer)


class ConstHeightRectangle(mpl.patches.Patch):
    
    def __init__(self, x1, x2, y, h, **kwargs):
        self.x1 = x1
        self.x2 = x2
        self.y  = y
        self.h  = h
        mpl.patches.Patch.__init__(self,**kwargs)
    
    def get_path(self):
        return mpl.path.Path.unit_rectangle()
    
    def get_transform(self):
        box = np.array([[self.x1,self.y],
                        [self.x2,self.y]])
        box = self.axes.transData.transform(box)
        
        h = self.h * self.axes.bbox.height / 2.0
        
        box[0,1] -= h
        box[1,1] += h
        
        return mpl.transforms.BboxTransformTo(mpl.transforms.Bbox(box))

class ConstHeightLine(mpl.lines.Line2D):
    
    def __init__(self,x,y,h,**kwargs):
        self.x = x
        self.y = y
        self.h = h
        mpl.lines.Line2D.__init__(self,[0,0],[0,1],**kwargs) # init to unit line
        
        # self.x = x
        # self.y = y
        # self.w = w
        # mpl.lines.Line2D.__init__(self,[0,1],[0,0],**kwargs) # init to unit line
    
    def get_transform(self):
        # define transform that takes unit horiz line seg
        # and places it in correct position using display
        # coords
        
        box = np.array([[self.x,self.y],
                        [self.x+1,self.y]])
        box = self.axes.transData.transform(box)
        
        h = self.h * self.axes.bbox.height / 2.0
        
        box[0,1] -= h
        box[1,1] += h
        
        #xdisp,ydisp = self.axes.transData.transform_point([self.x,self.y])
        #xdisp -= w
        #xleft  = xdisp - w
        #xright = xdisp + w
        
        return mpl.transforms.BboxTransformTo(mpl.transforms.Bbox(box))
        #return mpl.transforms.Affine2D().scale(w,1).translate(xdisp,ydisp)
    
    def draw(self,renderer):
        # the ONLY purpose of redefining this function is to force the Line2D
        # object to execute recache().  Otherwise, certain changes in the scale
        # do not invalidate the Line2D object, and the transform will not be
        # recomputed (and so the Axes coords computed earlier will be obsolete)
        self.recache()
        return mpl.lines.Line2D.draw(self,renderer)


def boxplot(ax, x, positions=None, widths=None, vert=1):
    # adapted from matplotlib
    
    # convert x to a list of vectors
    if hasattr(x, 'shape'):
        if len(x.shape) == 1:
            if hasattr(x[0], 'shape'):
                x = list(x)
            else:
                x = [x,]
        elif len(x.shape) == 2:
            nr, nc = x.shape
            if nr == 1:
                x = [x]
            elif nc == 1:
                x = [x.ravel()]
            else:
                x = [x[:,i] for i in xrange(nc)]
        else:
            raise ValueError, "input x can have no more than 2 dimensions"
    if not hasattr(x[0], '__len__'):
        x = [x]
    col = len(x)
    
    # get some plot info
    if positions is None:
        positions = range(1, col + 1)
    if widths is None:
        widths = min(0.3/len(positions),0.05)
    if isinstance(widths, float) or isinstance(widths, int):
        widths = np.ones((col,), float) * widths
    
    # loop through columns, adding each to plot
    for i,pos in enumerate(positions):
        d = np.ravel(x[i])
        row = len(d)
        if row==0:
            # no data, skip this position
            continue
        # get distrib info
        q1, med, q3 = mpl.mlab.prctile(d,[25,50,75])
        dmax = np.max(d)
        dmin = np.min(d)
        
        line_color = '#074687'
        face_color = '#96B7EC'
        if vert == 1:
            medline = ConstWidthLine(pos,med,widths[i],color=line_color,zorder=3)
            box = ConstWidthRectangle(pos,q1,q3,widths[i],facecolor=face_color,edgecolor=line_color,zorder=2)
            vertline = mpl.lines.Line2D([pos,pos],[dmin,dmax],color=line_color,zorder=1)
        else:
            medline = ConstHeightLine(med,pos,widths[i],color=line_color,zorder=3)
            box = ConstHeightRectangle(q1,q3,pos,widths[i],facecolor=face_color,edgecolor=line_color,zorder=2)
            vertline = mpl.lines.Line2D([dmin,dmax],[pos,pos],color=line_color,zorder=1)
        
        ax.add_line(vertline)
        ax.add_patch(box)
        ax.add_line(medline)


# define colormap for -1 to 1 (green-black-red) like gene expression
_redgreencdict = {'red': [(0.0,   0.0,   0.0),
                         (0.5,   0.0,   0.0),
                         (1.0,   1.0,   0.0)],
                        
                'green':[(0.0,   0.0,   1.0),
                         (0.5,   0.0,   0.0),
                         (1.0,   0.0,   0.0)],
                        
                'blue': [(0.0,   0.0,   0.0),
                         (0.5,   0.0,   0.0),
                         (1.0,   0.0,   0.0)]}

redgreen = mpl.colors.LinearSegmentedColormap('redgreen',_redgreencdict,256)
redgreen.set_bad(color='w')


def compute_log_view_lim(data):
    lo_lim = 10**np.floor(np.log10(np.min(data)))
    hi_lim = 10**np.ceil(np.log10(np.max(data)))
    return (lo_lim, hi_lim)

def generate_counthist(counts, label, view_lim=[1e-6,1e0,1e0,1e5]):
    """Generate count size histogram.
    
    counts -- dictionary of (key,count) pairs
    label  -- for the legend
    """
    max_size = max(counts.values())
    num_chains = sum(counts.values())
    sizes = np.arange(1,max_size+1)
    freqs = np.float_(sizes) / num_chains
    (hist,garbage) = np.histogram(counts.values(),bins=sizes)
    idxs = hist > 0
    
    fig = plt.figure()
    
    ax = fig.add_subplot(111)
    ax2 = ax.twiny()
        
    ax.spines['top'].set_position(('outward',5))
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_position(('outward',5))
    ax.spines['left'].set_position(('outward',5))
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.plot(freqs[idxs],hist[idxs],marker='o',linestyle='None',color='#e31a1c',markeredgewidth=0,markersize=4,clip_on=False,label=label)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(view_lim[:2])
    ax.set_ylim(view_lim[2:])
    
    ax2.spines['top'].set_position(('outward',5))
    ax2.spines['right'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.xaxis.set_ticks_position('top')
    ax2.yaxis.set_ticks_position('none')
    ax2.set_xscale('log')
    ax2.set_xlim([view_lim[0]*num_chains,view_lim[1]*num_chains])
    
    ax.set_xlabel('junction frequency (bottom) or count (top)')
    ax.set_ylabel('number of junctions')
    
    leg = ax.legend(loc=0,numpoints=1,prop=mpl.font_manager.FontProperties(size='small'))
    leg.get_frame().set_visible(False)
    
    return fig

def generate_counthistline(counts, label, view_lim=[1e-6,1e0,1e0,1e5]):
    """Generate count size histogram.
    
    counts -- dictionary of (key,count) pairs
    label  -- for the legend
    """
    max_size = max(counts.values())
    num_chains = sum(counts.values())
    bins = np.logspace(0,np.log10(max_size),21)
    bins_freqs = np.float_(bins) / num_chains
    (hist,garbage) = np.histogram(counts.values(),bins=bins)
        
    fig = plt.figure()
    
    ax = fig.add_subplot(111)
    ax2 = ax.twiny()
        
    ax.spines['top'].set_position(('outward',5))
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_position(('outward',5))
    ax.spines['left'].set_position(('outward',5))
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.plot(bins_freqs,list(hist)+[hist[-1]],color='#e31a1c',drawstyle='steps-post',clip_on=False,label=label)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(view_lim[:2])
    ax.set_ylim(view_lim[2:])
    
    ax2.spines['top'].set_position(('outward',5))
    ax2.spines['right'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.xaxis.set_ticks_position('top')
    ax2.yaxis.set_ticks_position('none')
    ax2.set_xscale('log')
    ax2.set_xlim([view_lim[0]*num_chains,view_lim[1]*num_chains])
    
    ax.set_xlabel('junction frequency (bottom) or count (top)')
    ax.set_ylabel('number of junctions')
    
    leg = ax.legend(loc=0,numpoints=1,prop=mpl.font_manager.FontProperties(size='small'))
    leg.get_frame().set_visible(False)
    
    return fig

def generate_rankaccum(counts,label,view_lim=[1e0,1e5,1e-6,1e0]):
    """Generate rankaccum curve.
    
    counts -- dictionary of (key,count) pairs
    label  -- for the legend
    """
    num_chains = sum(counts.values())
    freqs = np.float_(counts.values()) / num_chains
    
    fig = plt.figure()
    
    ax = fig.add_subplot(111)
    ax2 = ax.twinx()
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_position(('outward',5))
    ax.spines['bottom'].set_position(('outward',5))
    ax.spines['left'].set_position(('outward',5))
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.plot(range(1,len(counts.values())+1),sorted(freqs,reverse=True),marker='o',linestyle='None',color='#377db8',markeredgewidth=0,markersize=4,clip_on=False,label=label)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(view_lim[:2])
    ax.set_ylim(view_lim[2:])
    
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_position(('outward',5))
    ax2.spines['bottom'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.xaxis.set_ticks_position('none')
    ax2.yaxis.set_ticks_position('right')
    ax2.set_yscale('log')
    ax2.set_ylim([view_lim[2]*num_chains,view_lim[3]*num_chains])
    
    ax.set_xlabel('rank')
    ax.set_ylabel('junction frequency (left) or count (right)')
    
    leg = ax.legend(loc=0,numpoints=1,prop=mpl.font_manager.FontProperties(size='small'))
    leg.get_frame().set_visible(False)
    
    return fig


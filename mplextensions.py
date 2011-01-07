import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt

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

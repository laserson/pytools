import numpy as np

def load_timeseries(inhandle):
    """Load timeseries data from file.
    
    There may be 'control' lines that start with #, e.g.:
        #times
        #sums
    that are loaded into the returned data dictionary as:
        data['times'] = ...
    
    The control lines must contain a whitespace delimited list of numbers
    (float allowed)
    
    data['labels'] will contain all the labels (first entry of each timeseries
    row) in order
    
    data['matrix'] will contain the numpy array that has the actual data in it
    """
    data = {}
    labels = []
    matrix = []
    for line in inhandle:
        if line.startswith('#'):
            tokens = line.split()
            label = tokens[0].lstrip('#')
            values = np.asarray(map(float,tokens[1:]))
            data[label] = values
        else:
            values = line.split()
            labels.append(values[0].strip())
            matrix.append(map(int,values[1:]))
    data['labels'] = labels
    data['matrix'] = np.asarray(matrix)
    
    return data

def write_timeseries(outhandle,**kw):
    """Write timeseries to file.
    
    Must provide labels and matrix. All other arguments must be lists of
    numbers (floats allowed) which get printed as "comments". They will be
    loaded by the load function as well.
    
    matrix must always be integer type. (If normalization is required, pass
    the proper column sums in as control line #sums).
    """
    labels = kw.pop('labels')
    matrix = kw.pop('matrix')
    for (key,values) in kw.iteritems():
        print >>outhandle, '#%s ' % key + ' '.join(map(str,values))
    for (label,timeseries) in zip(labels,matrix):
        print >>outhandle, ' '.join(map(str,[label]+list(timeseries)))

def normalized_timeseries(timeseries):
    return np.float_(timeseries) / timeseries.sum(axis=0)

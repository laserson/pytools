import numpy as np

def load_timeseries(inhandle):
    # read in times
    for line in inhandle:
        if line.startswith('#times'):
            times = np.asarray(map(float,line.split()[1:]))
            break

    # read in data
    labels = []
    timeseriesmatrix = []
    for line in inhandle:
        data = line.split()
        labels.append(data[0].strip())
        timeseriesmatrix.append(map(int,data[1:]))
    timeseriesmatrix = np.asarray(timeseriesmatrix)
    
    return (labels,times,timeseriesmatrix)

def write_timeseries(outhandle,labels,times,timeseriesmatrix):
    print >>outhandle, '#times ' + ' '.join(map(str,times))
    for (label,timeseries) in zip(labels,timeseriesmatrix):
        print >>outhandle, ' '.join(map(str,[label]+list(timeseries)))

def normalized_timeseries(timeseries):
    return np.float_(timeseries) / timeseries.sum(axis=0)

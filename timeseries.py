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

import numpy as np

def exponential_moving_average(raw, alpha):
    # Equation: y[n] = alpha * x[n] + (1 - alpha) * y[n-1]

    raw = np.array(raw)
    smoothed = np.zeros_like(raw)

    smoothed[0] = raw[0]    #set start pos as first pos in raw

    for i in range(1, len(raw)):
        smoothed[i] = alpha * raw[i]  + (1 - alpha) * smoothed[i - 1]

    return smoothed


def moving_average(raw, window):
    raw = np.array(raw)
    
    n_samples = len(raw)
    smoothed = np.zeros_like(raw)

    for i in range(n_samples):

        #start from 0 if i < window size
        start_idx = max(0, i - window + 1)

        window_data = raw[start_idx : i + 1]
        smoothed[i] = np.mean(window_data, axis=0)

    return smoothed




        
                   
    

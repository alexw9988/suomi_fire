
import math

import matplotlib.pyplot as plt
import numpy as np


def maskQualityFlags(data, quality_flags):
    output = np.ma.masked_where(quality_flags > 0, data)
    return output

def maskWater(data, water_mask):
    output = np.ma.masked_where(water_mask != 1, data)
    return output

def plot(data, stepnames, idxs, extent):
    count = len(idxs)
    grid_x = math.ceil(count**0.5)
    grid_y = math.floor(count**0.5)
    if grid_x*grid_y < count: grid_y += 1 

    _, ax = plt.subplots(grid_y, grid_x)
    ax = ax.flatten()
    
    for i, idx in enumerate(idxs):
        ax[i].matshow(data[idx], extent=extent, cmap='hot')
        ax[i].set_title(stepnames[idx])
        
    plt.show()




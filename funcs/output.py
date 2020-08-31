
import math

import matplotlib.pyplot as plt
import numpy as np


def plot(data, step_names, plot_flags, extent):
    count = sum(plot_flags)
    grid_x = math.ceil(count**0.5)
    grid_y = math.floor(count**0.5)
    if grid_x*grid_y < count: grid_y += 1 

    _, ax = plt.subplots(grid_y, grid_x)
    ax = np.array(ax).flatten()
    
    pos = 0
    for idx, plot_flag in enumerate(plot_flags):
        if plot_flag: 
            ax[pos].matshow(data[idx], extent=extent, cmap='hot')
            ax[pos].set_title(step_names[idx])
            pos += 1
        
    plt.show()


from math import ceil, floor

import numpy as np
import scipy.ndimage as sn
import skimage.filters as sf


def getProcessFunc(name):
    if name == 'gaussian':
        return _gaussian
    elif name == 'threshold':
        return _threshold
    elif name == 'binary_closing':
        return _binaryClosing
    elif name == 'binary_opening':
        return _binaryOpening
    else: 
        print("Function not found!")
        return None

def _gaussian(data, params):
    sigma = params['sigma']

    output = sf.gaussian(data, sigma=sigma)
    return output

def _threshold(data, params):  
    thresh = params['thresh']

    output = np.array(np.where(data>thresh, 1, 0), dtype=np.bool)
    return output

def _binaryClosing(data, params):
    sz = params['structure_size']

    x,y = np.mgrid[-ceil(sz):ceil(sz)+1, -ceil(sz):ceil(sz)+1]
    structure = (x/sz)**2 + (y/sz)**2 < 1
    
    output = sn.binary_closing(data, structure=structure)
    return output

def _binaryOpening(data, params):
    sz = params['structure_size']

    x,y = np.mgrid[-ceil(sz):ceil(sz)+1, -ceil(sz):ceil(sz)+1]
    structure = (x/sz)**2 + (y/sz)**2 < 1
    
    output = sn.binary_opening(data, structure=structure)
    return output

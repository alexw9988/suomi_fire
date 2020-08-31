
import math

import geojson
import matplotlib.pyplot as plt
import numpy as np
import rasterio.features as rf
import shapely.geometry as sg


def plot(data, step_names, plot_flags, extent, array_reversed):
    count = sum(plot_flags)
    grid_x = math.ceil(count**0.5)
    grid_y = math.floor(count**0.5)
    if grid_x*grid_y < count: grid_y += 1 

    _, ax = plt.subplots(grid_y, grid_x)
    ax = np.array(ax).flatten()
    
    pos = 0
    for idx, plot_flag in enumerate(plot_flags):
        if plot_flag: 
            if array_reversed:
                ax[pos].matshow(np.flip(data[idx]), extent=extent)
            else:
                ax[pos].matshow(data[idx], extent=extent)
            ax[pos].set_title(step_names[idx])
            pos += 1
        
    plt.show()

def saveGeoJSON(data, lat, lon, output_fp):
    lat = lat.filled(np.nan)
    lon = lon.filled(np.nan)

    shapes = rf.shapes(np.array(data,dtype=np.uint8))

    features = []
    for shape in shapes:
        if shape[1] == 1:
            poly = geojson.Polygon(shape[0]['coordinates'])
            poly = geojson.utils.map_tuples(lambda c: _coordinateMapper(c, lat, lon), poly)
            feature = geojson.Feature(geometry=poly, properties={"fill": "#ff2600", "stroke": "#ff2600"})
            features.append(feature)
    
    collection = geojson.FeatureCollection(features)
    
    with open(output_fp, 'w') as fp: 
        geojson.dump(collection, fp)

def _coordinateMapper(c, lat, lon):
    x, y = c
    x = int(x)
    y = int(y)
    tup = (float(lon[y,x]), float(lat[y,x]))
    return tup

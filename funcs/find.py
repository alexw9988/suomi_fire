
import geojson
import scipy.ndimage as sn


def label(data):
    return sn.label(data)

def createGeoJSON(data, num_features, lat, lon):
    pass
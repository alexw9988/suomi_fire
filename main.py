
import argparse
import json
import os

import netCDF4 as nc
import numpy as np

import funcs


class Processor():

    def __init__(self, cfg_fp): 
        if os.path.splitext(cfg_fp)[-1].lower() != '.json':
            raise ValueError("Only .json files allowed!")
        with open(cfg_fp, 'r') as fp:
            self.config = json.load(fp)

    def __call__(self, obs_fp, geo_fp, output_fp):
        self.loadData(obs_fp, geo_fp) 
        self.prepareData()
        self.processData()
        self.findFeatures()
        self.outputResults(output_fp)

    def loadData(self, obs_fp, geo_fp):
        if os.path.splitext(obs_fp)[-1].lower() != '.nc' or \
           os.path.splitext(geo_fp)[-1].lower() != '.nc':
            raise ValueError("Only .nc files allowed!")
        
        self.obs_ds = obs_ds = nc.Dataset(obs_fp)
        self.geo_ds = geo_ds = nc.Dataset(geo_fp)

        band = self.config['band']
        self.data = [obs_ds['observation_data']['{}'.format(band)][:]]
        self.stepnames = ['raw_data']

        self.quality_flags = obs_ds['observation_data']['{}_quality_flags'.format(band)][:]
        self.water_mask = geo_ds['geolocation_data']['land_water_mask'][:]

        self.lat = geo_ds['geolocation_data']['latitude'][:]
        self.lon = geo_ds['geolocation_data']['longitude'][:]
        extent_lat = (np.amin(self.lat), np.amax(self.lat))
        extent_lon = (np.amin(self.lon), np.amax(self.lon))
        self.extent = (*extent_lon, *extent_lat)
        
    def prepareData(self):
        self.data.append(funcs.maskQualityFlags(self.data[-1], self.quality_flags))
        self.stepnames.append('quality_masked')

        self.data.append(funcs.maskWater(self.data[-1], self.water_mask))
        self.stepnames.append('water_masked')

    def processData(self):
        pass

    def findFeatures(self):
        pass 

    def outputResults(self, output_fp):
        plot_idxs = []
        for plot_step in self.config['plot_steps']:
            for idx, stepname in enumerate(self.stepnames):
                if stepname == plot_step:
                    plot_idxs.append(idx)
        funcs.plot(self.data, self.stepnames, plot_idxs, self.extent)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Rudimentary fire detection algorithm for the Suomi-NPP satellite")
    parser.add_argument('obs_fp', help="Filepath of observation .nc file")
    parser.add_argument('geo_fp', help="Filepath of georeference .nc file")
    parser.add_argument('-c', '--config', help="Filepath of config .json file", dest='cfg_fp', default='config.json')
    parser.add_argument('-o', '--output', help="Filepath of output file", dest='output_fp', default='output.json')

    args = parser.parse_args()
    obs_fp = args.obs_fp
    geo_fp = args.geo_fp
    cfg_fp = args.cfg_fp
    output_fp = args.output_fp

    processor = Processor(cfg_fp)(obs_fp, geo_fp, output_fp)

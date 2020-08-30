
import argparse
import json
import os

import netCDF4 as nc
import numpy as np


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

        self.data = obs_ds['observation_data']['M13'][:]
        self.quality_flags = obs_ds['observation_data']['M13_quality_flags'][:]
        self.lat = geo_ds['geolocation_data']['latitude'][:]
        self.lon = geo_ds['geolocation_data']['longitude'][:]

    def prepareData(self):
        pass

    def processData(self):
        pass

    def findFeatures(self):
        pass 

    def outputResults(self, output_fp):
        pass 


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

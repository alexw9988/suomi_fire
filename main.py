
import argparse
import json
import os

import netCDF4 as nc
import numpy as np

from funcs import output, prepare, process


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
        self.outputResults(output_fp)

    def loadData(self, obs_fp, geo_fp):
        if os.path.splitext(obs_fp)[-1].lower() != '.nc' or \
           os.path.splitext(geo_fp)[-1].lower() != '.nc':
            raise ValueError("Only .nc files allowed!")
        
        self.obs_ds = obs_ds = nc.Dataset(obs_fp)
        self.geo_ds = geo_ds = nc.Dataset(geo_fp)

        band = self.config['band']
        self.data = [obs_ds['observation_data']['{}'.format(band)][:]]
        self.step_names = ['raw_data']
        self.plot_flags = [True] if self.config['plot_raw_data'] else [False]

        self.quality_flags = obs_ds['observation_data']['{}_quality_flags'.format(band)][:]
        self.quality_flag_meanings = obs_ds['observation_data']['{}_quality_flags'.format(band)].getncattr('flag_meanings')
        self.quality_flag_masks = obs_ds['observation_data']['{}_quality_flags'.format(band)].getncattr('flag_masks')

        self.water_mask = geo_ds['geolocation_data']['land_water_mask'][:]

        self.lat = geo_ds['geolocation_data']['latitude'][:]
        self.lon = geo_ds['geolocation_data']['longitude'][:]
        extent_lat = (np.amin(self.lat), np.amax(self.lat))
        extent_lon = (np.amin(self.lon), np.amax(self.lon))
        self.extent = (*extent_lon, *extent_lat)
        
    def prepareData(self):
        self.data[-1] = self.data[-1].filled(np.nan)

        self.data.append(prepare.maskQualityFlags(self.data[-1], 
            self.quality_flags, self.quality_flag_meanings, 
            self.quality_flag_masks, self.config['mask_quality_flags']))
        self.step_names.append('quality_masked')
        self.plot_flags.append(self.config['plot_quality_masked'])

        self.data.append(prepare.maskWater(self.data[-1], self.water_mask))
        self.step_names.append('water_masked')
        self.plot_flags.append(self.config['plot_water_masked'])

    def processData(self):  
        for step in self.config['process_steps']:
            name = step['name']
            func = process.getProcessFunc(name)
            if func is None: 
                continue
                
            self.data.append(func(self.data[-1], step['params']))
            self.step_names.append(name)
            self.plot_flags.append(step['plot'])

    def outputResults(self, output_fp):
        output.saveGeoJSON(self.data[-1], self.lat, self.lon, output_fp)
        output.plot(self.data, self.step_names, self.plot_flags, self.extent)


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

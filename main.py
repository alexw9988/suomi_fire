
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
        
        #Load datasets 
        self.obs_ds = obs_ds = nc.Dataset(obs_fp)
        self.geo_ds = geo_ds = nc.Dataset(geo_fp)

        #Extract data
        band = self.config['band']
        self.data = [obs_ds['observation_data']['{}'.format(band)][:]]
        self.step_names = ['raw_data']
        self.plot_flags = [True] if self.config['plot_raw_data'] else [False]

        #Extract quality flags 
        self.quality_flags = obs_ds['observation_data']['{}_quality_flags'.format(band)][:]
        self.quality_flag_values = obs_ds['observation_data']['{}_quality_flags'.format(band)].getncattr('flag_masks')
        self.quality_flag_meanings = obs_ds['observation_data']['{}_quality_flags'.format(band)].getncattr('flag_meanings').split()
        
        #Extract water mask 
        self.land_water_flags = geo_ds['geolocation_data']['land_water_mask'][:]
        self.land_water_values = geo_ds['geolocation_data']['land_water_mask'].getncattr('flag_values')
        self.land_water_meanings = geo_ds['geolocation_data']['land_water_mask'].getncattr('flag_meanings').split()

        #Extract coordinates
        self.lat = geo_ds['geolocation_data']['latitude'][:]
        self.lon = geo_ds['geolocation_data']['longitude'][:]
        if self.lat[0,0] < self.lat[-1,0]: #Flip array when plotting
            self.array_reversed = True #Descending
        else:
            self.array_reversed = False #Ascending
        extent_lat = (np.amin(self.lat), np.amax(self.lat))
        extent_lon = (np.amin(self.lon), np.amax(self.lon))
        self.extent = (*extent_lon, *extent_lat)

    def prepareData(self):
        #Convert masked array to regular array (to avoid problems with filters)
        self.data[-1] = self.data[-1].filled(np.nan)

        #Apply quality flag masking
        self.data.append(prepare.maskFlags(self.data[-1], 
            self.quality_flags, self.quality_flag_meanings, 
            self.quality_flag_values, self.config['mask_quality_flags'],
            mode='binary_and'))
        self.step_names.append('quality_masked')
        self.plot_flags.append(self.config['plot_quality_masked'])

        #Apply water masking
        self.data.append(prepare.maskFlags(self.data[-1], 
            self.land_water_flags, self.land_water_meanings,
            self.land_water_values, self.config['mask_water_flags'],
            mode='equal'))
        self.step_names.append('water_masked')
        self.plot_flags.append(self.config['plot_water_masked'])

    def processData(self):
        #Process each filter step specified in the config 
        for step in self.config['process_steps']:
            name = step['name']
            func = process.getProcessFunc(name)
            if func is None: 
                continue
                
            self.data.append(func(self.data[-1], step['params']))
            self.step_names.append(name)
            self.plot_flags.append(step['plot'])

    def outputResults(self, output_fp):
        #Find features and export to GeoJSON file
        output.saveGeoJSON(self.data[-1], self.lat, self.lon, output_fp)
        
        #Show plots 
        output.plot(self.data, self.step_names, self.plot_flags, self.extent, self.array_reversed)


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

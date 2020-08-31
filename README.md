# suomi_fire
Rudimentary fire detection algorithm for the Suomi-NPP satellite

## Usage
Within the project folder run:
`python3 main.py OBS_FP GEO_FP`
* `OBS_FP`: Observation `.nc` file
* `GEO_FP`: Geolocation `.nc` file

Optional arguments: `-c CFG_FP -o OUTPUT_F`
* `CFG_FP`: Config `.json` file
* `OUTPUT_FP`: Output `.json` GEOJSON file

## Configuration
Use `config.json` to select the frequency band, which quality flags to mask out, which processing steps to use (and in what order) and which parameters to use with these filters. You can also choose which of the filter steps to plot by setting their plot flag. 

## Output
Besides the plotted images, a GeoJSON file will be exported to the desired output path `OUTPUT_FP` including all detected fire regions as Polygon Features. 

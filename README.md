# raster-js
Convert GIS Raster Datasets to a simple JavaScript object.

This is useful for using raster datasets in libraries such as Leaflet, OpenLayers and Google Maps for applications such as viewsheds, A* Routing algorithm and the calculation of multispectral indices (e.g. NDVI).

If the dataset CRS is defined by an EPSG code (which is not acceptable to [proj4js](http://proj4js.org/) then this script will use the code to look up the proj4 string at [EPSG.io](https://epsg.io/)). In order for this functionality to work, the script must have access to the internet.

### Usage

```bash
python tif2js.py --input data/Kampala.tif --output band1.js --band 1 --variable band1
```

#### Arguments

* `-h` `--help`: Print help message to the console 
* `-i` `--input`: specify the path to the input raster file (acceptable file types are dictated by support offered in the [rasterio](https://rasterio.readthedocs.io/en/stable/) and [GDAL](https://gdal.org/) libraries)
* `-o` `--output`: specify the path for the output raster file (must be `*.js`)
* `-b` `--bands` (optional) specify the band to be extracted into the JavaScript file *(default all bands)*
* `-v` `--variable` (optional) specify the variable name used to store the resulting object *(default `data`)*

#### Help output

```txt
python tif2js.py -h
usage: tif2js.py [-h] --input INPUT --output OUTPUT
                 [--bands [BANDS [BANDS ...]]] [--variable [VARIABLE]]

Convert GIS raster datasets to a JavaScript representation. You MUST be
connected to the internet for some coordinate definitions to work

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        set the path for the raster to convert to JS
  --output OUTPUT, -o OUTPUT
                        set the path for output .js file
  --bands [BANDS [BANDS ...]], -b [BANDS [BANDS ...]]
                        set the raster bands to convert to JS (default: all
                        bands)
  --variable [VARIABLE], -v [VARIABLE]
                        set the name of the variable that contains the output
                        JS object (default: 'data')
```

### Description of the JavaScript Object Data Structure

#### Properties

* `bands`: The number of bands contained in the dataset
* `.tl`: The coordinates of the top left corner of the raster (in the original CRS of the dataset)  (e.g. `[444440.0, 45000.0]`)
* `.bl`: The coordinates of the bottom left corner of the raster (in the original CRS of the dataset)  (e.g.  `[444440.0, 27890.0]`)
* `.tr`: The coordinates of the top right corner of the raster (in the original CRS of the dataset) (e.g.  `[462100.0, 45000.0]`)
* `.br`: The coordinates of the bottom right corner of the raster (in the original CRS of the dataset) (e.g. `[462100.0, 27890.0]`)
* `.bounds`: The bounds of the raster (in the original CRS of the dataset) (e.g. `[[444440.0, 27890.0] ,[462100.0, 45000.0]]`)
* `.resolution`: The resolution of the raster in the original units of the dataset (e.g. `10`) 
* `.width`: The width of the raster in pixels (e.g. `1766`) 
* `.height`: The height of the raster in pixels (e.g. `1711`) 
* `.proj`: The proj4 string representing the original CRS of the dataset (e.g. `"+proj=utm +zone=36 +datum=WGS84 +units=m +no_defs "`) 
* `.transformer`: A [proj4js]() object providing transformations between the original CRS of the dataset and WGS84 geographical coordinates (e.g. `proj4("+proj=longlat +datum=WGS84 +no_defs", "+proj=utm +zone=36 +datum=WGS84 +units=m +no_defs")`) 

#### Data

The data are stored in two dimensional arrays named `.band1`, `.band2`, `.band3` and so on. Data are accessed in the form `band1[x][y]`.

#### Functions

*All arguments and return values are in an array in the order `[x,y]` (`[lng, lat]`)*

* `.proj2image(coords[])`: convert coordinates between the original CRS of the dataset and image space
* `.image2proj(px[])` convert coordinates between image space and the original CRS of the dataset
* `.proj2geo(coords[])`: transform coordinates between the original CRS of the dataset and WGS84 geographical coordinates
* `.geo2proj(lngLat[])`: transform coordinates between WGS84 geographical coordinates and the original CRS of the dataset
* `.image2geo(pixels[])`: transform coordinates between image space and WGS84 geographical coordinates
* `.geo2image(latLng[])`: transform coordinates between WGS84 geographical coordinates and image space
* `.getGeoBounds()`: return the bounds of the dataset in WGS84 geographical coordinates

#### Convenience Functions

*In order to be more easily compatible with web mapping libraries such as Leaflet, OpenLayers and Google Maps, all geographical coordinates used in the arguments and return values in these variants of the functions are in an array in the order `[y,x]` (`[lat, lng]`)*

* `.proj2geo2(coords[])`: transform coordinates between the original CRS of the dataset and WGS84 geographical coordinates (in the reverse order `[lat, lng]`)
* `.geo2proj2(latLng[])`: transform coordinates between WGS84 geographical coordinates and the original CRS of the dataset (argument provided in the reverse order `[lat, lng]`)
* `.geo2image2(latLng[])`: transform coordinates between WGS84 geographical coordinates and image space (argument provided in the reverse order `[lat, lng]`)
* `.image2geo2(pixels[])`:  transform coordinates between image space and WGS84 geographical coordinates (in the reverse order `[lat, lng]`)
* `.getGeoBounds2()`: return the bounds of the dataset in WGS84 geographical coordinates (in the reverse order `[lat, lng]`)

### Dependencies

This script is written for [Python 3](https://www.python.org/) and is heavily reliant upon the excellent [rasterio](https://rasterio.readthedocs.io/en/stable/) library, which is in turn dependent upon the equally excellent [GDAL](https://gdal.org/) library.

The JavaScript output from the script is heavily reliant upon the excellent [proj4js](http://proj4js.org/) library, which is based upon the equally excellent [proj](https://proj.org/) library.

If a dataset CRS is defined by an EPSG code then this script will use the code to look up the proj4 string at the excellent [EPSG.io](https://epsg.io/)) website.

### Examples

```bash
# convert all bands in Kampala.tif to json
python tif2js.py -i data/Kampala.tif -o kampala.js -v kampala

# convert bands 1 2 and 4 from Kampala.tif to JSON
python tif2js.py -i data/Kampala.tif -o kampala.js -v kampala -b 1 2 4

# convert band 1 from Kampala.tif to json
tif2js.py --input data/Kampala.tif --output band1.js --bands 1 --variable kampala
```



### ToDo List

* Add multi-band support for a single file
* Error handling for EPSG-defined CRS being used when offline


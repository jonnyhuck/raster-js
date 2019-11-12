# raster-js
Convert GIS Raster Datasets to a simple JavaScript object.

This is useful for using raster datasets in libraries such as Leaflet, OpenLayers and Google Maps for applications such as viewsheds, A* Routing algorithm and the calculation of multispectral indices (e.g. NDVI).

### Usage

```bash
python tif2js.py --input data/Kampala.tif --output band1.js --band 1 --variable band1
```

#### Arguments

* `-h` `--help`: Print help message to the console 
* `--input`: specify the path to the input raster file (acceptable file types are dictated by support offered in the excellent [rasterio]() and [GDAL]() libraries)
* `--output`: specify the path for the output raster file (must be `*.js`)
* `--band` (optional) specify the band to be extracted into the JavaScript file *(default 1)*
* `--variable` (optional) specify the variable name used to store the resulting object *(default `data`)*

#### Help output

```txt
python tif2js.py -h
usage: tif2js.py [-h] --input INPUT --output OUTPUT [--band [BAND]]
                 [--variable [VARIABLE]]

Convert GIS raster datasets to a JavaScript representation. You MUST be
connected to the internet for some coordinate definitions to work

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         set the path for the raster to convert to JS
  --output OUTPUT       set the path for output .js file
  --band [BAND]         set the raster band to convert to JS (default: 1)
  --variable [VARIABLE]
                        set the name of the variable that contains the output
                        JS object (default: 'data')
```

### Description of the JavaScript Object Data Structure

#### Properties

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

### ToDo List

* Add multi-band support for a single file


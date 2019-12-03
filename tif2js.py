'''
Convert GIS raster dataset to a simple JavaScript object for use with Leaflet, OpenLayers,
 Google Maps etc.

python tif2js.py -i data/Kampala.tif -o kampala.js -v kampala -b 1 4

@author jonnyhuck
'''
from math import ceil
from requests import get
from numpy import transpose
from argparse import ArgumentParser
from rasterio import open as rio_open

# setup argument parser
parser = ArgumentParser(description='Convert GIS raster datasets to a JavaScript representation.\nYou MUST be connected to the internet for some coordinate definitions to work')
parser.add_argument('--input', '-i', nargs=1, required=True, help='set the path for the raster to convert to JS')
parser.add_argument('--output', '-o', nargs=1, required=True, help='set the path for output .js file')
parser.add_argument('--bands', '-b', nargs='*', required=False, help='set the raster bands to convert to JS (default: all bands)')
parser.add_argument('--variable', '-v', nargs='?', required=False, default='data', help='set the name of the variable that contains the output JS object (default: \'data\')')
args = parser.parse_args()

# validate output file is JavaScript
if args.output[0][-3:] != ".js":
	print("Sorry, " + args.output[0] + " is not a JavaScript file - it should be named in the form: \"*.js\"")
	exit()

# ready to catch errors
try:

	# open input data set
	with rio_open(args.input[0]) as ds:

		# open output file
		file = open(args.output[0],'w')

		# get list of bands if specified, otherwise set to all bands
		if (args.bands):
			bands = [int(x) for x in args.bands]
		else:
			bands = list(range(1, ds.count+1))

		# get projection string (from online if it is EPSG as proj4js doesn't like them)
		if ds.crs.is_epsg_code:
			projString = get("https://epsg.io/" + ds.crs.to_proj4()[11:] + ".proj4").text
		else:
			projString = ds.crs.to_proj4()

		# write JSON object
		file.write ("const " + args.variable + " = { \n")
		file.write ("bands: " + str(bands) + ", \n")
		file.write ("tl: [" + str(ds.bounds.left)  + ", " + str(ds.bounds.top) 	 + "], \n")
		file.write ("bl: [" + str(ds.bounds.left)  + ", " + str(ds.bounds.bottom) + "], \n")
		file.write ("tr: [" + str(ds.bounds.right) + ", " + str(ds.bounds.top)	 + "], \n")
		file.write ("br: [" + str(ds.bounds.right) + ", " + str(ds.bounds.bottom) + "], \n")
		file.write ("bounds: [[" + str(ds.bounds.left)  + ", " + str(ds.bounds.bottom) + "] , [" + str(ds.bounds.right) + ", " + str(ds.bounds.top)	 + "]], \n")
		file.write ("resolution: " + str(int(ds.res[0])) + ", \n")
		file.write ("width: " + str(ds.width) + ", \n")
		file.write ("height: " + str(ds.height) + ", \n")
		file.write ("proj: \"" + projString + "\", \n")
		file.write ("transformer: proj4(\"+proj=longlat +datum=WGS84 +no_defs\", \"" + projString + "\"), \n")

		# convert coordinates from projected space to image space
		file.write ("proj2image: function(coord) { return [parseInt((coord[0] - this.bl[0]) / this.resolution),(this.height - parseInt((coord[1] - this.bl[1]) / this.resolution))]; }, \n")

		# convert coordinates from image space to projected space
		file.write ("image2proj: function(px) { return [this.bl[0] + (px[0] * this.resolution), this.bl[1] + ((this.height - px[1]) * this.resolution)]; }, \n")

		# convert coordinates from projected space to geographic space
		file.write ("proj2geo: function(proj) { return this.transformer.inverse(proj); }, \n")

		# convert coordinates from geographical space to projected space
		file.write ("geo2proj: function(lngLat) { return this.transformer.forward(lngLat); }, \n")

		# convert coordinates from image space to geographical space
		file.write ("image2geo: function(px) { return this.proj2geo(this.image2proj(px)); }, \n")

		# convert coordinates from geographical space to image space
		file.write ("geo2image: function(lngLat) { return this.proj2image(this.geo2proj(lngLat)); }, \n")

		# return bounds in lng lat format
		file.write ("getGeoBounds: function() { return [ this.proj2geo(this.bl), this.proj2geo(this.tr) ]; }, \n")

		# convert coordinates from projected space to geographic space (reversed to latlng)
		file.write ("proj2geo2: function(proj) { return this.transformer.inverse(proj).reverse(); }, \n")

		# convert coordinates from geographical space to projected space (reversed to latlng)
		file.write ("geo2proj2: function(latlng) { return this.transformer.forward(latlng.reverse()); }, \n")

		# convert coordinates from geographical space to image space
		file.write ("geo2image2: function(latlng) { return this.proj2image(this.geo2proj(latlng.reverse())); }, \n")

		# convert coordinates from image space to geographical space (reversed to latlng)
		file.write ("image2geo2: function(px) { return this.proj2geo(this.image2proj(px).reverse()); }, \n")

		# return bounds in lng lat format (reversed to latlng)
		file.write ("getGeoBounds2: function() { return [ this.proj2geo(this.bl).reverse(), this.proj2geo(this.tr).reverse() ]; }, \n")

		# add all bands in one by one
		for b in bands:

			# open the desired band, transpose to make it x,y not y,x
			data = transpose(ds.read()[b-1])	# -1 converts to zero based list ref
			file.write ("band" + str(b) + ": [")
			for row in data:
				out = []
				for col in row:
						out.append(str(int(ceil(col - 0.5))))
				file.write ("[" + ",".join(out) + "],")
			file.write ("\n],\n")

		# close object
		file.write ("\n};")

		# close output file
		file.close()

# catch dodgy rasters
except RasterioIOError:
	print("Sorry, " + args.input[0] + " is not a valid Raster dataset")
	exit()

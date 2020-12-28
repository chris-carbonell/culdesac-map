# create GeoJSON for Leaflet

# general
import pandas as pd
import json

# https://geoffboeing.com/2015/10/exporting-python-data-geojson/
def df_to_geojson(df, properties, lat='latitude', lon='longitude', row_limit = None):
	
	# start geojson
	geojson = {
		'type':'FeatureCollection',
		"crs": {
			"type": "name",
			"properties": {
			  "name": "epsg:3857"
			}
		},
		'features':[]
	}
	
	# build geojson
	row_count = 0
	for _, row in df.iterrows():
		feature = {'type':'Feature',
				   'properties':{},
				   'geometry':{'type':'Point',
							   'coordinates':[]}}
		feature['geometry']['coordinates'] = [row[lat],row[lon]]
		for prop in properties:
			if not(pd.isnull(row[prop])):
				feature['properties'][prop] = row[prop]
			else:
				feature['properties'][prop] = "None"
		geojson['features'].append(feature)
		
		# break if necessary
		row_count += 1
		if row_limit is not None:
			if row_count >= row_limit:
				break
				
	return geojson

# https://stackoverflow.com/questions/16148598/leaflet-update-geojson-filter
def df_to_geojson_filter(df, properties, lat='latitude', lon='longitude', row_limit = None):

	# Filterable GeoJSON
	geojson = {
		'type':'FeatureCollection',
		"crs": {
			"type": "name",
			"properties": {
			  "name": "epsg:3857"
			}
		},
		'features':[]
	}

	# build geojson
	for _, row in df.iterrows():
		
		for prop in properties:
		
			feature = {'type':'Feature',
				   'properties':{},
				   'geometry':{'type':'Point',
							   'coordinates':[]}}
		
			if not(pd.isnull(row[prop])):
				feature['properties'][prop] = row[prop]
			else:
				feature['properties'][prop] = "None"
				
			feature['geometry']['coordinates'] = [row[lat],row[lon]]
		
			geojson['features'].append(feature)

	return geojson

if __name__ == "__main__":

	# get data
	df_data = pd.read_csv("../data/madison_scrub.csv", low_memory = False, index_col = 0)

	# prep args for conversion
	
	lat = "latitude"
	long = "longitude"
	ls_exclude = [lat, long]

	# properties

	# # original
	# ls_properties = []
	# for col in df_data.columns:
	#     if col not in ls_exclude:
	#         ls_properties.append(col)

	# filterable
	ls_properties = [
		"zestimate_central",
		"ElementarySchool",
		"MiddleSchool",
		"HighSchool",
		"YearBuilt",
		"TotalLivingArea",
		"Bedrooms",
		"Baths"
	]

	# create GeoJSON
	# geojson = df_to_geojson(df_data, ls_properties, lat, long, row_limit = 500) # oriinal
	geojson = df_to_geojson_filter(df_data, ls_properties, lat, long, row_limit = 500) # filterable

	# save GeoJSON
	# output_filename = '../data/geodata.geojson' # original
	output_filename = '../data/geodata_filter.geojson' # filterable
	with open(output_filename, "w", encoding="utf8") as output_file:
		json.dump(geojson, output_file, indent=2)
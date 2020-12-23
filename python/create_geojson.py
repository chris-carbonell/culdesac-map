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

if __name__ == "__main__":

	# get data
	df_data = pd.read_csv("../data/madison_scrub.csv", low_memory = False, index_col = 0)

	# prep args for conversion
	
	lat = "latitude"
	long = "longitude"
	ls_exclude = [lat, long]

	# properties
	ls_properties = []
	for col in df_data.columns:
	    if col not in ls_exclude:
	        ls_properties.append(col)

	# create GeoJSON
	geojson = df_to_geojson(df_data, ls_properties, lat, long)

	# save GeoJSON
	output_filename = '../data/geodata.geojson'
	with open(output_filename, "w", encoding="utf8") as output_file:
		json.dump(geojson, output_file, indent=2)
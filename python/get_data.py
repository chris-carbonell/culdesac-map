# get raw property data

# general
import pandas as pd
import time

# requests
import requests

if __name__ == "__main__":

	# get requests session
	session = requests.Session()
	session.headers.update({'User-Agent':
	                        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53' +
	                        '7.36 (KHTML, like Gecko) Chrome/58.0.3029.110 ' +
	                        'Safari/537.36'
	                        })

	# get object IDs for all CIR and CT properties
	str_request = "https://dcimapapps.countyofdane.com/arcgissrv/rest/services/ParcelLayers/MapServer/3/query?where=PropertyStreetTyp%20%3D%20%27CIR%27%20OR%20PropertyStreetTyp%20%3D%20%27CT%27&outFields=*&returnGeometry=false&returnIdsOnly=true&outSR=4326&f=json"
	r = session.get(str_request)
	ls_object_ids = r.json()['objectIds']

	# determine number of items to collect
	# and estimate runtime

	print("len: " + str(len(ls_object_ids)))
	print("estimated download time: " + str(round(len(ls_object_ids)/60,0)) + " min")
	print()

	# to launch or not launch?

	str_launch_code = "download"
	str_launch_input = input("Enter the launch code to proceed: ")

	if str_launch_input == str_launch_code:

	    # download loop
	    for str_object_id in ls_object_ids:

	        str_request = "https://dcimapapps.countyofdane.com/arcgissrv/rest/services/ParcelLayers/MapServer/3/query?where=OBJECTID%20=%20" + str(str_object_id).zfill(5) + "&outFields=*&outSR=4326&f=json"
	        r = session.get(str_request)

	        dict_features = r.json()['features'][0]['attributes'] # since we searched for a single object ID, there's only one item in the list hence 0

	        # https://stackoverflow.com/questions/9390126/pythonic-way-to-check-if-something-exists
	        if 'df_results' not in locals() and 'df_results' not in globals():
	            # df doesn't exist yet, so create it
	            df_results = pd.DataFrame(dict_features, index=[0]) # idc about the index
	        else:
	            # df does exist, so append

	            # convert to dataframe
	            df_append = pd.DataFrame(dict_features, index=[0]) # idc about the index
	            df_results = df_results.append(df_append, ignore_index=True)

	        # sleep
	        time.sleep(1)

	    # save to CSV
	    df_results.to_csv("../data/madison_raw.csv")

	# Example of Response

	# dict_features = r.json()['features'][0]['attributes'] # since we searched for a single object ID, there's only one item in the list hence 0

	# # e.g.,
	# # dict_features = {'OBJECTID': 5653,
	# #  'PARCELNO': '050903411541',
	# #  'CurrentParcel': 'Active',
	# #  'Owner': 'HIGHLANDS OF NETHERWOOD LLC',
	# #  'CoOwner': '',
	# #  'ConctOwner': 'HIGHLANDS OF NETHERWOOD LLC',
	# #  'Attention': '',
	# #  'PropertyAddress': '387 HUMBLE CIR',
	# #  'PrimaryAddress': 'Yes',
	# #  'PropertyStreetNum': '387',
	# #  'PropertyNumSuf': '',
	# #  'PropertyPreDir': '',
	# #  'PropertyStreetNm': 'HUMBLE',
	# #  'PropertyStreetTyp': 'CIR',
	# #  'PropertySuffixDir': '',
	# #  'PropertyUnitTyp': '',
	# #  'PropertyUnitNum': '',
	# #  'PropertyZipCode': '',
	# #  'PropertyZipExt': '',
	# #  'PropertyZipMuni': None,
	# #  'BillingStreetAddress': 'STE 101A 161 HORIZON DR',
	# #  'BillingCtyStZip': 'VERONA WI  53593',
	# #  'BillingCity': 'VERONA',
	# #  'BillingState': 'WI',
	# #  'BillingZip': '53593',
	# #  'Municipality': 'Village of Oregon',
	# #  'MunicipalityCode': '165',
	# #  'MunicipalityFIPS': '60200',
	# #  'MunicipalitySort': 'Oregon, Village of',
	# #  'TOWNSHIP': '05',
	# #  'TOWNSHIPDIRECTION': 'N',
	# #  'RANGE': '09',
	# #  'RANGEDIRECTION': 'E',
	# #  'SECTION': '03',
	# #  'QUARTER160': 'SE',
	# #  'Block': '',
	# #  'Lot': '115',
	# #  'LotType': 'LOT',
	# #  'PlatCode': '091430',
	# #  'PlatDescription': 'HIGHLANDS OF NETHERWOOD',
	# #  'SDStateCode': '4144',
	# #  'SchoolDistrict': 'OREGON SCHOOL DIST',
	# #  'DDStateCode': None,
	# #  'DrainageDistrict': None,
	# #  'LegalDescription': 'HIGHLANDS OF NETHERWOOD LOT 115 (0.359 A)\r\n',
	# #  'Assessed_Acres': 0.359,
	# #  'Sum_LandValue': 96400,
	# #  'Sum_ImprovementValue': 0,
	# #  'Shape.STArea()': 15647.040710449219,
	# #  'Shape.STLength()': 489.9580539730449}
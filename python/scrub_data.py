# scrub data
# filter to ideal properties

# general
import pandas as pd
from datetime import datetime

if __name__ == "__main__":

	# load data
	df_madison = pd.read_csv("../data/madison_raw.csv", index_col = 0, low_memory = False)

	# get school ranking data from school digger
	# except one which we matched via greatschools basically

	dict_rank_elementary = {
	    'Allis': 8.3,
	    'Chavez': 61.6,
	    'Crestwood': 64.2,
	    'Elvehjem': 60.9,
	    'Emerson': 55.8,
	    'Falk': 15.2,
	    'Franklin-Randall': 80.2,
	    'Glendale': 19.7,
	    'Gompers': 26.4,
	    'Hawthorne': 18.5,
	    'Huegel': 46.9,
	    'Kennedy': 37.3,
	    'Lake View': 7.0,
	    'Lapham-Marquette': 69.3,
	    'Leopold': 8.1,
	    'Lindbergh': 35.5,
	    'Lowell': 74.1,
	    'Mendota': 19.3,
	    'Midvale-Lincoln': 34.9,
	    'Muir': 43.1,
	    'Olson': 60, # greatschools 6, niche B
	    'Orchard Ridge': 20,
	    'Sandburg': 20.8,
	    'Schenk': 15.4,
	    'Stephens': 48.2,
	    'Thoreau': 61.5,
	    'Van Hise': 93.7
	}

	dict_rank_middle = {
	    'Black Hawk': 9.7,
	    'Cherokee': 46.2,
	    'Hamilton': 82.6,
	    'Jefferson': 29.8,
	    "O'Keeffe": 35.5,
	    'Opt Cherokee/Hamiltn': 82.6, # max of either
	    'Opt Toki/Jefferson': 29.8, # max of either
	    'Sennett': 15.1,
	    'Sherman': 16.8,
	    'Toki': 30.9,
	    'Whitehorse': 17.3
	}

	dict_rank_high = {
	    'East': 34.8, 
	    'Lafollette': 21,
	    'Memorial': 81.6, 
	    'Optional': 92, # max?
	    'West': 92
	}

	# map dicts
	df_madison['rank_elementary'] = df_madison['ElementarySchool'].map(dict_rank_elementary)
	df_madison['rank_middle'] = df_madison['MiddleSchool'].map(dict_rank_middle)
	df_madison['rank_high'] = df_madison['HighSchool'].map(dict_rank_high)

	# sum
	df_madison['rank_total'] = df_madison['rank_elementary'] + df_madison['rank_middle'] + df_madison['rank_high']

	# baths
	df_madison['Baths'] = df_madison['FullBaths'].astype(float) + 0.5 * df_madison['HalfBaths'].astype(float)

	# # tabulate
	# ls_group = ['ElementarySchool', 'MiddleSchool', 'HighSchool', 
	#             'rank_elementary', 'rank_middle', 'rank_high', 'rank_total']
	# df_madison[ls_group + ['Parcel']].groupby(ls_group).count().sort_values('rank_total', ascending = False)

	# filter to best school districts based on school digger scores
	df_madison_top = df_madison[df_madison['rank_total'] >= 195]

	# save to csv
	df_madison_top.to_csv("../data/madison_scrub.csv")
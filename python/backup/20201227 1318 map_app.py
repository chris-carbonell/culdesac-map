# streamlit app
# map with dynamic filters

# to do
# - remove dependence on zestimate_central (ie rename in CSV)

# general
import math

# data
import pandas as pd
import numpy as np

# app
import streamlit as st
import pydeck as pdk

@st.cache
def from_data_file(df_data, query = None, limit = None):
    
    try:
        
        # get return data
        if query is None:
            df_return = df_data
        else:
            df_return = df_data.query(query)

        # subset if necessary
        if limit is not None:
            return df_return.head(limit)
        else:
            return df_return

    except:
        return None

    return

def get_query_from_dict(dict_query):

    # example dict:
    # dict_query = {
    #     'StreetType': {
    #         'operator': "==",
    #         'condition': "Ct"
    #     },
    #     'YearBuilt': {
    #         'operator': ">=",
    #         'condition': 1990
    #     }
    # }

    # https://stackoverflow.com/questions/45925327/dynamically-filtering-a-pandas-dataframe
    ls_query = []
    for var, dict_condition in dict_query.items():
        ls_query.append(f"{var} {dict_condition['operator']} {repr(dict_condition['condition'])}")
        
    return " & ".join(ls_query)

# table of raw data

# get all data
ls_columns_keep = ['Parcel', 'Address', 'Bedrooms', 'Baths', 'rank_total', 'longitude', 'latitude', 'zestimate_central', 'StreetType', 'HomeStyle', 'PropertyUse', 'AreaName']
df_data = pd.read_csv("./data/madison_scrub.csv", index_col = 0, low_memory = False, usecols = ls_columns_keep)
df_data = df_data.loc[df_data['PropertyUse'] == "Single family"]

# set up sidebar

# https://discuss.streamlit.io/t/filter-logic/3085/2
filter = np.full(len(df_data.index), True)  # Initialize filter as only True

# inputs

st.sidebar.markdown("### Filter Map")

st.sidebar.markdown("#### Property")

# sliders
# key = column name in df_data
# value = slider
sliders = {
    "Bedrooms": st.sidebar.slider(
        "Bedrooms", min_value=0, max_value=max(df_data['Bedrooms']), value=(2,3), step=1
    ),
    "Baths": st.sidebar.slider(
        "Baths", min_value=0.0, max_value=max(df_data['Baths']), value=(2.0,3.0), step=0.5, format = "%.1f"
    ),
    "zestimate_central": st.sidebar.slider(
        "Est. Property Value", min_value=float(0), max_value=float(math.ceil(max(df_data['zestimate_central'])/100000)*100000), value=(float(300000),float(400000)), step=float(10000), format = "%.0f"
    ),
    "rank_total": st.sidebar.slider(
        "Cum. School Score", min_value=float(0), max_value=float(300), value=(float(250),float(300)), step=float(1), format = "%.0f"
    )
}

# Checkboxes
st.sidebar.markdown("#### Location")
cb_cir = st.sidebar.checkbox("Cir", value = True)
cb_ct = st.sidebar.checkbox("Ct", value = True)

# Here we update the filter to take into account the value of each slider
filter = (
    filter
    & (df_data['Bedrooms'] >= sliders['Bedrooms'][0])
    & (df_data['Bedrooms'] <= sliders['Bedrooms'][1])
    & (df_data['Baths'] >= sliders['Baths'][0])
    & (df_data['Baths'] <= sliders['Baths'][1])
    & (df_data['zestimate_central'] >= sliders['zestimate_central'][0])
    & (df_data['zestimate_central'] <= sliders['zestimate_central'][1])
)

# filter for data
if cb_cir:
    if cb_ct:
        filter = filter & (df_data['StreetType'].isin(["Cir","Ct"]))
    else:
        filter = filter & (df_data['StreetType'] == "Cir")
else:
    if cb_ct:
        filter = filter & (df_data['StreetType'] == "Ct")
    else:
        filter = filter & (~df_data['StreetType'].isin(["Cir","Ct"]))

# Other Selections

st.sidebar.markdown("#### Results")

max_results = st.sidebar.text_input("Number of Max Results", 1000)

# subset
df_results = df_data[filter]

# cap at max_results
df_results = df_results.head(int(max_results))

# output

# map

st.subheader('Map')

# set up map layers
ALL_LAYERS = {
    "Cir": pdk.Layer(
        "ScatterplotLayer",
        data=from_data_file(df_results, "StreetType == 'Cir'"),
        get_position=["latitude", "longitude"],
        auto_highlight=True,
        get_radius=10, # Radius is given in meters
        get_fill_color=[180, 0, 200, 140], # Set an RGBA value for fill
        pickable=True
    ),
    "Ct": pdk.Layer(
        "ScatterplotLayer",
        data=from_data_file(df_results, "StreetType == 'Ct'"),
        get_position=["latitude", "longitude"],
        auto_highlight=True,
        get_radius=10, # Radius is given in meters
        get_fill_color=[132, 220, 207, 140], # Set an RGBA value for fill
        pickable=True
    )
}

selected_layers = [] # filter for map
if cb_cir:
    if cb_ct:
        selected_layers += [ALL_LAYERS['Cir'], ALL_LAYERS['Ct']]
    else:
        selected_layers.append(ALL_LAYERS['Cir'])
else:
    if cb_ct:
        selected_layers.append(ALL_LAYERS['Ct'])
    else:
        pass

st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={"latitude": 42.99957799180822,
                        "longitude": -89.43664674446329, "zoom": 11, "pitch": 50},
    layers=selected_layers
))

# Raw Data
st.subheader("Property Details")
st.write(df_results)

# Neighborhood Stats
st.subheader("Neighborhood Stats")
df_neighborhood = df_results[['Address', 'AreaName', 'zestimate_central', 'rank_total']].groupby('AreaName').agg({'Address': "count", 'zestimate_central': np.mean, 'rank_total': np.mean})
st.write(df_neighborhood)

# Summary
st.subheader("Summary")
st.markdown(f"- number of matching properties: {len(df_results.index)}")
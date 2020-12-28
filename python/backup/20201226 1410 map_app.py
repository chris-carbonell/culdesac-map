# streamlit app
# map with dynamic filters

# to do
# - filter zestimate
# - different colors for cir vs ct
# - dynamic bulleted summary of data (e.g., X properties)
# - table breakdown by neighborhood?

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

st.subheader('Raw data')

# get all data
ls_columns_keep = ['Parcel', 'Address', 'Bedrooms', 'Baths', 'rank_total', 'longitude', 'latitude', 'zestimate_central']
df_data = pd.read_csv("./data/madison_scrub.csv", index_col = 0, low_memory = False, usecols = ls_columns_keep)

# set up sidebar

# https://discuss.streamlit.io/t/filter-logic/3085/2
filter = np.full(len(df_data.index), True)  # Initialize filter as only True

# inputs

max_results = st.sidebar.text_input("Number of Max Results", 1000)

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
        "zestimate_central", min_value=float(0), max_value=max(df_data['zestimate_central']), value=(float(300000),float(400000)), step=float(10000)
    ),
    "rank_total": st.sidebar.slider(
        "rank_total", min_value=float(0), max_value=max(df_data['rank_total']), value=(float(250),float(300)), step=float(1), format = "%.0f"
    )
}

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

# subset
df_results = df_data[filter]

# cap at max_results
df_results = df_results.head(int(max_results))

st.write(df_results)

st.subheader("Summary")
st.write(f"number of matches: {len(df_results.index)}")

# testing
st.write(sliders['Bedrooms'][0], sliders['Bedrooms'][1])

# try:
#     ALL_LAYERS = {
#         "Cir": pdk.Layer(
#             "ScatterplotLayer",
#             data=from_data_file("StreetType == 'Cir'"),
#             get_position=["latitude", "longitude"],
#             auto_highlight=True,
#             get_radius=10, # Radius is given in meters
#             get_fill_color=[180, 0, 200, 140], # Set an RGBA value for fill
#             pickable=True
#         ),
#         "Ct": pdk.Layer(
#             "ScatterplotLayer",
#             data=from_data_file("StreetType == 'Ct'"),
#             get_position=["latitude", "longitude"],
#             auto_highlight=True,
#             get_radius=10, # Radius is given in meters
#             get_fill_color=[180, 0, 200, 140], # Set an RGBA value for fill
#             pickable=True
#         )
#     }

#     # sidebar
#     st.sidebar.markdown('### Map Layers')
#     selected_layers = [
#         layer for layer_name, layer in ALL_LAYERS.items()
#         if st.sidebar.checkbox(layer_name, True)]
#     if selected_layers:
#         st.pydeck_chart(pdk.Deck(
#             map_style="mapbox://styles/mapbox/light-v9",
#             initial_view_state={"latitude": 42.99957799180822,
#                                 "longitude": -89.43664674446329, "zoom": 11, "pitch": 50},
#             layers=selected_layers,
#         ))
#     else:
#         st.error("Please choose at least one layer above.")
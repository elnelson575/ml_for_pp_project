import pandas as import import pd
import cenpy
from cenpy import products

conn = products.APIConnection("ACSDT5Y2018")


def get_block_tract_data(features_list):
    data_block = conn.query(features_list, geo_unit = 'block group', geo_filter = {"state": "17","county": "031"}) 

    block_filt = data_block.dropna(axis = 'columns', how='all')

    colnames = list(block_filt.columns)
    features_list2 = [feature for feature in features_list if feature not in colnames] + ['GEO_ID']

    data_tract = conn.query(features_list2, geo_unit = 'tract', geo_filter = {"state": "17","county": "031"})

    merged = block_filt.merge(data_tract, how = "inner", on = ["tract", "state", "county"])
    
    merged = merged.drop(['GEO_ID_y'], axis=1)
    merged = merged.rename(columns={"GEO_ID_x": "GEO_ID"})

    return merged

renamed = cm.rename_to_detailed(primary_data, 2018, features_list)

percents = cm.make_percents(renamed)

filtered = cm.rename_and_filter(percents)
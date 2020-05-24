censusdata.censusvar('acs1', 2015, ['B28009D_001E'])
import censusdata
import pandas as pd
import geopandas as gpd

# Candidate features:
'''
FINAL CODE LIST:

B19013e1 - median household income
B01002_001E - median age

B05001_001E - Total answered nativity question (I think)
B05001_006E - Total not US citizen

B06007_001E - Total from home language
B06007_008E - Speak English less than very well (Other langagues)
B06007_005E - Speak English less than very well (Spanish speaker)

B06009_001E - Total educational attainment question
B06009_002E - Less than HS
B06009_003E - HS or equivalent
B06009_004E - Some college or associates degree
B06009_005E - Bachelor's degree
B06009_006E - Graduate or professional degree

B28010_001E - Computers in household total respondents
B28010_002E - One or more types of computing devices
B28011_001E - Internet subscriptions in household total respondents
B28011_002E - Total with internet subscription
B28011_007E - Total with internet access w/o subscription
B28011_008E - Total no internet

B08014_001E - Vehical availability
B08014_002E - None available
B08014_003E - One available
B08014_004E - Two available

B22003_001E - TOTAL responded receipt of food stamps/snap in past 12 mo by poverty status
B22003_002E - Received food stamps/snap total
B22003_005E - Did not receive food stamps, etc.

C24050_001E - Total Industry by occupation for the civilian employed population over 16 yo
C24050_002E to 0015 - All diff occupations through 15

B17020_001E - total universe poverty status in past 12 months by age
B17020_002E = Total below poverty level
10E = total at or abo e poverty level

B23022_001E - total universe of 16-64 y/o 
B23022_002E - universe men
B23022_003E - men who worked in last 12 mo
B23022_004E - men who worked usually more than 35 hrs per wk in last 12 mo
B23022_025E - men who did not work in past 12 mo
B23022_026E - women universe
B23022_027E - women who worked in last 12 months
B23022_028E - women who usually worked more than 35 hrs per wk
B23022_049E - women didn't work in last 12 months

'''

features_list = [
"GEO_ID", 
"B19013_001E",
"B01002_001E",
"B05001_001E",
"B05001_006E",
"B06007_001E",
"B06007_008E",
"B06007_005E",

"B06009_001E",
"B06009_002E",
"B06009_003E",
"B06009_004E",
"B06009_005E",
"B06009_006E",


"B08014_001E",
"B08014_002E",
"B08014_003E",
"B08014_004E",

"B22003_001E",
"B22003_002E",
"B22003_005E",

"B17020_001E",
"B17020_002E",
"B17020_010E",

"B23022_001E",
"B23022_002E",
"B23022_003E",
"B23022_004E",
"B23022_025E",
"B23022_026E",
"B23022_027E",
"B23022_028E",
"B23022_049E",

"B28010_001E",
"B28010_002E",
"B28011_001E",
"B28011_002E",
"B28011_007E",
"B28011_008E"
]

def pull_raw_census_data(features):
    '''
    Pulls raw census data from API from year 2018 ACS5, requires list of variables to pull
    
    Input:
    features (list): list of census table names to pull from census data

    Output:
    acs_data (pandas df): dataframe with all the variables

    Example:
    primary_data = pull_raw_census_data(features_list)

    '''

    # Note: IL FIPS = 17, Cook County FIPS = 031, Table = B02001_001E (Total Population)
    acs_data = censusdata.download("acs5", 2018, censusdata.censusgeo(
        [("state", "17"), ("county", "031"), ("block group", "*")]), features)
    # Extract 12-digit FIPS code
    acs_data["geo_12"] = acs_data["GEO_ID"].map(lambda x: str(x)[-12:])

    return acs_data



def rename_to_detailed(acs_data, features):
    '''
    This function gets the detailed names of census variables and renames the acs table variables
    accordingly.

    Inputs:
    acs_data (pandas dataframe): ACS data with table name variables as columns
    features (list): list of ACS table names

    Outputs:
    acs_renamed (pandas dataframe): ACS data with column names replaced with detailed variable descriptiosn from Census

    Example: test = rename_to_detailed(primary_data, features_list)
    '''
    features1 = [feature for feature in features if feature != "GEO_ID" and not feature.startswith("C")]
    census_info = censusdata.censusvar('acs5', 2018, features1)

    rename_dict = {}
    for key, value in census_info.items():
        title = value[0].replace(" ", "_")
        subtype = value[1].replace("!!", "_")
        subtype = subtype.replace(" ", "_")
        rename_dict[key] = title + "__" + subtype
    
    
    acs_renamed = acs_data.rename(columns = rename_dict)

    return acs_renamed


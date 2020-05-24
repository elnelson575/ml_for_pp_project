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

def make_percents(acs_renamed):

    # Percent non-citizen
    acs_renamed['Percent_NonCitizen'] = acs_renamed['''NATIVITY_AND_CITIZENSHIP_STATUS_IN_THE_UNITED_STATES__Estimate_Total_Not_a_U.S._citizen'''] / acs_renamed['NATIVITY_AND_CITIZENSHIP_STATUS_IN_THE_UNITED_STATES__Estimate_Total']

    # Percent speak English Poorly
    acs_renamed['Percent_SpeakEngl_Poorly'] = acs_renamed['''PLACE_OF_BIRTH_BY_LANGUAGE_SPOKEN_AT_HOME_AND_ABILITY_TO_SPEAK_ENGLISH_IN_THE_UNITED_STATES__Estimate_Total_Speak_other_languages_Speak_English_less_than_"very_well"''']
    + acs_renamed['''PLACE_OF_BIRTH_BY_LANGUAGE_SPOKEN_AT_HOME_AND_ABILITY_TO_SPEAK_ENGLISH_IN_THE_UNITED_STATES__Estimate_Total_Speak_Spanish_Speak_English_less_than_"very_well"'''] / acs_renamed['''PLACE_OF_BIRTH_BY_LANGUAGE_SPOKEN_AT_HOME_AND_ABILITY_TO_SPEAK_ENGLISH_IN_THE_UNITED_STATES__Estimate_Total''']

    # Educational attainment
    acs_renamed['Percent_less_than_HS'] = acs_renamed['''PLACE_OF_BIRTH_BY_EDUCATIONAL_ATTAINMENT_IN_THE_UNITED_STATES__Estimate_Total_Less_than_high_school_graduate''']/ acs_renamed['''PLACE_OF_BIRTH_BY_EDUCATIONAL_ATTAINMENT_IN_THE_UNITED_STATES__Estimate_Total''']

    acs_renamed['Percent_HS'] = acs_renamed['''PLACE_OF_BIRTH_BY_EDUCATIONAL_ATTAINMENT_IN_THE_UNITED_STATES__Estimate_Total_High_school_graduate_(includes_equivalency)'''] / acs_renamed['''PLACE_OF_BIRTH_BY_EDUCATIONAL_ATTAINMENT_IN_THE_UNITED_STATES__Estimate_Total''']

    acs_renamed['Percent_SomeCollege'] = acs_renamed['''PLACE_OF_BIRTH_BY_EDUCATIONAL_ATTAINMENT_IN_THE_UNITED_STATES__Estimate_Total_Some_college_or_associate's_degree'''] / acs_renamed['''PLACE_OF_BIRTH_BY_EDUCATIONAL_ATTAINMENT_IN_THE_UNITED_STATES__Estimate_Total''']

    acs_renamed['Percent_Bach'] = acs_renamed['''PLACE_OF_BIRTH_BY_EDUCATIONAL_ATTAINMENT_IN_THE_UNITED_STATES__Estimate_Total_Bachelor's_degree'''] / acs_renamed['''PLACE_OF_BIRTH_BY_EDUCATIONAL_ATTAINMENT_IN_THE_UNITED_STATES__Estimate_Total''']

    acs_renamed['Percent_Grad'] = acs_renamed['''PLACE_OF_BIRTH_BY_EDUCATIONAL_ATTAINMENT_IN_THE_UNITED_STATES__Estimate_Total_Graduate_or_professional_degree'''] / acs_renamed['''PLACE_OF_BIRTH_BY_EDUCATIONAL_ATTAINMENT_IN_THE_UNITED_STATES__Estimate_Total''']

    #No vehicals
    acs_renamed['Percent_No_vehicals'] = acs_renamed['''SEX_OF_WORKERS_BY_VEHICLES_AVAILABLE__Estimate_Total_No_vehicle_available'''] / acs_renamed['''SEX_OF_WORKERS_BY_VEHICLES_AVAILABLE__Estimate_Total''']
  
    #SNAP and Benefits

    acs_renamed['Percent_Received_SNAP'] = acs_renamed['''RECEIPT_OF_FOOD_STAMPS/SNAP_IN_THE_PAST_12_MONTHS_BY_POVERTY_STATUS_IN_THE_PAST_12_MONTHS_FOR_HOUSEHOLDS__Estimate_Total_Household_received_Food_Stamps/SNAP_in_the_past_12_months''']/ acs_renamed['''RECEIPT_OF_FOOD_STAMPS/SNAP_IN_THE_PAST_12_MONTHS_BY_POVERTY_STATUS_IN_THE_PAST_12_MONTHS_FOR_HOUSEHOLDS__Estimate_Total''']

    #Work Status

    acs_renamed['Percent_Men_Usually_Fulltime_Employed'] = acs_renamed['''SEX_BY_WORK_STATUS_IN_THE_PAST_12_MONTHS_BY_USUAL_HOURS_WORKED_PER_WEEK_IN_THE_PAST_12_MONTHS_BY_WEEKS_WORKED_IN_THE_PAST_12_MONTHS_FOR_THE_POPULATION_16_TO_64_YEARS__Estimate_Total_Male_Worked_in_the_past_12_months_Usually_worked_35_or_more_hours_per_week'''] / acs_renamed['''SEX_BY_WORK_STATUS_IN_THE_PAST_12_MONTHS_BY_USUAL_HOURS_WORKED_PER_WEEK_IN_THE_PAST_12_MONTHS_BY_WEEKS_WORKED_IN_THE_PAST_12_MONTHS_FOR_THE_POPULATION_16_TO_64_YEARS__Estimate_Total_Male''']

    acs_renamed['Percent_Women_Usually_Fulltime_Employed'] = acs_renamed['''SEX_BY_WORK_STATUS_IN_THE_PAST_12_MONTHS_BY_USUAL_HOURS_WORKED_PER_WEEK_IN_THE_PAST_12_MONTHS_BY_WEEKS_WORKED_IN_THE_PAST_12_MONTHS_FOR_THE_POPULATION_16_TO_64_YEARS__Estimate_Total_Female_Worked_in_the_past_12_months_Usually_worked_35_or_more_hours_per_week'''] / acs_renamed['''SEX_BY_WORK_STATUS_IN_THE_PAST_12_MONTHS_BY_USUAL_HOURS_WORKED_PER_WEEK_IN_THE_PAST_12_MONTHS_BY_WEEKS_WORKED_IN_THE_PAST_12_MONTHS_FOR_THE_POPULATION_16_TO_64_YEARS__Estimate_Total_Female''']

    return acs_renamed

def rename_and_filter(acs_renamed):
    acs_renamed = acs_renamed.rename(columns={"MEDIAN_HOUSEHOLD_INCOME_IN_THE_PAST_12_MONTHS_(IN_2018_INFLATION-ADJUSTED_DOLLARS)__Estimate_Median_household_income_in_the_past_12_months_(in_2018_inflation-adjusted_dollars)" : "Median_Income", "MEDIAN_AGE_BY_SEX__Estimate_Median_age_--_Total" : "Median_Age"})

    filter_cols = [col for col in acs_renamed.columns if col.startswith('Percent') or col.startswith('geo') or col.startswith('Median')]

    acs_filtered = acs_renamed[filter_cols]

    return acs_filtered
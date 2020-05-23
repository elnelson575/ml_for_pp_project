import censusdata
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


# Note: IL FIPS = 17, Cook County FIPS = 031, Table = B02001_001E (Total Population)
acs_data = censusdata.download("acs5", 2015, censusdata.censusgeo(
    [("state", "17"), ("county", "031"), ("block group", "*")]), 
                               ["B02001_001E", "B02001_002E", "B02001_003E", "B02001_004E", "B02010_001E", "B19013_001E", "GEO_ID"])
# Total pop, #White alone, #black alone, # Indigenous alone, #Indigenous in combination with other, # Median income

# Download Census block boundaries for Chicago 
census_gdf = gpd.read_file("https://data.cityofchicago.org/resource/bt9m-d2mf.geojson?$limit=9999999")

# Extract 12-digit FIPS code from both datasets 
census_gdf["geo_12"] = census_gdf["geoid10"].map(lambda x: str(x)[:12])
acs_example["geo_12"] = acs_example["GEO_ID"].map(lambda x: str(x)[-12:])

# Merge ACS data with Census block boundaries 
# Assumes the crime df was converted to a geopandas df (crime_gdf)  
merged_gdf = (gpd.GeoDataFrame(acs_example.merge(census_gdf, on="geo_12", how="inner"), 
                               crs=crime_gdf.crs))

# Limit columns 
limited_gdf = merged_gdf[["B02001_001E", "GEO_ID", "geometry"]].drop_duplicates()

# Plot geopandas dataframe with total population by Census block
limited_gdf.plot()

# Print a sample of rows 
limited_gdf.sample(3)
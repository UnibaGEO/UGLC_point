#-----------------------------------------------------------------------------------------------------------------------
#                                              UGLC DATAFRAME CONVERTER
#-----------------------------------------------------------------------------------------------------------------------
# native dataframe:     GFLD - Global fatal landslide occurrence from 2004 to 2016, Froude, M. J. and Petley, D. N
#-----------------------------------------------------------------------------------------------------------------------
# Conversion
#-----------------------------------------------------------------------------------------------------------------------

import pandas as pd
import json


import pandas as pd
import json

# Native Dataframe 02_COOLR_NATIVE loading
df_OLD = pd.read_csv("../../00.INPUT/NATIVE_DATASET/02_COOLR_NATIVE.csv",low_memory=False)

# JSON Lookup Tables Loading
with open('02_COOLR_LOOKUPTABLES.json', 'r') as file:
    lookup_config = json.load(file)
    lookup_tables = lookup_config["02_COOLR LOOKUP TABLES"]

df_OLD['injuries'].fillna('ND', inplace=True)
df_OLD['fatalities'].fillna('ND', inplace=True)

# Application of lookup Tables to the columns of the old DataFrame
for column in df_OLD.columns:
    lookup_table_key = f"{column}_lookup"  # Lookup table match-Key construction

    # Lookup Tables check if is a string or a dictionary
    if lookup_table_key in lookup_tables and isinstance(lookup_tables[lookup_table_key], dict):
        lookup_table = lookup_tables[lookup_table_key]

        # If the lookup table is marked as "ND" the sytem will keep the original content
        if lookup_table == "ND":
            continue
        else:
            # Update just the no-"ND" columns
            df_OLD[column] = df_OLD[column].map(lambda x: lookup_table.get(str(x), x))

# null values replacement in the Native Dataframe
df_OLD = df_OLD.fillna("ND")

# New dataframe Configuration
new_data = {
    'WKT_GEOM': [],
    'NEW DATASET': [],
    'ID': [],
    'OLD DATASET': [],
    'OLD ID': [],
    'VERSION': [],
    'COUNTRY': [],
    'ACCURACY': [],
    'START DATE': [],
    'END DATE': [],
    'TYPE': [],
    'TRIGGER': [],
    'AFFIDABILITY': [],
    'PSV': [],
    'DCMV': [],
    'FATALITIES': [],
    'INJURIES': [],
    'NOTES': [],
    'LINK': []
}

# New dataframe Creation
df_NEW = pd.DataFrame(new_data)

# New Dataframe Updating with the Old Dataframe columns content values
df_NEW['WKT_GEOM'] = df_OLD['WKT']
df_NEW['NEW DATASET'] = "UGLC"
df_NEW['ID'] = range(1, len(df_OLD) + 1)
df_NEW['OLD DATASET'] = df_OLD['source']
df_NEW['OLD ID'] = df_OLD['ev_id']
df_NEW['VERSION'] = "2019"
df_NEW['COUNTRY'] = df_OLD['ctry_name']
df_NEW['ACCURACY'] = df_OLD['loc_acc']
df_NEW['START DATE'] = df_OLD['ev_date'].replace('ND', '1956/01/01')
df_NEW['END DATE'] = df_OLD['ev_date'].replace('ND', '2023/01/01')
df_NEW['TYPE'] = df_OLD['ls_cat']
df_NEW['TRIGGER'] = df_OLD['ls_trig']
df_NEW['AFFIDABILITY'] = "CALC"
df_NEW['PSV'] = "CALC"
df_NEW['DCMV'] = "CALC"
df_NEW['FATALITIES'] = df_OLD['fatalities']
df_NEW['INJURIES'] = df_OLD['injuries']
df_NEW['NOTES'] = "Cooperative Open Online Landslide Repository - NASA, locality: " + df_OLD['loc_desc'] + ", description: " + df_OLD['ev_desc']
df_NEW['LINK'] = "Source: " + df_OLD['src_link']

print(df_OLD['fatalities'].unique())
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
# Corrections
#-----------------------------------------------------------------------------------------------------------------------f

from function import apply_country_corrections
from function import apply_affidability_calculator


apply_country_corrections(df_NEW)
apply_affidability_calculator(df_NEW)
print(df_NEW['FATALITIES'])
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
# Output
#-----------------------------------------------------------------------------------------------------------------------

# Creation of the new updated Dataframe as a .csv file in the selected directory
df_NEW.to_csv('../../02.OUTPUT/DATASET_CONVERTED/02_COOLR_CONVERTED.csv', index=False)
print("________________________________________________________________________________________")
print("COOLR-report points successfully converted as COOLR_02_CONVERTED.csv in the DATASET_CONVERTED directory")
print("________________________________________________________________________________________")
#-----------------------------------------------------------------------------------------------------------------------
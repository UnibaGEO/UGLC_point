#-----------------------------------------------------------------------------------------------------------------------
#                                              UGLC DATAFRAME CONVERTER
#-----------------------------------------------------------------------------------------------------------------------
# native dataframe:     VLS -  Vermont Geological Survey's preliminary landslide inventory
#-----------------------------------------------------------------------------------------------------------------------
# Conversion
#-----------------------------------------------------------------------------------------------------------------------
import pandas as pd
import json
import os
from dotenv import load_dotenv
from lib.function_collection import apply_affidability_calculator

# Load the enviroment variables from config.env file
load_dotenv("../../config.env")
root = os.getenv("FILES_REPO")

# Native Dataframe 01_COOLR_native loading
df_OLD = pd.read_csv(f"{root}/input/native_datasets/12_VLS_native.csv", low_memory=False, encoding="utf-8")

# JSON Lookup Tables Loading
with open('12_VLS_lookuptables.json', 'r', encoding="utf-8") as file:
    lookup_config = json.load(file)
    lookup_tables = lookup_config["12_VLS LOOKUP TABLES"]

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

df_OLD['LS_TYPE1'] = df_OLD['LS_TYPE1'].fillna('ND')
df_OLD['TOWN'] = df_OLD['TOWN'].fillna('ND')
df_OLD['COMMENTS'] = df_OLD['COMMENTS'].fillna('ND')
df_OLD['SOURCE'] = df_OLD['SOURCE'].fillna('ND')

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
df_NEW['WKT_GEOM'] = df_OLD['geometry']
df_NEW['NEW DATASET'] = "UGLC"
df_NEW['ID'] = "CALC"
df_NEW['OLD DATASET'] = "Vermont Geological Survey's preliminary landslide inventory"
df_NEW['OLD ID'] = df_OLD['OBJECTID']
df_NEW['VERSION'] = "Last update 2024/03/05"
df_NEW['COUNTRY'] = "United States of America"
df_NEW['ACCURACY'] = df_OLD['FIELD_VISI']
df_NEW['START DATE'] = df_OLD['START DATE']
df_NEW['END DATE'] = df_OLD['END DATE']
df_NEW['TYPE'] = df_OLD['LS_TYPE1']
df_NEW['TRIGGER'] = df_OLD['TRIGGER']
df_NEW['AFFIDABILITY'] = "CALC"
df_NEW['PSV'] = "CALC"
df_NEW['DCMV'] = "CALC"
df_NEW['FATALITIES'] = "-99999"
df_NEW['INJURIES'] = "-99999"
df_NEW['NOTES'] = df_OLD.apply(lambda row: f"VLS - locality: Vermont, {repr(row['TOWN'])} - description: {repr(row['COMMENTS'])} ", axis=1)
df_NEW['LINK'] = df_OLD.apply(lambda row: f"Source: {row['SOURCE']}", axis=1)

#-----------------------------------------------------------------------------------------------------------------------
# Corrections
#-----------------------------------------------------------------------------------------------------------------------

apply_affidability_calculator(df_NEW)

#-----------------------------------------------------------------------------------------------------------------------
# Output
#-----------------------------------------------------------------------------------------------------------------------

# Creation of the new updated Dataframe as a .csv file in the selected directory
df_NEW.to_csv(f"{root}/output/converted_csv/12_VLS_converted.csv", sep=',', index=False, encoding="utf-8")

print("__________________________________________________________________________________________")
print("                             12_VLS_native conversion: DONE                               ")
print("__________________________________________________________________________________________")
#--------------------------------------------------------------------------------------------------------------------
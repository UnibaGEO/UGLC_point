#-----------------------------------------------------------------------------------------------------------------------
#                                              UGLC DATAFRAME CONVERTER
#-----------------------------------------------------------------------------------------------------------------------
# native dataframe:     ALC - Landslide Inventories across the United States version2_USGS, Mirus, B.B., Jones, E.S., Baum, R.L. et al.
#-----------------------------------------------------------------------------------------------------------------------
# Conversion
#-----------------------------------------------------------------------------------------------------------------------
import numpy as np
import pandas as pd
import json
import os
from dotenv import load_dotenv
from lib.function_collection import trasforma_accuracy,apply_affidability_calculator,trasforma_data_end,trasforma_data_start,assign_country_to_points

# Load the enviroment variables from config.env file
load_dotenv("../../config.env")
root = os.getenv("FILES_REPO")

# Native Dataframe 01_COOLR_native loading
df_OLD = pd.read_csv(f"{root}/input/native_datasets/07_RBR_native.csv", low_memory=False,encoding="utf-8")
print(df_OLD.columns.values)

df_OLD['Year'] = df_OLD['Year'].astype(str)
print(df_OLD['Year'].dtypes)
print(df_OLD['Year'].unique())
#null values replacement in the Native Dataframe


# JSON Lookup Tables Loading
with open('07_RBR_LOOKUPTABLES.json', 'r',encoding="utf-8") as file:
    lookup_config = json.load(file)
    lookup_tables = lookup_config["07_RBR LOOKUP TABLES"]



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
df_NEW['WKT_GEOM'] = df_OLD['WKT_GEOM']
df_NEW['NEW DATASET'] = "UGLC"
df_NEW['ID'] = "CALC"
df_NEW['OLD DATASET'] = "RBR"
df_NEW['OLD ID'] = df_OLD['ID']
df_NEW['VERSION'] = "Version v1.0"
df_NEW['COUNTRY'] = assign_country_to_points(df_OLD)['NAME']
df_NEW['ACCURACY'] = "calc"
df_NEW['START DATE'] = df_OLD['Year'].apply(trasforma_data_start)
df_NEW['END DATE'] = df_OLD['Year'].apply(trasforma_data_end)
df_NEW['TYPE'] = "ND"
df_NEW['TRIGGER'] = "ND"
df_NEW['AFFIDABILITY'] = "CALC"
df_NEW['PSV'] = "CALC"
df_NEW['DCMV'] = "CALC"
df_NEW['FATALITIES'] = "-99999"
df_NEW['INJURIES'] = "-99999"
#df_NEW['NOTES'] = df_NEW.apply(lambda row:f"SHALLOW LANDSLIDE INVENTORY  for 2000-2019 (eastern DRC, Rwanda, Burundi) -locality:{row['COUNTRY']},description:ND" )
df_NEW['LINK'] ="Source: ND"

#-----------------------------------------------------------------------------------------------------------------------
# Corrections
#-----------------------------------------------------------------------------------------------------------------------

#apply_affidability_calculator(df_NEW)


#-----------------------------------------------------------------------------------------------------------------------
# Output

# Creation of the new updated Dataframe as a .csv file in the selected directory
df_NEW.to_csv(f"{root}/output/converted_csv/07_RBR_converted.csv", sep=',', index=False,encoding="utf-8")

print("__________________________________________________________________________________________")
print("                             05_ALC_native conversion: DONE                             ")
print("__________________________________________________________________________________________")
#--------------------------------------------------------------------------------------------------------------------

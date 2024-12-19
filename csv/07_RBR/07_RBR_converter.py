#-----------------------------------------------------------------------------------------------------------------------
#                                              UGLC DATAFRAME CONVERTER
#-----------------------------------------------------------------------------------------------------------------------
# native dataframe:     RBR - Shallow Landslide Inventory for 2000-2019 (eastern DRC, Rwanda, Burundi), Arthur Depicker, Gerard Govers, et al.
#-----------------------------------------------------------------------------------------------------------------------
# Conversion
#-----------------------------------------------------------------------------------------------------------------------
import numpy as np
import pandas as pd
import json
import os
from dotenv import load_dotenv
from lib.function_collection import apply_RELIABILITY_calculator, trasforma_data_end, trasforma_data_start, assign_country_to_points

# Enviroment loading from config.env file -----------------------------------------------------------------------

load_dotenv("../../config.env")
files_repo = os.getenv("FILES_REPO")
files_repo_linux = os.getenv("FILES_REPO_LINUX")

# Verify if its there is a Windows G-Drive files repo or a Linux G-Drive files repo
if os.path.exists(files_repo):
    root = files_repo
else:
    root = files_repo_linux

print(f"Using root= {root}")

# -----------------------------------------------------------------------

# Native Dataframe 01_COOLR_native loading
df_OLD = pd.read_csv(f"{root}/input/native_datasets/07_RBR_native.csv", low_memory=False,encoding="utf-8")

# JSON Lookup Tables Loading
with open('07_RBR_lookuptables.json', 'r', encoding="utf-8") as file:
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

df_OLD['Year'] = df_OLD['Year'].astype(str)

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
    'PHYSICAL FACTORS': [],
    'RELIABILITY': [],
    'RECORD TYPE': [],
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
df_NEW['OLD DATASET'] = "Shallow Landslide Inventory for 2000-2019 (eastern DRC, Rwanda, Burundi)"
df_NEW['OLD ID'] = df_OLD['ID']
df_NEW['VERSION'] = str("Version v1.0")
df_NEW['COUNTRY'] = assign_country_to_points(df_OLD)['NAME'].replace('Dem. Rep. Congo', 'Democratic Republic of Congo')
df_NEW['ACCURACY'] = (np.sqrt(df_OLD['area'].astype(float) / np.pi)).apply(round).astype(int)
df_NEW['START DATE'] = df_OLD['Year'].apply(trasforma_data_start)
df_NEW['END DATE'] = df_OLD['Year'].apply(trasforma_data_end)
df_NEW['TYPE'] = "ND"
df_NEW['PHYSICAL FACTORS'] = "deforestation (P)"
df_NEW['RELIABILITY'] = "CALC"
df_NEW['RECORD TYPE'] = "event"
df_NEW['FATALITIES'] = "-99999"
df_NEW['INJURIES'] = "-99999"
df_NEW['NOTES'] = df_NEW.apply(lambda row:f"RBR - locality: {repr(row['COUNTRY'])} - description: ND ",axis=1)
df_NEW['LINK'] ="Source: ND"

#-----------------------------------------------------------------------------------------------------------------------
# Corrections
#-----------------------------------------------------------------------------------------------------------------------

apply_RELIABILITY_calculator(df_NEW)

#-----------------------------------------------------------------------------------------------------------------------
# Output
#-----------------------------------------------------------------------------------------------------------------------

# Creation of the new updated Dataframe as a .csv file in the selected directory
df_NEW.to_csv(f"{root}/output/converted_csv/07_RBR_converted.csv", sep=',', index=False,encoding="utf-8")

print("__________________________________________________________________________________________")
print("                             07_RBR_native conversion: DONE                               ")
print("__________________________________________________________________________________________")
#--------------------------------------------------------------------------------------------------------------------
